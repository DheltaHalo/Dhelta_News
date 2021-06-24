import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from telegram import ParseMode, Poll, Update
from telegram.ext import *
from telegram.utils import helpers

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

# Commands
def start_command(update, context):
    msg = "Buenos días! Soy el bot programado por DheltaHalo para informar " \
          "de novedades en varios ámbitos de internet.\n" \
          "\nPara ver los comandos disponibles escribe /help."

    update.message.reply_text(msg)

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

def error(update, context):
    print("Error")

def handle_message(update, context):
    text = str(update.message.text).lower()
    response = R.sample_responses(text)

    update.message.reply_text(response)

def main():
    if not(os.path.isfile("files/anuncios.csv")):
      scrap_m.main()

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