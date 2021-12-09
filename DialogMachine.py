from transitions import Machine


class DialogMachine(object):
    _states = ['ready for start', 'waiting for size', 'waiting for payment method',
               'waiting for confirmation', 'confirm order']
    _pizza_size = ''
    _payment_method = ''

    default_state = _states[0]

    def __init__(self):
        self._machine = Machine(model=self, states=DialogMachine._states, initial='ready for start')

        self._machine.add_transition('start_dialog', 'ready for start', 'waiting for size')
        self._machine.add_transition('accept_size', 'waiting for size', 'waiting for payment method')
        self._machine.add_transition('accept_pay_method', 'waiting for payment method', 'waiting for confirmation')
        self._machine.add_transition('confirm_order', 'waiting for confirmation', 'confirm order')

        self._machine.add_transition('start_again', '*', 'ready for start',
                                     before='clear_data')
        self._machine.add_transition('back_from_pay', 'waiting for payment method', 'waiting for size',
                                     before='clear_payment_method')
        self._machine.add_transition('back_from_confirm', 'waiting for confirmation', 'waiting for payment method',
                                     before='clear_payment_method')

    def clear_data(self):
        self._pizza_size = ''
        self._payment_method = ''

    def clear_payment_method(self):
        self._payment_method = ''
