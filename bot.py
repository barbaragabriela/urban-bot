# -*- coding: utf-8 -*-

from telegram.ext import Updater
from telegram.ext import CommandHandler
import urllib
import json
import logging

import config


class UrbanBot:
    def __init__(self):
        self.updater = Updater(token=config.TOKEN)
        self.logger = logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
        self.dispatcher = self.updater.dispatcher

        self.updater.start_polling()


    def start(self):
        help_handler = CommandHandler('help', self.helpsies)
        self.dispatcher.add_handler(help_handler)

        define_handler = CommandHandler('define', self.define)
        self.dispatcher.add_handler(define_handler)


    def helpsies(self, bot, update):
        bot.sendMessage(chat_id=update.message.chat_id, text=config.HELP, parse_mode='Markdown')


    def define(self, bot, update):
        text = update.message.text
        term = text.split("/define")[-1].strip()
        query_params = {
            'term': '{}'.format(term)
        }
        query_params = urllib.urlencode(query_params)
        query_url = config.URBAN_URL + query_params
        response = json.loads(urllib.urlopen(query_url).read())
        if len(response['list']) == 0:
            bot_response = '*¯\_(ツ)_/¯* \n_{}_ not found'.format(term)
        else:
            bot_response = '*{}*\n\n'.format(term)
            for idx, value in enumerate(response['list']):
                definition = value['definition'].encode('utf-8')
                example = value['example'].encode('utf-8')
                bot_response = bot_response + '{}. {}\n _{}_\n{}\n'.format(idx+1, definition, example, config.DIVISION)

                if idx == 2: # temporal so i dont get the 4096 characters error
                    break

        bot.sendMessage(chat_id=update.message.chat_id, text=bot_response, parse_mode='Markdown')

bot = UrbanBot()
bot.start()
