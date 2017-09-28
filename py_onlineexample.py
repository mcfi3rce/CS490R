import threading

class PrimeNumber(threading.Thread):
    def __init__(self, number):
        threading.Thread.__init__(self)
        self.Number = number

    def run(self):
        counter = 2
        while counter*counter < self.Number:
            if self.number % counter == 0:

