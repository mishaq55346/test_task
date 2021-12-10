import telebot

from Database import Database
from StateMachine import StateMachine
from keyboa import Keyboa

dMachine = StateMachine()
bot = telebot.TeleBot('5016454045:AAHwLAPdAiWnsjfI09-0rWHSl8iYVDyIpXs')
db = Database()

pizza_size_keyboard = ['Большую', 'Маленькую']
payment_method_keyboard = ['Наличкой', 'Картой']

kb_pizza = Keyboa(items=pizza_size_keyboard, copy_text_to_callback=True)
kb_payment = Keyboa(items=payment_method_keyboard, copy_text_to_callback=True)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    person_id = message.from_user.id
    if not(db.has_user(person_id)):
        db.add_user(person_id, dMachine.default_state)
    else:
        dMachine.state = db.get_state(person_id)
        dMachine.pizza_size = db.get_pizza_size(person_id)
        dMachine.payment_method = db.get_payment_method(person_id)
    if dMachine.state == 'ready for start':
        bot.send_message(chat_id=person_id, reply_markup=kb_pizza, text="Какую вы хотите пиццу? Большую или маленькую?")


    #bot.send_message(message.from_user.id, message.from_user.id)
    #global num
    #if message.text == "get num":
    #    bot.send_message(message.from_user.id, "num = " + str(num))
    #if str(message.text).startswith("set num"):
    #    num = int(str(message.text).replace("set num ", ''))
    #    bot.send_message(message.from_user.id, "num now = " + str(num))
    #    _number = num
    #    # bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")


bot.polling(none_stop=True, interval=0)


def message_processing(message):
    pass
    # if(dMachine.state == 'ready for start'):
    # if(dMachine.state == 'waiting for size'):
    # if(dMachine.state == 'waiting for payment method'):
    # if(dMachine.state == 'waiting for confirmation'):
    # if(dMachine.state == 'confirm order'):
