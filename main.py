from transitions import Machine


class DialogMachine(object):
    states = ['ready for start', 'waiting for size', 'waiting for payment method',
              'waiting for confirmation', 'confirm order']
    pizza_size = ''
    payment_method = ''

    def __init__(self, id):
        self.machine = Machine(model=self, states=DialogMachine.states, initial='ready for start')

        self.machine.add_transition('start dialog', 'ready for start', 'waiting for size')
        self.machine.add_transition('accept size', 'waiting for size', 'waiting for payment method')
        self.machine.add_transition('accept pay method', 'waiting for payment method', 'waiting for confirmation')
        self.machine.add_transition('confirm order', 'waiting for confirmation', 'confirm order')

        self.machine.add_transition('start again', '*', 'ready for start',
                                    before='clear_data')
        self.machine.add_transition('back from pay', 'waiting for payment method', 'waiting for size',
                                    before='clear_payment_method')
        self.machine.add_transition('back from ', 'waiting for confirmation', 'waiting for payment method',
                                    before='clear_payment_method')

    def clear_data(self):
        self.pizza_size = ''
        self.payment_method = ''

    def clear_payment_method(self):
        self.payment_method = ''
