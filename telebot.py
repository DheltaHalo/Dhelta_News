import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from telegram import ParseMode, Poll, Update, User
from telegram.ext import *
from telegram.utils import helpers
from telegram.error import *

import pandas as pd
import numpy as np
from datetime import datetime

from settings import *
from modules import file_builder as f_build
from modules import milanuncios_scrap as scrap_m

# Misc functions
def link_builder(text: str, url: str):
    return "["+f"{text}"+"]("+f"{url}"+")"

def get_user(update):
    first_name = update.message.chat.first_name
    last_name = update.message.chat.last_name
    user = update.message.chat.username

    if user == None:
        user = first_name + " " + last_name
    
    return user

def log(update, function: str):
    f = open(files_path + log_name, "a+")
    f.write(f"User \"\" used {function} ({str(datetime.now())})\n")
    f.close()

# Commands
def start_command(update, context):
    #user = get_user(update)

    msg = f"Buenos días! Soy el bot programado por DheltaHalo para informar " \
          "de novedades en varios ámbitos de internet.\n" \
          "\nPara ver los comandos disponibles escribe /help."

    update.message.reply_text(msg)
    
    log(update, "start")

def milanuncios_command(update, context):
    bot = context.bot
    milanuncios = scrap_m.decode()

    for k in range(len(milanuncios)):
        url = milanuncios["urls"][k]
        text = milanuncios["titulares"][k]

        msg =link_builder(text, url)
        update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
    
    log(update, "milanuncios")

func_dict = {"start": start_command, "milanuncios": milanuncios_command}

# Help and error/message handling
def help_command(update, context):
    txt = "Los comandos disponibles son: \n"
    for k in func_dict:
        txt += "/"+k+"\n"

    update.message.reply_text(txt)
    log(update, "help")

def error(update, context):
    try:
        raise context.error
    except (Unauthorized, BadRequest, TimedOut, NetworkError, TelegramError):
        print(1)

def main():
    print("Bot started at: "+str(datetime.now()))
    
    # Build files
    f_build.main()

    # Bot builder
    updater = Updater(api_key)
    dp = updater.dispatcher

    for i in func_dict:
        dp.add_handler(CommandHandler(i, func_dict[i]))

    dp.add_handler(CommandHandler("help", help_command))
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()