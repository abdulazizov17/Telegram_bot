import json
import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from config import TOKEN, ADMIN_ID
from handlers.contact import contact

async def log_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.chat.id)
    username = update.message.chat.username or ""
    first_name = update.message.chat.first_name or ""
    last_name = update.message.chat.last_name or ""
    full_name = f"{first_name} {last_name}".strip()

    user_identifier = f"@{username}" if username else full_name
    users_file = "data/users.json"

    if not os.path.exists("data"):
        os.makedirs("data")

    try:
        with open(users_file, "r", encoding="utf-8") as file:
            users = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        users = {}

    if user_id not in users:
        users[user_id] = user_identifier
        with open(users_file, "w", encoding="utf-8") as file:
            json.dump(users, file, indent=4, ensure_ascii=False)

        for admin_id in ADMIN_ID:
            await context.bot.send_message(
                chat_id=admin_id,
                text=f"🔔 Yangi foydalanuvchi: {user_identifier} (ID: {user_id}) botga kirdi."
            )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await log_user(update, context)

    keyboard = [
        ["📩 Abdulazizov Asilbek uchun xabar"],
        ["📞 Abdulazizov Asilbek bilan bog‘lanish"],
        ["🤖 Bot haqida ma'lumot"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Assalomu alaykum! Quyidagilardan birini tanlang:", reply_markup=reply_markup)

async def send_game_card(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("📌 send_game_card funksiyasi chaqirildi")

    chat_id = update.message.chat_id
    image_path = "images/dasturchi.jpg"
    caption = """📌 Bot haqida ma'lumot:

🇬🇧 **English:** Hello, dear user! You have entered the personal bot of Abdulazizov A. You can send a message to him or contact him through this bot.

🇺🇿 **O'zbekcha:** Assalomu alaykum! Siz Abdulazizov A ning shaxsiy botiga kirdingiz. Ushbu bot orqali unga xabar yuborishingiz yoki bog‘lanishingiz mumkin."""

    if os.path.exists(image_path):
        with open(image_path, "rb") as photo:
            await context.bot.send_photo(chat_id=chat_id, photo=photo, caption=caption, parse_mode="Markdown")
    else:
        await update.message.reply_text("❌ Rasm topilmadi! Admin bilan bog'laning.")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.message.chat

    if text == "📩 Abdulazizov Asilbek uchun xabar":
        await update.message.reply_text("📩 Xabar yoki savolingizni yozing:")

    elif text == "📞 Abdulazizov Asilbek bilan bog‘lanish":
        await contact(update, context)

    elif text == "🤖 Bot haqida ma'lumot":
        await send_game_card(update, context)

    elif text == "🔙 Orqaga":
        await start(update, context)

    else:
        for admin_id in ADMIN_ID:
            await context.bot.send_message(
                chat_id=admin_id,
                text=f"📩 Yangi xabar: {text}\n👤 {user.first_name} (@{user.username}) - ID: {user.id}"
            )

async def file_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.chat

    if update.message.photo:
        file_id = update.message.photo[-1].file_id
        caption = update.message.caption or "📷 Rasm"
        for admin_id in ADMIN_ID:
            await context.bot.send_photo(chat_id=admin_id, photo=file_id, caption=f"{caption}\n👤 {user.first_name} (@{user.username}) - ID: {user.id}")

    elif update.message.video:
        file_id = update.message.video.file_id
        caption = update.message.caption or "🎥 Video"
        for admin_id in ADMIN_ID:
            await context.bot.send_video(chat_id=admin_id, video=file_id, caption=f"{caption}\n👤 {user.first_name} (@{user.username}) - ID: {user.id}")

    elif update.message.document:
        file_id = update.message.document.file_id
        caption = update.message.caption or "📂 Hujjat"
        for admin_id in ADMIN_ID:
            await context.bot.send_document(chat_id=admin_id, document=file_id, caption=f"{caption}\n👤 {user.first_name} (@{user.username}) - ID: {user.id}")

    elif update.message.audio:
        file_id = update.message.audio.file_id
        caption = update.message.caption or "🎵 Audio"
        for admin_id in ADMIN_ID:
            await context.bot.send_audio(chat_id=admin_id, audio=file_id, caption=f"{caption}\n👤 {user.first_name} (@{user.username}) - ID: {user.id}")

    elif update.message.contact:
        contact = update.message.contact
        for admin_id in ADMIN_ID:
            await context.bot.send_message(
                chat_id=admin_id,
                text=f"📞 Yangi kontakt: {contact.first_name} {contact.last_name or ''}\n☎️ {contact.phone_number}\n👤 ID: {user.id}"
            )

    elif update.message.location:
        location = update.message.location
        for admin_id in ADMIN_ID:
            await context.bot.send_location(chat_id=admin_id, latitude=location.latitude, longitude=location.longitude)
            await context.bot.send_message(chat_id=admin_id, text=f"📍 Manzil jo‘natildi\n👤 {user.first_name} (@{user.username}) - ID: {user.id}")

    elif "http://" in update.message.text or "https://" in update.message.text:
        for admin_id in ADMIN_ID:
            await context.bot.send_message(
                chat_id=admin_id,
                text=f"🔗 Foydalanuvchi havola yubordi:\n{update.message.text}\n👤 {user.first_name} (@{user.username}) - ID: {user.id}"
            )

    await update.message.reply_text("📥 Siz yuborgan narsa qabul qilindi!")

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("game", send_game_card))
    app.add_handler(MessageHandler(filters.TEXT, button_handler))
    app.add_handler(MessageHandler(filters.PHOTO | filters.VIDEO | filters.Document.ALL | filters.AUDIO | filters.CONTACT | filters.LOCATION, file_handler))

    print("🤖 Bot ishga tushdi...")
    app.run_polling()

if __name__ == "__main__":
    main()
