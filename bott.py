import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from flask import Flask, request

# إعداد السجلات (Logs)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# دمج التوكن والـ Username مباشرة في الكود
TOKEN = "9279252211:AAFO3K3UYYfBb2GgouEzStiVEPcYu8mDzug"
BOT_USERNAME = "Gta2027_bot"

# جلب رابط Render (يجب إضافته في إعدادات Render باسم RENDER_URL)
RENDER_URL = os.getenv("RENDER_URL") 

# إعداد Flask وتطبيق التلغرام
app = Flask(__name__)
tg_app = Application.builder().token(TOKEN).build()

# دالة أمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"أهلاً بك! أنا بوت تلغرام (@{BOT_USERNAME}) أعمل على منصة Render.")

# دالة للرد على الرسائل النصية
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"لقد قلت: {update.message.text}")

# إضافة الأوامر والمستمعين
tg_app.add_handler(CommandHandler("start", start))
tg_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

# مسار استقبال تحديثات الـ Webhook
@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), tg_app.bot)
        tg_app.create_task(tg_app.process_update(update))
        return "OK", 200

@app.route('/')
def index():
    return f"البوت @{BOT_USERNAME} يعمل بنجاح!"

if __name__ == '__main__':
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(tg_app.initialize())
    
    # ربط الـ Webhook تلقائياً عند تشغيل السيرفر إذا كان رابط ريندر موجوداً
    if RENDER_URL:
        loop.run_until_complete(tg_app.bot.set_webhook(url=f"{RENDER_URL}/{TOKEN}"))
        logging.info(f"Webhook set successfully to: {RENDER_URL}/{TOKEN}")
    else:
        logging.warning("RENDER_URL environment variable is missing!")
        
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
