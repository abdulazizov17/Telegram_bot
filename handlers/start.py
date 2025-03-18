from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext
import json


def log_user(update: Update):
    user_id = update.message.chat.id
    first_name = update.message.chat.first_name
    last_name = update.message.chat.last_name or ""

    try:
        with open("data/users.json", "r") as file:
            users = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        users = {}

    users[str(user_id)] = f"{first_name} {last_name}"

    with open("data/users.json", "w") as file:
        json.dump(users, file, indent=4)


def start(update: Update, context: CallbackContext):
    log_user(update)

    keyboard = [["📩 Abdulazizov Asilbek uchun xabar"], ["📞 Abdulazizov Asilbek bilan bog‘lanish"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    update.message.reply_text("Assalomu aleykum Siz Abdulazizov Asilbek Botiga tashrif buyurdingiz Quyidagilardan birini tanlang:", reply_markup=reply_markup)
