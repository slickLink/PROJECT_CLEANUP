
import random, base64

def random_string(length):
    ''' Generates a random string of size (length)'''

    string = 'abcdefghijklmnopqrstuvwxyz0123456789'
    return ''.join(random.choice(string) for x in range(length))

def encode_pair(first, second):
    ''' returns a base64 encoded <first:second> string '''

    encoded_data = base64.b64encode(bytes(f"{first}:{second}", "ISO-8859-1")).decode("ascii")
    return encoded_data

def convert_time(ms):
    if type(ms) is not int:
        return None

    seconds = int((ms / 1000) % 60)
    minutes = int((ms / (1000 * 60)) % 60)
    return '{}:{}'.format(minutes, seconds)