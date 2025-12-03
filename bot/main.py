import re
import telebot
import asyncio
import fortune
import json
import random
import logging
import sys

#from os import getenv
#from antiswear import *  ---------- no need
from datetime import datetime, timezone
from difflib import SequenceMatcher
from telebot.async_telebot import AsyncTeleBot

TOKEN = str()

try:
    with open("config/token.txt", "r", encoding="utf-8") as f:
        TOKEN = str(f.read().strip())
except (FileNotFoundError):
    print("Hey there! There is no config/token.txt file!")
    sys.exit(1)

doas = AsyncTeleBot(TOKEN)

# Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Saving time at the moment of bot start
start_time = datetime.now(timezone.utc)

# Modules
import ml
ml.doas = doas; ml.register()

import info
info.doas = doas; info.start_time = start_time; info.register()

#import not_used
#not_used.doas = doas; not_used.register()

# User verification function for administrator rights
async def is_user_admin(chat_id, user_id):
    admin_statuses = ["creator", "administrator"]
    if str(user_id) == "YOUR_ID": # God mode
        return 1
    result = await doas.get_chat_member(chat_id, user_id)
    if result.status in admin_statuses:
        return 1
    return 0

# Function for searching and removing swear words from users in the monitoring list
@doas.message_handler(func=lambda message: True)
async def checking_messages(message):
    text = message.text
    user_id = str(message.from_user.id)
    text_cleaning = re.split(r'[,.\n? ]+', text)
    user_name = message.from_user.username

    # Handling errors and searching/removing swear words from users from the monitoring list
    try:
        # Reading files with a list of users
        with open("config/users.txt", "r") as user_content:
            users_check = user_content.read().split()

        logging.info(f"Message checking: ID = {user_id}, Username = @{user_name}")  # Debugging to the console
        
        # !!! NO NEED !!!
        # Searching for a user in the list of users to monitoring
        #if user_id in users_check:
        #    # Searching for swear words in user's text
        #    for word in text_cleaning:
        #        if check(word):
        #            logging.info(f"Message removed, word '{word}', message {text_cleaning}")   # Debugging to the console
        #            await doas.delete_message(message.chat.id, message.id)
        #            return
    # Sending an error message that files were not found
    except FileNotFoundError as e:
        logging.info(f"File not found: {str(e)}")
    # Sending an error message
    except Exception as e:
        logging.info(f"An error occurred while checking messages: {str(e)}")



# Running a bot
if __name__ == '__main__':
    print("doas!bot is turned on!")
    asyncio.run(doas.polling())
