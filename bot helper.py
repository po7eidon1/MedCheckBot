from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackQueryHandler
from datetime import datetime
import re

# Состояния анкеты
DATE_SURVEY, NAME, GENDER, BIRTHDAY, HYPERTENSION, MEDICATION_HYPERTENSION, ISCHEMIC_HEART_DISEASE, CEREBROVASCULAR_DISEASE, BRONCHIAL_DISEASE, DIABETES, STOMACH_DISEASE,\
    KIDNEY_DISEASE, CANCER, CHOLESTEROL, MEDICATION_CHOLESTEROL, FINISH = range(16)

async def start(update: Update, context):
    # Приветствие
    await update.message.reply_text("Привет! Я помогу вам пройти анкетирование. Для завершения на любом этапе введите команду /stop.")
    return await ask_date_survey(update, context)

async def stop(update: Update, context):
    # Завершаем разговор по команде /stop
    await update.message.reply_text("Анкетирование завершено.")
    return ConversationHandler.END 

async def ask_date_survey(update: Update, context):
    # Спрашиваем дату анкетирования
    await update.message.reply_text("Введите дату анкетирования (день, месяц, год):")
    return DATE_SURVEY

async def handle_date_survey(update: Update, context):
    # Проверка формата даты
    if is_valid_date(update.message.text):
        context.user_data['date_survey'] = update.message.text
        return await ask_name(update, context)
    else:
        await update.message.reply_text("Неверный формат. Пожалуйста, введите дату в формате дд.мм.гггг:")
        return DATE_SURVEY

def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, "%d.%m.%Y")
        return True
    except ValueError:
        return False

async def ask_name(update: Update, context):
    # Спрашиваем ФИО
    await update.message.reply_text("Полное Ф.И.О. пациента:")
    return NAME

async def handle_name(update: Update, context):
    # Проверка на наличие только букв и пробелов
    if re.match(r"^[А-Яа-яA-Za-z\s]+$", update.message.text):
        context.user_data['name'] = update.message.text
        return await ask_gender(update, context)
    else:
        await update.message.reply_text("Имя должно содержать только буквы. Пожалуйста, введите Ф.И.О. снова:")
        return NAME

async def ask_gender(update: Update, context):
    # Спрашиваем пол пациента
    await update.message.reply_text("Введите ваш пол (м - мужской, ж - женский):")
    return GENDER

async def handle_gender(update: Update, context):
    # Проверка ввода на "м" или "ж"
    if update.message.text.lower() in ['м', 'ж']:
        context.user_data['gender'] = update.message.text.lower()
        return await ask_birthday(update, context)
    else:
        await update.message.reply_text("Пожалуйста, введите только 'м' или 'ж' для пола:")
        return GENDER

async def ask_birthday(update: Update, context):
    # Спрашиваем дату рождения
    await update.message.reply_text("Введите вашу дату рождения в формате дд.мм.гггг:")
    return BIRTHDAY

async def handle_birthday(update: Update, context):
    # Проверка формата даты
    if is_valid_date(update.message.text):
        context.user_data['birthday'] = update.message.text
        return await ask_hypertension(update, context)
    else:
        await update.message.reply_text("Неверный формат. Пожалуйста, введите дату в формате дд.мм.гггг:")
        return BIRTHDAY

