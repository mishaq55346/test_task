

from Database import Database
from StateMachine import StateMachine

TOKEN = ''
dMachine = StateMachine()
# bot = Bot(TOKEN)
banlist = ['103953122']
db = Database()


def handle_text_messages(message):
    print("facebook. id=" + str(message.from_user.id) + " used bot. input: " + message.text)
    if str(message.from_user.id) in banlist:
        return
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
        send_message(chat_id=person_id, text="Спасибо за заказ")
    if message.text == 'Нет' or message.text == 'Сделать новый заказ':
        dMachine.start_again()
        db.update_info(person_id, dMachine.state, dMachine.pizza_size, dMachine.payment_method)
        send_message(chat_id=person_id, text="Давайте начнем заново")
    if dMachine.state == 'ready for start':
        send_message(chat_id=person_id,
                     text="Какую вы хотите пиццу? Большую или маленькую?")
    elif dMachine.state == 'know size':
        send_message(chat_id=person_id,
                     text="Как вы будете платить?")
    elif dMachine.state == 'know payment method':
        send_message(chat_id=person_id,
                     text="Вы хотите {} пиццу, оплата - {}?"
                     .format(dMachine.pizza_size.lower(), dMachine.payment_method.lower()))


def send_message(chat_id, text):
    pass


def start():
    print("facebook bot started")
