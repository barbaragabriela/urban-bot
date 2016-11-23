# -*- coding: utf-8 -*-

import os

TOKEN = os.environ.get('TOKEN',"")

URBAN_URL = 'http://api.urbandictionary.com/v0/'
URBAN_WEB_URL = 'http://www.urbandictionary.com/define.php?'
DEFINE_URL = 'define?'
RANDOM_URL = 'random'

HELP = """
urbanBot helps you query urbandictionary from the commodity of your telegram chat 👻👻👻

to define something use the ```/define``` command.

to get a random definition use the ```/random``` command.

each command returns one definition but you can ask for more adding the number of definitions you want, for example:
```/random 5```
or 
```/define hello 2```
"""