async def ask_hypertension(update: Update, context):
    # Вопрос о гипертонической болезни
    keyboard = [
        [InlineKeyboardButton("Да", callback_data="yes"), InlineKeyboardButton("Нет", callback_data="no")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("У вас есть гипертоническая болезнь (повышенное артериальное давление)?", reply_markup=reply_markup)
    return HYPERTENSION

async def handle_hypertension(update: Update, context):
    query = update.callback_query
    await query.answer()
    context.user_data['hypertension'] = "Да" if query.data == "yes" else "Нет"
    return await ask_medication_hypertension(query, context)

async def ask_medication_hypertension(query, context):
    # Запрашиваем, принимаются ли препараты для снижения давления
    keyboard = [
        [InlineKeyboardButton("Да", callback_data="yes"), InlineKeyboardButton("Нет", callback_data="no")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text("Если «Да», то принимаете ли Вы препараты для снижения давления?", reply_markup=reply_markup)
    return MEDICATION_HYPERTENSION

async def handle_medication_hypertension(update: Update, context):
    query = update.callback_query
    await query.answer()
    context.user_data['medication_hypertension'] = "Да" if query.data == "yes" else "Нет"
    return await ask_ischemic_heart_disease(query, context)

async def ask_ischemic_heart_disease(query, context):
    # Вопрос о ишемической болезни сердца
    keyboard = [
        [InlineKeyboardButton("Да", callback_data="yes"), InlineKeyboardButton("Нет", callback_data="no")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text("У вас есть ишемическая болезнь сердца?", reply_markup=reply_markup)
    return ISCHEMIC_HEART_DISEASE

async def handle_ischemic_heart_disease(update: Update, context):
    query = update.callback_query
    await query.answer()
    context.user_data['ischemic_heart_disease'] = "Да" if query.data == "yes" else "Нет"
    return await ask_cerebrovascular_disease(query, context)

async def ask_cerebrovascular_disease(query, context):
    # Вопрос о сосудистых заболеваниях мозга
    keyboard = [
        [InlineKeyboardButton("Да", callback_data="yes"), InlineKeyboardButton("Нет", callback_data="no")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text("У вас есть сосудистые заболевания мозга?", reply_markup=reply_markup)
    return CEREBROVASCULAR_DISEASE

async def handle_cerebrovascular_disease(update: Update, context):
    query = update.callback_query
    await query.answer()
    context.user_data['cerebrovascular_disease'] = "Да" if query.data == "yes" else "Нет"
    return await ask_bronchial_disease(query, context)

async def ask_bronchial_disease(query, context):
    # Вопрос о бронхиальной болезни
    keyboard = [
        [InlineKeyboardButton("Да", callback_data="yes"), InlineKeyboardButton("Нет", callback_data="no")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text("У вас есть бронхиальная болезнь?", reply_markup=reply_markup)
    return BRONCHIAL_DISEASE

async def handle_bronchial_disease(update: Update, context):
    query = update.callback_query
    await query.answer()
    context.user_data['bronchial_disease'] = "Да" if query.data == "yes" else "Нет"
    return await ask_diabetes(query, context)

async def ask_diabetes(query, context):
    # Вопрос о диабете
    keyboard = [
        [InlineKeyboardButton("Да", callback_data="yes"), InlineKeyboardButton("Нет", callback_data="no")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text("У вас есть диабет?", reply_markup=reply_markup)
    return DIABETES

async def handle_diabetes(update: Update, context):
    query = update.callback_query
    await query.answer()
    context.user_data['diabetes'] = "Да" if query.data == "yes" else "Нет"
    return await ask_stomach_disease(query, context)

async def ask_stomach_disease(query, context):
    # Вопрос о заболеваниях желудка
    keyboard = [
        [InlineKeyboardButton("Да", callback_data="yes"), InlineKeyboardButton("Нет", callback_data="no")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text("У вас есть заболевания желудка?", reply_markup=reply_markup)
    return STOMACH_DISEASE

async def handle_stomach_disease(update: Update, context):
    query = update.callback_query
    await query.answer()
    context.user_data['stomach_disease'] = "Да" if query.data == "yes" else "Нет"
    return await ask_kidney_disease(query, context)

async def ask_kidney_disease(query, context):
    # Вопрос о заболеваниях почек
    keyboard = [
        [InlineKeyboardButton("Да", callback_data="yes"), InlineKeyboardButton("Нет", callback_data="no")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text("У вас есть заболевания почек?", reply_markup=reply_markup)
    return KIDNEY_DISEASE

async def handle_kidney_disease(update: Update, context):
    query = update.callback_query
    await query.answer()
    context.user_data['kidney_disease'] = "Да" if query.data == "yes" else "Нет"
    return await ask_cancer(query, context)

async def ask_cancer(query, context):
    # Вопрос о раке
    keyboard = [
        [InlineKeyboardButton("Да", callback_data="yes"), InlineKeyboardButton("Нет", callback_data="no")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text("У вас есть рак?", reply_markup=reply_markup)
    return CANCER

async def handle_cancer(update: Update, context):
    query = update.callback_query
    await query.answer()
    context.user_data['cancer'] = "Да" if query.data == "yes" else "Нет"
    return await ask_cholesterol(query, context)

async def ask_cholesterol(query, context):
    # Вопрос о холестерине
    keyboard = [
        [InlineKeyboardButton("Да", callback_data="yes"), InlineKeyboardButton("Нет", callback_data="no")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text("У вас повышенный уровень холестерина?", reply_markup=reply_markup)
    return CHOLESTEROL

async def handle_cholesterol(update: Update, context):
    query = update.callback_query
    await query.answer()
    context.user_data['cholesterol'] = "Да" if query.data == "yes" else "Нет"
    return await ask_medication_cholesterol(query, context)

async def ask_medication_cholesterol(query, context):
    # Вопрос о приеме препаратов от холестерина
    keyboard = [
        [InlineKeyboardButton("Да", callback_data="yes"), InlineKeyboardButton("Нет", callback_data="no")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text("Принимаете ли вы препараты для снижения холестерина?", reply_markup=reply_markup)
    return MEDICATION_CHOLESTEROL

async def handle_medication_cholesterol(update: Update, context):
    query = update.callback_query
    await query.answer()
    context.user_data['medication_cholesterol'] = "Да" if query.data == "yes" else "Нет"
    return await finish(query, context)

async def finish(query, context):
    # Вывод результатов анкетирования
    result = f"""   Анкета успешно завершена! Вот ваши данные:

    Дата анкетирования: {context.user_data.get('date_survey')}
    Имя: {context.user_data.get('name')}
    Пол: {context.user_data.get('gender')}
    Дата рождения: {context.user_data.get('birthday')}
    Гипертоническая болезнь: {context.user_data.get('hypertension')}
    Прием препаратов для снижения давления: {context.user_data.get('medication_hypertension')}
    Ишемическая болезнь сердца: {context.user_data.get('ischemic_heart_disease')}
    Цереброваскулярное заболевание: {context.user_data.get('cerebrovascular_disease')}
    Хроническое заболевание бронхов или легких: {context.user_data.get('bronchial_disease')}
    Сахарный диабет: {context.user_data.get('diabetes')}
    Заболевания желудка: {context.user_data.get('stomach_disease')}
    Хроническое заболевание почек: {context.user_data.get('kidney_disease')}
    Злокачественное новообразование: {context.user_data.get('cancer')}
    Повышенный уровень холестерина: {context.user_data.get('cholesterol')}
    Прием препаратов для снижения холестерина: {context.user_data.get('medication_cholesterol')}"""

    await query.message.reply_text(result)
    return ConversationHandler.END

# Основная функция запуска бота
def main():
    application = Application.builder().token("7993727733:AAFUp-mdBbS7S3gazpqoGS5T6BLS3rtOu0w").build()

    # Команды
    start_handler = CommandHandler("start", start)
    stop_handler = CommandHandler("stop", stop)

    # Обработчики состояний анкеты
    conversation_handler = ConversationHandler(
        entry_points=[start_handler],
        states={
            DATE_SURVEY: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_date_survey)],
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_name)],
            GENDER: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_gender)],
            BIRTHDAY: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_birthday)],
            HYPERTENSION: [CallbackQueryHandler(handle_hypertension)],
            MEDICATION_HYPERTENSION: [CallbackQueryHandler(handle_medication_hypertension)],
            ISCHEMIC_HEART_DISEASE: [CallbackQueryHandler(handle_ischemic_heart_disease)],
            CEREBROVASCULAR_DISEASE: [CallbackQueryHandler(handle_cerebrovascular_disease)],
            BRONCHIAL_DISEASE: [CallbackQueryHandler(handle_bronchial_disease)],
            DIABETES: [CallbackQueryHandler(handle_diabetes)],
            STOMACH_DISEASE: [CallbackQueryHandler(handle_stomach_disease)],
            KIDNEY_DISEASE: [CallbackQueryHandler(handle_kidney_disease)],
            CANCER: [CallbackQueryHandler(handle_cancer)],
            CHOLESTEROL: [CallbackQueryHandler(handle_cholesterol)],
            MEDICATION_CHOLESTEROL: [CallbackQueryHandler(handle_medication_cholesterol)],
        },
        fallbacks=[stop_handler],
    )

    # Добавляем обработчики в приложение
    application.add_handler(conversation_handler)
    application.add_handler(stop_handler)

    # Запускаем бота
    application.run_polling()

if __name__ == '__main__':
    main()
