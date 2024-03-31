import threading
import time
import random


class Philosopher(threading.Thread):
    def __init__(self, index, left_fork: threading.Lock, right_fork: threading.Lock):
        super().__init__()
        self.index = index
        self.left_fork = left_fork
        self.right_fork = right_fork
        self.starving_time = 0

    def run(self):
        while True:
            self.think()
            while not self.try_eat():
                self.starving_time += 1
                time.sleep(0.1)
                print(self.starving_time, self.index)
            else:
                self.starving_time = 0

    def think(self):
        time.sleep(random.random())

    def try_eat(self):
        if not self.left_fork.acquire(False):
            return

        if not self.right_fork.acquire(False):
            self.left_fork.release()

        else:
            self.eat()
            self.right_fork.release()
            self.left_fork.release()
            return True

    def eat(self):
        time.sleep(max(random.randint(1, 10), 2))


def main():
    num_philosophers = 5
    forks = [threading.Lock() for _ in range(num_philosophers)]
    philosophers = [
        Philosopher(i, forks[i], forks[(i + 1) % num_philosophers])
        for i in range(num_philosophers)
    ]

    for philosopher in philosophers:
        philosopher.start()

    for philosopher in philosophers:
        philosopher.join()


if __name__ == "__main__":
    main()
