import time
import threading
import random
import string

num_threads = 15
thread_timeout = 10
my_global_value = 5
my_global_sentence = "This is a sentence that will get clobbered"

class SuperThread(threading.Thread):
    def __init__(self, id):
        threading.Thread.__init__(self)
        self.thread_id = id
        # print("Hi, I'm a new thread! ID: {:2d}".format(self.thread_id))

    def run(self):
        global thread_timeout
        global my_global_value
        global my_global_sentence

        prev_int = my_global_value
        started_time = time.time()
        print("Starting new thread ID: {:2d}".format(self.thread_id))
        while time.time() - thread_timeout < started_time:
            time.sleep(1)
            letter = random.choice(string.ascii_letters)
            new = random.choice(string.ascii_letters)

            my_global_sentence = my_global_sentence.replace(letter, new)

            difference_from_last = prev_int - my_global_value

            if random.choice([True, False]):
                my_global_value += self.thread_id
            else:
                my_global_value -= self.thread_id

            prev_int = my_global_value

            print("ID: {:<2d} Global int changed by: {:3d} string: {:s}".format(self.thread_id, difference_from_last, my_global_sentence))

        print("Thread exiting ID: {:2d}".format(self.thread_id))

print("Original sentence: {:s}".format(my_global_sentence))

for i in range(num_threads):
    t = SuperThread(i)
    t.start()
    time.sleep(1 / num_threads)

print("Exiting main thread")
