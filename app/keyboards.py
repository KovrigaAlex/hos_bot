from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton,)

from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from app.database.requests import get_income, get_outcome, get_tank_volume
from datetime import datetime

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Информация')],
                                     [KeyboardButton(text='Внесение данных')]],
                           resize_keyboard=True,
                           input_field_placeholder='Выберите пункт меню...')


async def choise():
    keyboard = ReplyKeyboardBuilder()
    keyboard.add(KeyboardButton(text='/Откачка',))
    keyboard.add(KeyboardButton(text='/Приём'))
    keyboard.add(KeyboardButton(text='/На главную'))
    keyboard.adjust(1)
    return keyboard.as_markup(resize_keyboard=True)


def make_date_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()
    today = datetime.now().date()
    daylist = []
    for day_ in range((today.day-1), (today.day+3)):
        daylist.append(datetime.strftime(
            (today.replace(day=day_)), '%d %m %Y'))
    for item in daylist:
        keyboard.add(KeyboardButton(text=item))
    keyboard.adjust(6)
    return keyboard.as_markup(resize_keyboard=True)


def make_hour_keyboard() -> ReplyKeyboardMarkup:
    hourlist = []
    keyboard = ReplyKeyboardBuilder()
    for hour_ in range(0, 25):
        if hour_//10 == 0:
            hour_ = '0'+str(hour_)
        hourlist.append(str(hour_))
    for item in hourlist:
        keyboard.add(KeyboardButton(text=item))
    keyboard.adjust(6)
    return keyboard.as_markup(resize_keyboard=True)


def make_minute_keyboard() -> ReplyKeyboardMarkup:
    minutelist = []
    keyboard = ReplyKeyboardBuilder()
    for minute_ in range(0, 61):
        if minute_//10 == 0:
            minute_ = '0'+str(minute_)
        minutelist.append(str(minute_))
    for item in minutelist:
        keyboard.add(KeyboardButton(text=item))
    keyboard.adjust(6)
    return keyboard.as_markup(resize_keyboard=True)


'''
async def items(category_id):
    all_items = await get_category_item(category_id)
    keyboard = InlineKeyboardBuilder()
    for item in all_items:
        keyboard.add(InlineKeyboardButton(text=item.name, callback_data=f"item_{item.id}"))
    keyboard.add(InlineKeyboardButton(text='На главную', callback_data='to_main'))
    return keyboard.adjust(2).as_markup()
'''
