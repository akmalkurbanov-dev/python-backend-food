
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def contact_keyboard():
    kb = [[KeyboardButton(text="📱 Отправить номер", request_contact=True)]]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

def location_keyboard():
    kb = [[KeyboardButton(text="📍 Отправить локацию", request_location=True)]]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
