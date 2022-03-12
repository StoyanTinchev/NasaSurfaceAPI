import random
import time
from threading import Thread


class RedisCustom(Thread):
    def __init__(self):
        super().__init__()
        self.dict = {}

    def set(self, key, value):
        self.dict[key] = value

    def get(self, key):
        return self.dict[key]

    def contains(self, key):
        return key in self.dict

    def remove_all(self):
        self.dict = {}

    def run(self):
        while True:
            time.sleep(random.randint(60*30, 60*60*2))
