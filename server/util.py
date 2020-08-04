import random
import string


def randStr(lens):
    return ''.join([random.choice(string.ascii_letters + string.digits) for n in range(lens)])
