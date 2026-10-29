import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp
TOKEN=os.getenv("BOT_TOKEN")
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ ابعت رابط تيك توك")
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url=update.message.text
    m=await update.message.reply_text("⏳ بحمل...")
    try:
        with yt_dlp.YoutubeDL({'format':'mp4','outtmpl':'video.mp4','quiet':True}) as ydl:
            ydl.download([url])
        await update.message.reply_video(video=open('video.mp4','rb'))
        os.remove('video.mp4')
        await m.delete()
    except Exception as e:
        await m.edit_text(f"خطأ {e}")
app=Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start",start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,handle))
app.run_polling()
