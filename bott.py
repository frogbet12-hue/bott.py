import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# تفعيل نظام تسجيل الأخطاء (Logging)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# اسم البوت الخاص بك
BOT_USERNAME = "@Gta2027_bot"

# 🎬 قائمة الأفلام والروابط (يمكنك تعديل الأسماء والروابط أو إضافة المزيد هنا)
MOVIES_DATABASE = {
    "فيلم الرسالة": "https://youtube.com🍿_رابط_الفيلم_هنا",
    "فيلم عمر المختار": "https://youtube.com🍿_رابط_الفيلم_هنا",
    "فيلم وثائقي عن الفضاء": "https://youtube.com🍿_رابط_الفيلم_هنا",
    "the matrix": "https://youtube.com🍿_رابط_الفيلم_هنا",
}

# 1. الاستجابة لأمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    first_name = user.first_name
    
    print(f" New User Started Bot -> ID: {user.id} | Name: {first_name}")
    
    # رسالة الترحيب وقائمة الأفلام المتوفرة
    available_movies = "\n".join([f"• {title}" for title in MOVIES_DATABASE.keys()])
    
    await update.message.reply_text(
        f"👋 أهلاً بك في {BOT_USERNAME}، يا {first_name}!\n\n"
        f"🎬 أرسل لي اسم الفيلم الذي تبحث عنه وسأعطيك رابط المشاهدة.\n\n"
        f"🍿 **الأفلام المتوفرة حالياً:**\n{available_movies}"
    )

# 2. التعامل مع بحث المستخدم عن الأفلام
async def handle_movie_search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    movie_name = update.message.text.strip()
    user = update.message.from_user
    
    print(f"🔍 User {user.first_name} searched for: {movie_name}")
    
    # البحث عن الفيلم (تجاهل حالة الأحرف الكبيرة والصغيرة للأفلام الإنجليزية)
    found_movie = None
    for title in MOVIES_DATABASE.keys():
        if movie_name.lower() == title.lower():
            found_movie = title
            break
            
    if found_movie:
        # إذا تم العثور على الفيلم، أرسل الرابط
        movie_link = MOVIES_DATABASE[found_movie]
        response_text = (
            f"🍿 **تم العثور على الفيلم!**\n\n"
            f"🎬 **الاسم:** {found_movie}\n"
            f"🔗 **رابط المشاهدة على يوتيوب:**\n{movie_link}"
        )
    else:
        # إذا لم يتم العثور على الفيلم
        available_movies = "\n".join([f"• {title}" for title in MOVIES_DATABASE.keys()])
        response_text = (
            f"❌ عذراً، فيلم *{movie_name}* غير متوفر حالياً.\n\n"
            f"💡 **الأفلام المتوفرة لدينا هي:**\n{available_movies}"
        )
    
    await update.message.reply_text(response_text, parse_mode="Markdown", disable_web_page_preview=False)

def main():
    # 🚨 ضع التوكن السري الخاص بك من BotFather هنا بين القوسين
    TOKEN="9279252211:AAFO3K3UYYfBb2GgouEzStiVEPcYu8mDzug"
    
    # بناء التطبيق
    application = Application.builder().token(TOKEN).build()

    # تسجيل الأوامر والرسائل
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_movie_search))

    # تشغيل البوت
    print(f"{BOT_USERNAME} is running...")
    application.run_polling()

if __name__ == "__main__":
    main()
