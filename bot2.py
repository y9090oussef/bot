from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters

# معرف الدردشة الخاص بك
YOUR_CHAT_ID = '1389120372'  # استبدل بهذا المعرف
# بيانات التطبيقات
app_links = {
    'app_1': {
        "name": "مهرجانات 2024 بدون نت الذهبي",
        "description": "تطبيق يتيح لك الاستماع إلى مجموعة كبيرة من مهرجانات 2024 بدون الحاجة للاتصال بالإنترنت.",
        "image_url": "https://play-lh.googleusercontent.com/l3bflcGnHY9RnD8DlQQ3pHDEbh29criVgLF1K2o8f3r8eZvqjZ62DOgNgvjo3xlbBjLK=w526-h296-rw",
        "url": "https://play.google.com/store/apps/details?id=com.Golden_2024_Festivals.Mahraganat_2024_Golde&hl=ar"
    },
    'app_2': {
        "name": "تطبيق 2",
        "description": "وصف التطبيق 2.",
        "image_url": "https://link-to-image2.com/image.png",
        "url": "https://link-to-app2.com"
    },
    'app_3': {
        "name": "تطبيق 3",
        "description": "وصف التطبيق 3.",
        "image_url": "https://link-to-image3.com/image.png",
        "url": "https://link-to-app3.com"
    },
    'app_4': {
        "name": "تطبيق 4",
        "description": "وصف التطبيق 4.",
        "image_url": "https://link-to-image4.com/image.png",
        "url": "https://link-to-app4.com"
    },
    'app_5': {
        "name": "تطبيق 5",
        "description": "وصف التطبيق 5.",
        "image_url": "https://link-to-image5.com/image.png",
        "url": "https://link-to-app5.com"
    }
}

# دالة الترحيب عند بدء المحادثة
async def start(update: Update, context):
    user = update.effective_user
    username = user.username if user.username else "بدون اسم مستخدم"
    first_name = user.first_name if user.first_name else "بدون اسم"
    last_name = user.last_name if user.last_name else "بدون لقب"
    
    # جمع بيانات المستخدم
    user_data = f"""
    اسم المستخدم: {username}
    الاسم: {first_name}
    اللقب: {last_name}
    معرف المستخدم: {user.id}
    """
    print(user_data)  # طباعة بيانات المستخدم في وحدة التحكم

    try:
        # إرسال بيانات المستخدم إلى حسابك
        await context.bot.send_message(chat_id=YOUR_CHAT_ID, text=user_data)
        await update.message.reply_text("تم إرسال بياناتك بنجاح إلى المالك!")
    except Exception as e:
        print(f"حدث خطأ أثناء إرسال الرسالة: {e}")
        await update.message.reply_text("حدث خطأ أثناء إرسال البيانات.")
    
    await show_main_menu(update, context)

# عرض القائمة الرئيسية
async def show_main_menu(update: Update, context):
    keyboard = [
        [InlineKeyboardButton("قائمة التطبيقات 📱", callback_data='apps')],
        [InlineKeyboardButton("منصات التواصل الاجتماعي 🌐", callback_data='social_media')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "مرحبًا بك في البوت الاحترافي! اختر أحد الخيارات أدناه 👇",
        reply_markup=reply_markup
    )

# عرض قائمة التطبيقات
async def show_apps(update: Update, context):
    keyboard = [
        [InlineKeyboardButton("مهرجانات 2024 بدون نت الذهبي", callback_data='app_1')],
        [InlineKeyboardButton("تطبيق 2", callback_data='app_2')],
        [InlineKeyboardButton("تطبيق 3", callback_data='app_3')],
        [InlineKeyboardButton("تطبيق 4", callback_data='app_4')],
        [InlineKeyboardButton("تطبيق 5", callback_data='app_5')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    try:
        # تعديل الرسالة إذا كانت هناك رسالة موجودة
        if update.callback_query:
            await update.callback_query.edit_message_text(
                "اختر تطبيقًا لتحميله:",
                reply_markup=reply_markup
            )
        else:
            # إرسال رسالة جديدة إذا لم تكن هناك رسالة لتحريرها
            await update.message.reply_text(
                "اختر تطبيقًا لتحميله:",
                reply_markup=reply_markup
            )
    except Exception as e:
        print(f"Error while showing apps: {e}")

# عرض قائمة منصات التواصل الاجتماعي
async def show_social_media(update: Update, context):
    keyboard = [
        [InlineKeyboardButton("فيسبوك", url='https://facebook.com')],
        [InlineKeyboardButton("تويتر", url='https://twitter.com')],
        [InlineKeyboardButton("إنستغرام", url='https://instagram.com')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.callback_query.edit_message_text(
        "اختر منصة للتواصل الاجتماعي:",
        reply_markup=reply_markup
    )

# معالجة ضغط الأزرار
async def button_handler(update: Update, context):
    query = update.callback_query
    await query.answer()

    if query.data == 'apps':
        await show_apps(update, context)
    elif query.data == 'social_media':
        await show_social_media(update, context)
    elif query.data.startswith('app_'):
        await send_app_details(update, context, query.data)

# دالة إرسال تفاصيل التطبيق
async def send_app_details(update: Update, context, app_id):
    if app_id in app_links:
        app_data = app_links[app_id]
        
        app_name = app_data['name']
        app_description = app_data['description']
        app_image_url = app_data['image_url']
        app_download_url = app_data['url']
        
        # إنشاء زر تحميل وزر عرض جميع التطبيقات
        download_button = InlineKeyboardButton("تحميل الآن 📥", url=app_download_url)
        view_all_apps_button = InlineKeyboardButton("عرض جميع التطبيقات 📋", callback_data='apps')
        keyboard = InlineKeyboardMarkup([[download_button], [view_all_apps_button]])

        # إرسال الصورة مع الوصف والرابط
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=app_image_url,
            caption=f"{app_name}\n{app_description}",
            reply_markup=keyboard,
            parse_mode='Markdown'
        )

# إعداد البوت
if __name__ == '__main__':
    app = ApplicationBuilder().token('8063240957:AAGFh_yRyi-0VPIvD9Mpv-Hr-uByXrqv6B4').build()

    # إضافة معالجات الأوامر
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    print("💡 البوت الاحترافي يعمل الآن...")
    app.run_polling()
