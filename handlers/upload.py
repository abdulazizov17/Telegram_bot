from telegram import Update
from telegram.ext import CallbackContext
from telegram import ReplyKeyboardMarkup

def button_handler(update: Update, context: CallbackContext):
    text = update.message.text

    if text == "📩 Abdulazizov Asilbek uchun xabar":
        update.message.reply_text("Fayl, rasm yoki video yuboring. Orqaga qaytish uchun  ni bosing.")

    elif text == "📞 Abdulazizov Asilbek bilan bog‘lanish":
        keyboard = [["📸 Instagram", "📱 Telegram"], ["📞 WhatsApp", "🐦 Twitter"], ["🔙 Orqaga"]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        update.message.reply_text("Quyidagi platformalardan birini tanlang:", reply_markup=reply_markup)

    elif text == "🔙 Orqaga":
        from handlers.start import start
        start(update, context)

def file_handler(update: Update, context: CallbackContext):
    update.message.reply_text("Fayl qabul qilindi! Orqaga qaytish uchun  ni bosing.")
