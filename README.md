# PFAF Bot
## Pull PFAF data directly onto your Discord server.

PFAF Bot identifies pulls data directly from [PFAF], displaying it in code blocks in your Discord server. This bot was written as a proof of concept, utilising web scraping of aspx pages.

This bot is not currently in any of my servers, therefore there is no invite link. Please feel free to host it somewhere and add it to your server, and let me know so that I can actively maintain the code!

## Features

- Returns latin names of plants that were searched for by common names
- Returns the details of a plant that was serached for by latin name
- Takes an optional 'verbose' argument to return multiple pages of data
- Uses Discord's slash commands

## Prerequisites

Plant ID Bot uses a small number of prerequisites in order to work properly:

- [Pycord] -  a modern, easy to use, feature-rich, and async ready API wrapper for Discord, written in Python
- [PrettyTable] - A simple Python library for easily displaying tabular data in a visually appealing ASCII table format
- [Beautiful Soup] - a python library for pulling data out of HTML and XML files
- [python-dotenv] - for reading local .env files during development

## Installation

If you fork this repository and wish to host your own version of this bot, you will need to:

- Create a new application and bot at the [Discord Developer Portal](https://discord.com/developers/applications). Follow this [guide](https://realpython.com/how-to-make-a-discord-bot-python/) if you are unsure
- create a local .env file to store your bot's secret token under 'DISCORD_TOKEN'
- Enable the bot permissions 'Read Messages/View Channels', 'Send Messages', 'Embed Links', 'Add Reactions'
- Enable 'application.commands' permissions
- Host the files on your platform of choice. A procfile is included if you wish to use [Heroku](https://www.heroku.com)
- Add the bot's secret token to your platform's environment variables under the key 'DISCORD_TOKEN' 

## Development

Want to contribute? Simply fork, clone, edit and then create a pull request. Details of how to do this can be found [here](https://www.digitalocean.com/community/tutorials/how-to-create-a-pull-request-on-github).

## Credits
- [themanifold](https://github.com/themanifold) who cast his careful eye over the code, making sure that I wasn't making any obvious errors, and for making my todo list longer each day

## License

MIT

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

   [git-repo-url]: <https://github.com/TheRealOwenRees/plantID_discordbot>
   [PrettyTable]: <https://pypi.org/project/prettytable/>
   [PFAF]: <https://pfaf.org>
   [Pycord]: <https://pycord.dev/>
   [python-dotenv]: <https://pypi.org/project/python-dotenv/>
   [Beautiful Soup]: <https://beautiful-soup-4.readthedocs.io/en/latest/>
