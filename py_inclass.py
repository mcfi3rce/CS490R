import threading
import hashlib

# Can use globals

def fun(numbers):
    # numbers = [2 * x for x in numbers]
    for i in numbers:
        print(i)
    # print("Running thread {:d}".format(num))

numbers = range(500)
half = int(len(numbers) / 2)

t1 = threading.Thread(target = fun, args = ([numbers[:half]]))
t2 = threading.Thread(target = fun, args = ([numbers[half:]]))

print("Starting the thread")
t2.start()
t1.start()
t1.join()
t2.join()
