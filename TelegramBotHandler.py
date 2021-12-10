from aiogram import Bot, types, Dispatcher
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor

from Database import Database
from StateMachine import StateMachine

dMachine = StateMachine()
bot = Bot('5016454045:AAHwLAPdAiWnsjfI09-0rWHSl8iYVDyIpXs')
dp = Dispatcher(bot)
db = Database()

kb_pizza = ReplyKeyboardMarkup(resize_keyboard=True)
kb_pizza.add(KeyboardButton('Большую'))
kb_pizza.add(KeyboardButton('Маленькую'))

kb_payment = ReplyKeyboardMarkup(resize_keyboard=True)
kb_payment.add(KeyboardButton('Наличкой'))
kb_payment.add(KeyboardButton('Картой'))

kb_confirm = ReplyKeyboardMarkup(resize_keyboard=True)
kb_confirm.add(KeyboardButton('Да'))
kb_confirm.add(KeyboardButton('Нет'))

kb_again = ReplyKeyboardMarkup(resize_keyboard=True)
kb_again.add(KeyboardButton('Сделать новый заказ'))


# kb_pizza = Keyboa(items=pizza_size_keyboard, copy_text_to_callback=True)
# kb_payment = Keyboa(items=payment_method_keyboard, copy_text_to_callback=True)

@dp.message_handler(content_types=['text'])
async def get_text_messages(message: types.Message):
    print(message.from_user.id)
    # if str(message.from_user.id) == "103953122":
    #    return
    person_id = message.from_user.id
    if not (db.has_user(person_id)):
        db.add_user(person_id, dMachine.default_state)
    else:
        dMachine.state = db.get_state(person_id)
        dMachine.pizza_size = db.get_pizza_size(person_id)
        dMachine.payment_method = db.get_payment_method(person_id)

    if message.text == 'Большую' or message.text == 'Маленькую':
        dMachine.accept_size()
        dMachine.pizza_size = message.text
        db.update_info(person_id, dMachine.state, dMachine.pizza_size, dMachine.payment_method)
    if message.text == 'Наличкой' or message.text == 'Картой':
        dMachine.accept_pay_method()
        dMachine.payment_method = message.text
        db.update_info(person_id, dMachine.state, dMachine.pizza_size, dMachine.payment_method)
    if message.text == 'Да':
        dMachine.confirm_order()
        db.update_info(person_id, dMachine.state, dMachine.pizza_size, dMachine.payment_method)
        await bot.send_message(chat_id=person_id, reply_markup=kb_again, text="Спасибо за заказ")
    if message.text == 'Нет' or message.text == 'Сделать новый заказ':
        dMachine.start_again()
        db.update_info(person_id, dMachine.state, dMachine.pizza_size, dMachine.payment_method)
        await bot.send_message(chat_id=person_id, reply_markup=kb_again, text="Давайте начнем заново")
    if dMachine.state == 'ready for start':
        await bot.send_message(chat_id=person_id, reply_markup=kb_pizza,
                               text="Какую вы хотите пиццу? Большую или маленькую?")
    elif dMachine.state == 'know size':
        await bot.send_message(chat_id=person_id, reply_markup=kb_payment,
                               text="Как вы будете платить?")
    elif dMachine.state == 'know payment method':
        await bot.send_message(chat_id=person_id, reply_markup=kb_confirm,
                               text="Вы хотите {} пиццу, оплата - {}?"
                               .format(dMachine.pizza_size.lower(), dMachine.payment_method.lower()))


def start():
    executor.start_polling(dp)


def message_processing(message):
    pass
    # if(dMachine.state == 'ready for start'):
    # if(dMachine.state == 'waiting for size'):
    # if(dMachine.state == 'waiting for payment method'):
    # if(dMachine.state == 'waiting for confirmation'):
    # if(dMachine.state == 'confirm order'):
