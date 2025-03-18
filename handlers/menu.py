from telegram import Update
from telegram.ext import CallbackContext

def help(update: Update, context: CallbackContext):
    update.message.reply_text("❓ Yordam kerak bo'lsa, admin bilan bog'laning.\n\n"
                              "📩 Xabar jo‘natish: Abdulazizov Asilbek uchun xabar\n"
                              "📞 Aloqa: Abdulazizov Asilbek bilan bog‘lanish\n"
                              "🔄 /start - Botni qayta ishga tushirish")
