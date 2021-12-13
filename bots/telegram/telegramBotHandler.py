from aiogram import Bot, types, Dispatcher
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor

from Database import Database
from StateMachine import StateMachine
from utils import TELEGRAM_TOKEN

dMachine = StateMachine()
bot = Bot(TELEGRAM_TOKEN)
banlist = ['10395312 2']
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
    await handle_messages(message.from_user.id, message.text)


async def handle_messages(user_id, text):
    if str(user_id) in banlist:
        return
    if not (db.has_user(user_id)):
        db.add_user(user_id, dMachine.default_state)
    else:
        dMachine.state = db.get_state(user_id)
        dMachine.pizza_size = db.get_pizza_size(user_id)
        dMachine.payment_method = db.get_payment_method(user_id)
    print("telegram. id=" + str(user_id) + " used bot. input: " + text + ". Current state=" + dMachine.state)
    reply, kb_format, state = handle_message(text, dMachine.state)
    if kb_format is None:
        await send_message(text=reply, chat_id=user_id)
    else:
        await send_message(text=reply, chat_id=user_id, reply_markup=kb_format)
    db.update_info(person_id=user_id, newState=state,
                   pizza_size=dMachine.pizza_size, payment_method=dMachine.payment_method)


async def send_message(text, chat_id, reply_markup=None):
    await bot.send_message(chat_id=chat_id, reply_markup=reply_markup,
                           text=text)


def handle_message(text: str, state=None):
    reply = None
    kb_format = None

    if (text == 'Большую' or text == 'Маленькую') and state == 'ready for start':
        dMachine.accept_size()
        kb_format = kb_payment

        dMachine.pizza_size = text

        state = dMachine.state
        reply = 'Как вы будете платить?'

    elif (text == 'Наличкой' or text == 'Картой') and state == 'know size':
        dMachine.accept_pay_method()
        kb_format = kb_confirm

        dMachine.payment_method = text

        state = dMachine.state
        reply = "Вы хотите {} пиццу, оплата - {}?".format(dMachine.pizza_size.lower(), dMachine.payment_method.lower())

    elif text == 'Да' and state == 'know payment method':
        dMachine.confirm_order()
        kb_format = kb_again

        dMachine.payment_method = ''
        dMachine.pizza_size = ''

        state = dMachine.state
        reply = "Спасибо за заказ"

    elif text == 'Нет' and state == 'know payment method':
        dMachine.start_again()
        kb_format = kb_again

        dMachine.payment_method = ''
        dMachine.pizza_size = ''

        state = dMachine.state
        reply = 'Давайте начнем заново.'

    elif text == 'Сделать новый заказ':
        dMachine.start_again()
        kb_format = kb_pizza

        dMachine.payment_method = ''
        dMachine.pizza_size = ''

        reply = 'Какую вы хотите пиццу? Большую или маленькую?'
        state = dMachine.state

    elif (text == 'Нет' or text == 'Да' or
          text == 'Наличкой' or text == 'Картой' or
          text == 'Большую' or text == 'Маленькую'):

        dMachine.start_again()
        kb_format = kb_again

        dMachine.payment_method = ''
        dMachine.pizza_size = ''

        state = dMachine.state
        reply = 'Давайте начнем заново.'

    else:
        reply = 'Я вас не понял. Попробуйте нажать на появляющуюся клавиатуру.'
        state = dMachine.state
        kb_format = None

    return reply, kb_format, state  # после этого надо сделать апдейт в бд и вызвать кнопку


def start():
    print("telegram bot started")
    executor.start_polling(dp)
