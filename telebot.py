import os

from telegram import ParseMode, Poll, Update, User
from telegram.ext import *
from telegram.utils import helpers
from telegram.error import *

import pandas as pd
import numpy as np
import datetime as datetime

import constants as keys
from modules import automatic_answers as R
from modules import milanuncios_scrap as scrap_m
from modules import idealista_scrap as scrap_i

#
print("Bot started at: "+str(datetime.datetime.now()))

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
    f = open(files_path + "log.txt", "a+")
    f.write(f"{get_user(update)} used the {function} function.\n")
    f.close()

# Commands
def start_command(update, context):
    user = get_user(update)

    msg = f"Buenos días {user}! Soy el bot programado por DheltaHalo para informar " \
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

def idealista_place(update: Update, context: CallbackContext):
    """Sends a predefined poll"""
    questions = ["Los Castros", "Centro - Ayuntamiento", "General Dávila", "Puerto chico", 
                 "El sardinero", "Numancia - San Fernando", "Cuatro Caminos", "Castilla - Hermida",
                 "Alisal - Casoña - San Román", "Valdenoja"]
    message = context.bot.send_poll(
        update.effective_chat.id,
        "¿Qué zona de Santander quieres mirar?",
        questions,
        is_anonymous=False,
        allows_multiple_answers=True,
    )
    # Save some info about the poll the bot_data for later use in receive_poll_answer
    payload = {
        message.poll.id: {
            "questions": questions,
            "message_id": message.message_id,
            "chat_id": update.effective_chat.id,
            "answers": 0,
        }
    }
    context.bot_data.update(payload)

    log(update, "idealista")

def idealista_place_answer(update: Update, context: CallbackContext):
    """Summarize a users poll vote"""
    answer = update.poll_answer
    poll_id = answer.poll_id
    selected_options = answer.option_ids
    answer_string = ""

    try:
        questions = context.bot_data[poll_id]["questions"]

    except KeyError:
        return

    links = scrap_i.cheap()

    for question_id in selected_options:
        text = questions[question_id]
        url = links[question_id]
        answer_string += link_builder(text, url)+"\n"

    msg = f"A continuación aparecen los links a las zonas que quieres ver: \n{answer_string}"

    context.bot.send_message(context.bot_data[poll_id]["chat_id"], msg, parse_mode=ParseMode.MARKDOWN,
                             disable_web_page_preview=True)

func_dict = {"start": start_command, "milanuncios": milanuncios_command, 
             "idealista": idealista_place}

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


def handle_message(update, context):
    text = str(update.message.text).lower()
    response = R.sample_responses(text)

    update.message.reply_text(response)

def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Additional files and folders generation
    global files_path
    files_path = "files/"
    folder = os.path.dirname(files_path)

    if not(os.path.isdir(folder)):
        os.mkdir(folder)

    if not(os.path.isfile(files_path + "anuncios.csv")):
      scrap_m.main()

    f = open(files_path + "log.txt", "a+")
    f.write(f"TELEGRAM BOT LOG. TIME: {datetime.datetime.now()}\n")
    f.close()

    # Bot builder
    updater = Updater(keys.api_key)
    dp = updater.dispatcher

    for i in func_dict:
        dp.add_handler(CommandHandler(i, func_dict[i]))

    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(PollAnswerHandler(idealista_place_answer))
    dp.add_handler(MessageHandler(Filters.text, handle_message))
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()