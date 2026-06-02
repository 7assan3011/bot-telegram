import os
import telebot
from yt_dlp import YoutubeDL

# حط هنا التوكن بتاعك اللي أخدته من BotFather
BOT_TOKEN = '8946043898:AAFgp4JcLXvrzCsMR0tsCanNwB_JcPSKqTg'
bot = telebot.TeleBot(BOT_TOKEN)

# 1. رسالة الترحيب وعرض المميزات لما المستخدم يدوس /start
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "👑 أهلاً بك في بوت التحميل السريع!\n\n"
        "🚀 **مميزات البوت:**\n"
        "• بيحمل من أي منصة (يوتيوب، إنستغرام، تيك توك، فيسبوك، إكس... إلخ).\n"
        "• بيجيبلك الفيديو بأعلى جودة ممكنة.\n"
        "• شغال وسريع على مدار الـ 24 ساعة.\n\n"
        "📥 **طريقة الاستخدام:**\n"
        "كل اللي عليك تعمله، ابعت لينك الفيديو وسيب البوت يتعامل!"
    )
    bot.reply_to(message, welcome_text, parse_mode='Markdown')

# 2. استقبال اللينكات والتعامل معاها
@bot.message_handler(func=lambda message: True)
def handle_links(message):
    url = message.text
    
    # التأكد إن المستخدم بعت لينك فعلاً مش أي كلام
    if not url.startswith(("http://", "https://")):
        bot.reply_to(message, "⚠️ يرجى إرسال رابط فيديو صحيح يبدأ بـ http أو https.")
        return

    # رسالة للمستخدم عشان يعرف إن البوت شغال
    status_msg = bot.reply_to(message, "⏳ جاري معالجة الرابط وتحميل الفيديو، انتظر ثواني...")

    # تعديل الإعدادات هنا عشان يشوف ملف الكوكيز اللي عملناه
    ydl_opts = {
        'format': 'best',  # بيجيب أفضل جودة مدمج فيها الصوت والفيديو
        'outtmpl': 'downloaded_video.%(ext)s',  # اسم الملف الناتج
        'quiet': True,
        'cookiefile': 'instagram_cookies.txt',  # <--- السطر الجديد هنا يا معلم ✨
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            # استخراج معلومات الفيديو وتحميله
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
        
        # تحديث الحالة للمستخدم
        bot.edit_message_text("📤 جاري رفع الفيديو للتليجرام...", chat_id=message.chat.id, message_id=status_msg.message_id)

        # إرسال الفيديو للمستخدم
        with open(filename, 'rb') as video:
            bot.send_video(message.chat.id, video, reply_to_message_id=message.id)

        # حذف الفيديو من السيرفر بعد ما اتبعث عشان ما يملأش المساحة
        os.remove(filename)
        bot.delete_message(chat_id=message.chat.id, message_id=status_msg.message_id)

    except Exception as e:
        print(f"Error: {e}")
        bot.edit_message_text("❌ عذراً، حدث خطأ أثناء تحميل الفيديو. تأكد من أن الرابط مدعوم أو جرب لاحقاً.", chat_id=message.chat.id, message_id=status_msg.message_id)
        # لتجنب بقاء ملفات معطوبة
        if 'filename' in locals() and os.path.exists(filename):
            os.remove(filename)

# تشغيل البوت بشكل مستمر
print("🚀 The fast download bot is now working! Enjoy fast downloads from any platform! 👑")
bot.infinity_polling()