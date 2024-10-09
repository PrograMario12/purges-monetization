''' This module is used to get the current turn '''
import datetime

class Support:
    ''' This class is used to get the current turn '''
    def __init__(self):
        self._name = "support"

    def get_turn(self):
        ''' Get the current turn '''
        time = datetime.datetime.now().time()

        if datetime.time(23, 0, 0) <= time or time < datetime.time(7, 0, 0):
            return 3
        if datetime.time(7, 0, 0) <= time < datetime.time(15, 0, 0):
            return 1
        return 2

if __name__ == "__main__":
    Support().get_turn()
