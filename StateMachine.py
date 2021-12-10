from transitions import Machine


class StateMachine(object):
    _states = ['ready for start', 'know size', 'know payment method', 'confirm order']
    pizza_size = ''
    payment_method = ''

    default_state = _states[0]

    def __init__(self):
        self._machine = Machine(model=self, states=StateMachine._states, initial='ready for start')

        self._machine.add_transition('accept_size', 'ready for start', 'know size')
        self._machine.add_transition('accept_pay_method', 'know size', 'know payment method')
        self._machine.add_transition('confirm_order', 'know payment method', 'confirm order')

        self._machine.add_transition('start_again', '*', 'ready for start',
                                     before='clear_data')

    def clear_data(self):
        self.pizza_size = ''
        self.payment_method = ''

    def clear_payment_method(self):
        self.payment_method = ''
