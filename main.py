from transitions import Machine


class DialogMachine(object):
    states = ['ready for start', 'waiting for size', 'waiting for payment method',
              'waiting for confirmation', 'confirm order']

    def __init__(self, id):
        self.machine = Machine(model=self, states=DialogMachine.states, initial='ready for start')
        self.machine.add_transition('start dialog', 'ready for start', 'waiting for size')
        self.machine.add_transition('', 'waiting for size', 'waiting for payment method')
        self.machine.add_transition('', 'waiting for payment method', 'waiting for confirmation')
        self.machine.add_transition('', 'waiting for confirmation', 'confirm order')

        self.machine.add_transition('', 'waiting for payment method', 'ready for start')
        self.machine.add_transition('', 'waiting for confirmation', 'waiting for payment method')
        self.machine.add_transition('', 'waiting for confirmation', 'ready for start')
