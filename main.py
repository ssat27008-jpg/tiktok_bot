import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
import yt_dlp

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL = "@tik_downloads_eg"

async def is_subscribed(context, user_id):
    try:
        m = await context.bot.get_chat_member(CHANNEL, user_id)
        return m.status in ['member','administrator','creator']
    except:
        return True

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎥 أهلاً بيك!\nابعت رابط التيك توك وهحملهولك بدون علامة مائية\n\n📢 قناتنا: @tik_downloads_eg")

async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not await is_subscribed(context, user_id):
        btn = [[InlineKeyboardButton("✅ اشترك في القناة", url="https://t.me/tik_downloads_eg")],[InlineKeyboardButton("🔄 تأكدت إني اشتركت", callback_data="check_sub")]]
        await update.message.reply_text(f"⚠️ عشان تحمل لازم تشترك الأول في {CHANNEL}", reply_markup=InlineKeyboardMarkup(btn))
        return
    url = update.message.text
    if "tiktok.com" not in url: return
    msg = await update.message.reply_text("⏳ بحمل...")
    try:
        opts = {'format':'mp4','outtmpl':'vid.mp4','quiet':True}
        with yt_dlp.YoutubeDL(opts) as ydl: ydl.download([url])
        await update.message.reply_video(video=open('vid.mp4','rb'), caption="✅ تم - @tik_downloads_eg")
        os.remove('vid.mp4')
        await msg.delete()
    except Exception as e: await msg.edit_text(f"❌ خطأ: {e}")

async def check_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if await is_subscribed(context, query.from_user.id):
        await query.edit_message_text("✅ تمام! ابعت الرابط دلوقتي")
    else:
        await query.answer("❌ لسه مشتركتش!", show_alert=True)

app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(check_button))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))
app.run_polling()
