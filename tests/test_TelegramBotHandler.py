import pytest
from aiogram import types
from aiogram.types import User

from StateMachine import StateMachine
from bots.telegram.telegramBotHandler import handle_message
import bots.telegram.telegramBotHandler as f

dMachine = StateMachine()
def setup():
    dMachine.state = dMachine.default_state

def test_handle_messages_accept_size():
    dMachine.state = 'ready for start'
    dMachine.accept_size()
    test, test_kb, test_response_state = handle_message('Большую', 'ready for start')
    assert dMachine.state == test_response_state

def test_handle_messages_accept_pay_method():
    dMachine.state = 'know size'
    dMachine.accept_pay_method()
    test, test_kb, test_response_state = handle_message('Картой', 'know size')
    assert dMachine.state == test_response_state

def test_handle_messages_confirm_order():
    dMachine.state = 'know payment method'
    dMachine.confirm_order()
    test, test_kb, test_response_state = handle_message('Да', 'know payment method')
    assert dMachine.state == test_response_state

def test_handle_messages_start_again():
    dMachine.state = 'know size'
    dMachine.start_again()
    test, test_kb, test_response_state = handle_message('Сделать новый заказ', 'know size')
    assert dMachine.state == test_response_state
    test, test_kb, test_response_state = handle_message('Нет', 'know payment method')
    assert dMachine.state == test_response_state

def test_handle_messages_unknown_message():
    test_response, test_kb, test_state = handle_message('Налом', 'know payment method')
    assert test_response == 'Я вас не понял. Попробуйте нажать на появляющуюся клавиатуру.'



