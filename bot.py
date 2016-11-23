# -*- coding: utf-8 -*-

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.error import TelegramError
import urllib
import json
import logging

import config
import helper


class UrbanBot:
    def __init__(self):
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
        self.logger = logging.getLogger()
        self.updater = Updater(token=config.TOKEN)
        self.dispatcher = self.updater.dispatcher
        self.updater.start_polling()


    def start(self):
        help_handler = CommandHandler('help', self.helpsies)
        self.dispatcher.add_handler(help_handler)

        define_handler = CommandHandler('define', self.define)
        self.dispatcher.add_handler(define_handler)

        random_handler = CommandHandler('random', self.random)
        self.dispatcher.add_handler(random_handler)


    def helpsies(self, bot, update):
        bot.sendMessage(chat_id=update.message.chat_id, text=config.HELP, parse_mode='Markdown')


    def define(self, bot, update):
        text = update.message.text
        term = text.split("/define")[-1].encode('utf-8').strip()
        self.logger.info('SEARCH TERM: "{}"'.format(term))

        query_params = {
            'term': '{}'.format(term)
        }
        query_params = urllib.urlencode(query_params)
        query_url = config.URBAN_URL + config.DEFINE_URL + query_params
        response = json.loads(urllib.urlopen(query_url).read())

        if len(response['list']) == 0:
            bot_response = '*¯\_(ツ)_/¯* \n"_{}_"not found'.format(term)
        else:
            bot_response = '*{}*\n\n'.format(term)
            for idx, value in enumerate(response['list']):
                definition = helper.make_pretty(value['definition'].encode('utf-8'))
                example = helper.make_pretty(value['example'].encode('utf-8'))

                formated_definition = '*{}*. {}\n _{}_\n\n'.format(idx+1, definition, example)
                if len(bot_response + formated_definition) <= 4096:
                    bot_response = bot_response + formated_definition
                else:
                    break

        send_message(bot, update, bot_response, term)


    def random(self, bot, update):
        text = update.message.text
        arg = text.split("/random")[-1].encode('utf-8').strip()

        query_url = config.URBAN_URL + config.RANDOM_URL
        response = json.loads(urllib.urlopen(query_url).read())
        bot_response = ''
        try:
            arg = int(arg)
        except ValueError:
            arg = 1

        for i, value in enumerate(response['list']):
            if arg == i:
                break
            term = value['word']
            definition = helper.make_pretty(value['definition'].encode('utf-8'))
            example = helper.make_pretty(value['example'].encode('utf-8'))
            formated_definition = '*{}*\n {}\n _{}_\n→{}\n'.format(term, definition, example, value['permalink'])
            if len(bot_response + formated_definition) <= 4096:
                bot_response = bot_response + formated_definition
            else:
                break

        send_message(bot, update, bot_response)


def send_message(bot, update, bot_response, term=None):
    try:
        bot.sendMessage(chat_id=update.message.chat_id, text=bot_response, parse_mode='Markdown')
    except TelegramError:
        if term is None:
            error = 'There was an error retrieveing a random word, probably they messed with the _Markdown_ 👀👀👀'
        else:
            error = 'There was an error in retrieving *{}*, probably they messed with the _Markdown_ 👀👀👀'.format(term)
        bot.sendMessage(chat_id=update.message.chat_id, text=error, parse_mode='Markdown')


if __name__ == '__main__':
    bot = UrbanBot()
    bot.start()
