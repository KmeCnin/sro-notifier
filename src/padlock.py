import os

lockFile = os.path.dirname(os.path.realpath(__file__))+'/../.locked'

def lock():
    if os.path.isfile(lockFile):
        raise Exception('Notifier is running already.')
    with open(lockFile, 'w') as file:
        file.write('')

def unlock():
    if not os.path.isfile(lockFile):
        raise Exception('Cannot unlock a not locked process.')
    os.remove(lockFile)
