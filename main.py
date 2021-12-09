from DialogMachine import DialogMachine

dMachine = DialogMachine(123)
print(dMachine.state)
dMachine.start_dialog()
print(dMachine.state)

