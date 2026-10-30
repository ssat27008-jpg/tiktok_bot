import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import yt_dlp

TOKEN=os.getenv("BOT_TOKEN")

async def start(update: Update, context):
    await update.message.reply_text("أهلاً 👋 ابعت رابط تيك توك وأنا أحمله بدون علامة مائية")

async def handle(update: Update, context):
    url=update.message.text
    if "tiktok.com" not in url:
        return await update.message.reply_text("ابعت رابط تيك توك بس 🔗")
    m=await update.message.reply_text("⏳ بحمّل...")
    try:
        with yt_dlp.YoutubeDL({'format':'mp4','outtmpl':'video.mp4','quiet':True}) as ydl:
            ydl.download([url])
        await update.message.reply_video(video=open('video.mp4','rb'), caption="✅ بدون علامة مائية - @tik_tokers_eg_bot")
        os.remove('video.mp4')
        await m.delete()
    except Exception as e:
        await update.message.reply_text(f"مش عارف أحمله: {e}")

app=Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
app.run_polling()
