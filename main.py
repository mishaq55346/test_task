from StateMachine import StateMachine

dMachine = StateMachine()
print(dMachine.state)
dMachine.start_dialog()
print(dMachine.state)
dMachine.state = 'ready for start'
print(dMachine.state)
dMachine.start_dialog()
print(dMachine.state)

