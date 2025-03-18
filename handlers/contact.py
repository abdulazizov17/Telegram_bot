from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from config import ADMIN_ID

async def contact(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("📱 Telegram", url="https://t.me/Abdulazizov_170")],
        [InlineKeyboardButton("📸 Instagram", url="https://www.instagram.com/abdulazizov______a/")],
        [InlineKeyboardButton("📞 WhatsApp", url="https://wa.me/998932420211")],
        [InlineKeyboardButton("🐦 Twitter", url="https://twitter.com/AbdulazizovA7")],
        [InlineKeyboardButton("🐙 Git hub", url="https://github.com/abdulazizov17/")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        await update.message.reply_text("📩 Abdulazizov Asilbek bilan bog‘lanish uchun o'zingizga qulay app orqali aloqaga chiqing:", reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.message.reply_text("📩 Abdulazizov Asilbek bilan bog‘lanish:", reply_markup=reply_markup)

    user = update.effective_user
    user_info = f"👤 {user.first_name} {user.last_name or ''} (@{user.username}) - ID: {user.id}"

    try:
        await context.bot.send_message(chat_id=ADMIN_ID, text=f"🔔 Foydalanuvchi start tugmasini  bosib botga kirdi:\n{user_info}")
    except Exception as e:
        print(f"Admin xabar yuborishda xatolik: {e}")
