from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message, ForceReply
from datetime import datetime
import app.database.requests as rq
import app.keyboards as kb
from app.database.requests import set_income
router = Router()
input_dict = {}


class IncomeInput(StatesGroup):
    choosing_date = State()
    choosing_hour = State()
    choosing_minute = State()
    input_concentration = State()


@router.message(StateFilter(None), Command("Откачка"))
async def date_chose(message: Message, state: FSMContext):
    await message.answer(
        text="Выберите дату:",
        reply_markup=kb.make_date_keyboard()
    )
    # Устанавливаем пользователю состояние "выбирает название"
    await state.set_state(IncomeInput.choosing_date)


@router.message(
    IncomeInput.choosing_date
)
async def hour_choose(message: Message, state: FSMContext):
    await state.update_data(chosen_date=message.text.lower())
    await message.answer(
        text="Выбирите час",
        reply_markup=kb.make_hour_keyboard()
    )
    await state.set_state(IncomeInput.choosing_hour)


@router.message(
    IncomeInput.choosing_hour
)
async def minute_choose(message: Message, state: FSMContext):
    await state.update_data(choosing_hour=message.text.lower())
    await message.answer(
        text="Выбирите минуту",
        reply_markup=kb.make_minute_keyboard()
    )
    await state.set_state(IncomeInput.choosing_minute)


@router.message(
    IncomeInput.choosing_minute
)
async def hos_choose(message: Message, state: FSMContext):
    await state.update_data(choosing_minute=message.text.lower())
    await message.answer(
        text="Введите концентрацию ХОС в формате Ч,Ч",
        reply_markup=ForceReply()
    )
    await state.set_state(IncomeInput.input_concentration)


@router.message(
    IncomeInput.input_concentration
)
async def hos_choose(message: Message, state: FSMContext):
    await state.update_data(choosing_hos=message.text.lower())
    user_data = await state.get_data()
    await message.answer(
        text=f"Откачка Лопатино {user_data['chosen_date']} {user_data['choosing_hour']}:"
        f"{user_data['choosing_minute']} ХОС {user_data['choosing_hos']}")
    date = datetime.strptime(user_data['chosen_date'], '%d %m %Y').date()
    time = datetime.strptime(
        user_data['choosing_hour']+':'+user_data['choosing_minute'], '%H:%M').time()
    await set_income(date=date, time=time, concentration=user_data['choosing_hos'])
    await state.clear()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id)
    await message.answer('Добро пожаловать в информационную систему по ситуации с ХОС!',
                         reply_markup=kb.main)


@router.message(F.text == 'Внесение данных')
async def input_choise(message: Message):
    await message.answer('Выберите что будете заность', reply_markup=await kb.choise())


'''



@router.callback_query(F.data.startswith('category_'))
async def category(callback: CallbackQuery):
    await callback.answer('Вы выбрали категорию')
    await callback.message.answer('Выберите товар по категории',
                                  reply_markup=await kb.items(callback.data.split('_')[1]))


@router.callback_query(F.data.startswith('item_'))
async def category(callback: CallbackQuery):
    item_data = await rq.get_item(callback.data.split('_')[1])
    await callback.answer('Вы выбрали товар')
    await callback.message.answer(f'Название: {item_data.name}\nОписание: {item_data.description}\nЦена: {item_data.price}$')
'''
