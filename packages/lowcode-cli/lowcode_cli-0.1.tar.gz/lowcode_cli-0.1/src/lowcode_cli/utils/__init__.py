import uuid
import string
import random


def make_unique_string(length: int = 6):
    return "".join(random.sample(string.ascii_letters, length))
