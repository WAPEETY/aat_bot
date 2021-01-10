from time import sleep
import telepotpro

from telepotpro import Bot, glance
from telepotpro.exception import TelegramError, BotWasBlockedError
from telepotpro.namedtuple import InlineQueryResultArticle, InlineQueryResultPhoto, InputTextMessageContent

from threading import Thread
from datetime import datetime, timedelta
from json import load as jsload
from os.path import abspath, dirname, join

import phrase

with open(join(dirname(abspath(__file__)), "settings.json")) as settings_file:
    js_settings = jsload(settings_file)

bot = Bot(js_settings["key"])
maintenance = js_settings["maintenance"]


if not maintenance:
    print("Bot Started Successfully")
else:
    print("WARNING! You started the bot is in maintenance mode, change this setting in settings.json")


def reply(msg):
    global maintenance
    
    
    chatId = msg['chat']['id']
    name = msg['from']['first_name']
    
    try:
        text = msg['text']
    except ValueError:
        text = ""
    
    command = getCommand(text).lower()

    if not maintenance:
        if command == "/dona":
            bot.sendMessage(chatId, "Ecco qui il mio link PayPal, Grazie mille! ❤️\n"
                                    "https://www.paypal.me/wapeetyofficial")
        
        elif command == "/source":
            bot.sendMessage(chatId, "Ecco qui il link Github, Aggiungi una stellina! 😘\n"
                                    "https://github.com/WAPEETY/aatf_bot")

        elif command == "/start":
            bot.sendMessage(chatId, "Benvenuto❗️\n"
                                    "\n"
                                    "<i>Questo bot funziona inline</i>\n\n"
                                    "Vai in una qualsiasi chat e scrivi @aatf_bot per usarlo", parse_mode="HTML")
        
        elif command == "/help":
            bot.sendMessage(chatId, "<i>Questo bot funziona inline</i>\n\n"
                                    "Vai in una qualsiasi chat e scrivi @aatf_bot per usarlo", parse_mode="HTML")

        else:
            bot.sendMessage(chatId, "Comando non riconosciuto ☹️")
    else:
        bot.sendMessage(chatId, "⚠️ <b>Bot Attualmente in manutenzione.</b> ⚠️\n"
                                "<i>Ci scusiamo per il disagio.</i>", parse_mode="HTML")


def getCommand(content):
    t=0
    output = ""
    for i in content:
        if i != " " and t == 0:
            output += i
        else:
            t = 1
        
    return output



def on_inline_query(msg):
    query_id, from_id, query_string = telepotpro.glance(msg, flavor='inline_query')
    print ('Inline Query:', query_id, from_id, query_string)

    global maintenance

    if not maintenance:
        for i in range(0, phrase.getLenght() ):
            if(i == 0):
                articles = [InlineQueryResultArticle(
                                id=i,
                                title= phrase.getName(i),
                                description= phrase.getDescription(i),
                                #thumb_url= ,
                                input_message_content=InputTextMessageContent(
                                    message_text= phrase.getContent(i),
                                    parse_mode="HTML"
                                )
                            )]
            else:
                articles += [InlineQueryResultArticle(
                                id=i,
                                title= phrase.getName(i),
                                description= phrase.getDescription(i),
                                #thumb_url= ,
                                input_message_content=InputTextMessageContent(
                                    message_text= phrase.getContent(i),
                                    parse_mode="HTML"
                                )
                            )]
        bot.answerInlineQuery(query_id, articles)

    else:
        articles = [InlineQueryResultArticle(
                        id=0,
                        title= "⚠️ Bot in Manutenzione ⚠️",
                        description= "Ci scusiamo per il disagio",
                        input_message_content=InputTextMessageContent(
                            message_text="⚠️ <b>Bot Attualmente in manutenzione.</b> ⚠️ \n\n <i>Ci scusiamo per il disagio.</i>",
                            parse_mode="HTML"
                        )
                    )]

bot.message_loop({'chat': reply, 'inline_query': on_inline_query})
while True:
    sleep(60)
