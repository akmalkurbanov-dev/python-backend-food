
from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import aiohttp

from keyboards.default import contact_keyboard, location_keyboard
from config import API_URL

router = Router()

class RegisterState(StatesGroup):
    waiting_for_contact = State()
    waiting_for_location = State()

@router.message(F.text == "/start")
async def start_register(message: Message, state: FSMContext):
    await message.answer("Добро пожаловать! Пожалуйста, отправьте свой номер телефона:", reply_markup=contact_keyboard())
    await state.set_state(RegisterState.waiting_for_contact)

@router.message(RegisterState.waiting_for_contact, F.contact)
async def get_contact(message: Message, state: FSMContext):
    await state.update_data(phone=message.contact.phone_number)
    await message.answer("Теперь отправьте свою геолокацию:", reply_markup=location_keyboard())
    await state.set_state(RegisterState.waiting_for_location)


from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

@router.message(RegisterState.waiting_for_location, F.location)
async def get_location(message: Message, state: FSMContext):
    data = await state.get_data()
    payload = {
        "telegram_id": message.from_user.id,
        "username": message.from_user.username or "",
        "full_name": message.from_user.full_name,
        "phone_number": data["phone"],
        "location_lat": message.location.latitude,
        "location_lng": message.location.longitude
    }

    # Инлайн-кнопка на веб-приложение
    webapp_button = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🍽 Открыть меню", url="https://486b8eddc894.ngrok-free.app")]
        ]
    )

    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL, json=payload) as resp:
            if resp.status in [201, 200]:
                await message.answer("✅ Регистрация успешна! Нажмите кнопку ниже, чтобы открыть меню:", reply_markup=webapp_button)
            elif resp.status == 400:
                error = await resp.json()
                if "telegram_id" in error:
                    await message.answer("🔁 Вы уже зарегистрированы. Нажмите кнопку ниже, чтобы открыть меню:", reply_markup=webapp_button)
                else:
                    await message.answer(f"❌ Ошибка регистрации: {error}")
            else:
                await message.answer(f"⚠️ Неизвестная ошибка: {resp.status}")
    await state.clear()


