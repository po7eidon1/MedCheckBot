import asyncio
import logging
import sys
from os import getenv
from typing import Any, Dict

from aiogram import Bot, Dispatcher, F, Router, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import (
    KeyboardButton,
    Message,
    CallbackQuery,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

TOKEN = '7993727733:AAFUp-mdBbS7S3gazpqoGS5T6BLS3rtOu0w'#getenv("BOT_TOKEN")

form_router = Router()

#Дефолтная анкета
def def_anketa():
    return {'HYPERTENSION':'У вас есть гипертоническая болезнь (повышенное артериальное давление)?',
            'MEDICATION_HYPERTENSION':'Если «Да», то принимаете ли Вы препараты для снижения давления?',
            'ISCHEMIC_HEART_DISEASE':'У вас есть ишемическая болезнь сердца?',
            'DONE':'Завершить анкету?'}

#Дефолтные ответы ✅❌
def def_anss(anketa):
    anss = {}
    for key in anketa:
        anss[key] = '❌'
    return anss

class Form(StatesGroup):
    name = State()
    like_bots = State()
    language = State()
    anketa = State()
    # Create variables from the dictionary keys
    # for key in def_anketa():
    #     globals()[key] = State()

@form_router.message(CommandStart())
async def command_start(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.name)
    await message.answer(
        "Hi there! What's your name?",
        reply_markup=ReplyKeyboardRemove(),
    )

@form_router.message(Command("cancel"))
@form_router.message(F.text.casefold() == "cancel")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info("Cancelling state %r", current_state)
    await state.clear()
    await message.answer(
        "Cancelled.",
        reply_markup=ReplyKeyboardRemove(),
    )

def create_anketa(anketa, anss):
    builder = InlineKeyboardBuilder()
    for key in anss:
        builder.row(
            InlineKeyboardButton(
                text='Нет'+anss[key]+' '+anketa[key],
                callback_data=key
            )
        )
    builder.adjust(1)
    return builder.as_markup()
    # markup = []
    # for key in anss:
    #     markup+=[[InlineKeyboardButton(text=anketa[key]+' '+anss[key]+'Нет', callback_data=key, resize_keyboard=True)]]
    # return InlineKeyboardMarkup(inline_keyboard=markup, resize_keyboard=True)

@form_router.message(Form.name)
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await state.set_state(Form.anketa)
    anketa = def_anketa()
    answers = def_anss(anketa)
    await state.update_data(anketa=anketa)
    await state.update_data(answers=answers)
    await message.answer(
        f"Привет, {html.quote(message.text)}!\nЗаполни анкету:",
        reply_markup=create_anketa(anketa, answers),
    )

# Обработчик нажатий на кнопки
@form_router.callback_query(lambda call: True)
async def callback_inline(call: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    if 'anketa' in data and 'answers' in data:
        anketa = data['anketa']
        answers = data['answers']
    else:
        return
    for key in answers:
        if call.data == 'DONE':
            answers[call.data] = '✅' if answers[key] == '❌' else '❌'
            result = f"Привет, {html.quote(data['name'])}!\nРезультаты анкеты:\n<pre>"
            for key in answers:
                if key != 'DONE':
                    result+='\n'+anketa[key]+' '+answers[key]
            result+='</pre>'
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text=result, reply_markup=None)
            await call.message.answer(
                f"Nice to meet you, {html.quote(data['name'])}!\nDid you like to write bots?",
                reply_markup=ReplyKeyboardMarkup(
                    keyboard=[
                        [
                            KeyboardButton(text="Yes"),
                            KeyboardButton(text="No"),
                        ]
                    ],
                    resize_keyboard=True,
                ),
            )
            await state.set_state(Form.like_bots)
        elif call.data == key:
            answers[call.data] = '✅' if answers[key] == '❌' else '❌'
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"Привет, {html.quote(data['name'])}!\nЗаполни анкету:", reply_markup=create_anketa(anketa, answers))

@form_router.message(Form.like_bots, F.text.casefold() == "no")
async def process_dont_like_write_bots(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    await state.clear()
    await message.answer(
        "Not bad not terrible.\nSee you soon.",
        reply_markup=ReplyKeyboardRemove(),
    )
    await show_summary(message=message, data=data, positive=False)


@form_router.message(Form.like_bots, F.text.casefold() == "yes")
async def process_like_write_bots(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.language)

    await message.reply(
        "Cool! I'm too!\nWhat programming language did you use for it?",
        reply_markup=ReplyKeyboardRemove(),
    )

@form_router.message(Form.like_bots)
async def process_unknown_write_bots(message: Message) -> None:
    await message.reply("I don't understand you :(")


@form_router.message(Form.language)
async def process_language(message: Message, state: FSMContext) -> None:
    data = await state.update_data(language=message.text)
    await state.clear()

    if message.text.casefold() == "python":
        await message.reply(
            "Python, you say? That's the language that makes my circuits light up! 😉"
        )

    await show_summary(message=message, data=data)


async def show_summary(message: Message, data: Dict[str, Any], positive: bool = True) -> None:
    name = data["name"]
    language = data.get("language", "<something unexpected>")
    text = f"I'll keep in mind that, {html.quote(name)}, "
    text += (
        f"you like to write bots with {html.quote(language)}."
        if positive
        else "you don't like to write bots, so sad..."
    )
    await message.answer(text=text, reply_markup=ReplyKeyboardRemove())


async def main():


    dp = Dispatcher()

    dp.include_router(form_router)

    # Start event dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    asyncio.run(main())