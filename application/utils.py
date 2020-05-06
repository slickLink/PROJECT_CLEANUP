
import random

def random_string(length):
    ''' Generates a random string of size (length)'''

    string = 'abcdefghijklmnopqrstuvwxyz0123456789'
    return ''.join(random.choice(string) for x in range(length))

