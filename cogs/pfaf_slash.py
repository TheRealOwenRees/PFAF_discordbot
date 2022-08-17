import requests
import re

from bs4 import BeautifulSoup
from prettytable import PrettyTable, ALL

import discord
from discord import option
from discord.ext.commands import Cog, slash_command


class PfafSlashCommands(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.useragent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:103.0) Gecko/20100101 Firefox/103.0'
        self.headers = {
            'User-Agent': self.useragent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-GB,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        # initial url to retrieve essential form values for aspx scraping
        self.get_url = requests.get('https://pfaf.org/user/DatabaseSearhResult.aspx', headers=self.headers)
        self.soup_dummy = BeautifulSoup(self.get_url.content, 'html.parser')
        self.viewstate = self.soup_dummy.find('input', id='__VIEWSTATE')
        self.viewstategen = self.soup_dummy.find('input', id='__VIEWSTATEGENERATOR')

    @slash_command(name='search', description='search for a plant by a common name')
    async def search(self, ctx: discord.ApplicationContext, common_name: str):

        search_url = 'https://pfaf.org/user/Default.aspx'

        data = {
            '__VIEWSTATE': self.viewstate,
            '__VIEWSTATEGENERATOR': self.viewstategen,
            'ctl00$ContentPlaceHolder1$txtSearch': common_name,
            '__EVENTTARGET': 'ctl00$ContentPlaceHolder1$imgbtnSearch1'
        }

        # parse the result page HTML
        res = requests.post(search_url, headers=self.headers, data=data)
        soup = BeautifulSoup(res.content, 'html.parser')
        
        # new ascii table instance
        ascii_table = PrettyTable()
        ascii_table.hrules=ALL

        # find the table that contains the results
        try:
            rows = soup.find('table', id='ContentPlaceHolder1_gvresults').find_all('tr')
        except Exception:
            await ctx.respond(f'```There was no response from PFAF. This likely means that your search returned nothing. Please try again```')

        # find table headers + add to ascii_table
        th = rows[0].find_all('th')

        ascii_table.field_names = [
            th[0].get_text(),
            th[1].get_text(),
            # th[2].get_text(), # th[3].get_text(), # th[4].get_text(), # th[5].get_text(), # th[6].get_text(), # th[7].get_text(), # th[8].get_text(), # th[9].get_text(), # th[10].get_text(),
        ]

        for row in rows[1:]:
            content = row.find_all('td')
            latin_name = content[0].get_text()
            common_name = content[1].get_text()
            # habit = content[2].get_text() # height = content[3].get_text() # hardiness = content[4].get_text() # growth = content[5].get_text() # soil = content[6].get_text() # shade = content[7].get_text() # moisture = content[8].get_text() # edible = content[9].get_text() # medicinal = content[10].get_text()

            ascii_table.add_row([
                latin_name.replace(' ', '\n'), 
                common_name.replace(',', '\n'),
                # habit, # height, # hardiness, # growth, # soil, # shade, # moisture, # edible, # medicinal,
            ])

        ascii_table_str = ascii_table.get_string()
        print(ascii_table_str)

        await ctx.respond(f'```{ascii_table_str if len(ascii_table_str) <= 2000 else "Your search returned too many results to display. Please narrow your search"}```')
        

    @slash_command(name="details", description='find plant details by latin name')
    @option("verbose", choices=["no", "yes"], default="no", description='return all details (lots of messages!')
    async def details(self, ctx: discord.ApplicationContext, latin_name: str, verbose: str):

        details_url = "https://pfaf.org/user/Plant.aspx?LatinName="
        res = requests.get(f'{details_url}{latin_name}', headers=self.headers)
        soup = BeautifulSoup(res.content, 'html.parser')


        async def basic_details(ctx: discord.ApplicationContext):
            try:
                table_title = soup.find('span', id='ContentPlaceHolder1_lbldisplatinname').text
                if len(table_title) < 3:
                    raise Exception
                rows = soup.find('table', class_='table table-hover table-striped').find_all('tr')
            except Exception:
                await ctx.respond(f'```Your search has returned nothing```')

            message_str = f'**{table_title}**\n<{res.url}>\n'

            for row in rows[:10]:
                content = row.find_all('td')
                left_text = content[0].get_text().strip()
                right_text = content[1].get_text().strip()
                message_str += f'```{left_text}:\n\t{right_text}\n\n```\n\n'

            # separate 'care info' due to needing to retrieve 'alt' data
            care_info_str = f'{rows[10].find("td").get_text().strip()}:\n'
            care_info_table = rows[10].find('table', id='ContentPlaceHolder1_tblIcons')
            img_row = care_info_table.find_all('img', alt=True)
            for img in img_row:
                care_info_str += f'\t{img.get("alt")}\n'
            care_info_block = f'```{care_info_str}```'

            await ctx.respond(f'Here are the details for: {message_str}{care_info_block}')
        
        
        async def verbose_details(ctx: discord.ApplicationContext):
            await basic_details(ctx)

            rows = soup.find_all('span')
            rsub = r'\[[^\]]*\]'   # regex pattern to remove square brackets and their contents
            
            def content(title, row_num):
                title += ':\n\t'
                content_str = re.sub(rsub, '', f'{rows[row_num].get_text()}')
                if (len(content_str) > 2000):
                    return f'```{title}Too long to display here, please visit the PFAF.org link at the top of the first message```' 
                elif (len(content_str) == 0):
                    return f'```{title}N\\A```'
                else:
                    return f'```{title}{content_str}```'  
            
            summary = content('Summary', 15)
            phy_char = content('Physical Characteristics', 16)
            synonyms = content('Synonyms', 17)
            habitats = content('Habitats', 18)
            edible_uses = content('Edible Uses', 19)
            medicinal_uses = content('Medicinal Uses', 20)
            other_uses = content('Other Uses', 22)
            special_uses = content('Special Uses', 23)
            cultivation = content('Cultivation', 24)
            propagation = content('Propagation', 27)

            await ctx.respond(f'{summary}\n\n{phy_char}\n\n{synonyms}\n\n{habitats}')
            await ctx.respond(f'{edible_uses}\n\n{medicinal_uses}')
            await ctx.respond(f'{other_uses}\n\n{special_uses}')
            await ctx.respond(f'{cultivation}')
            await ctx.respond(f'{propagation}')

        await basic_details(ctx) if verbose == "no" else await verbose_details(ctx)

