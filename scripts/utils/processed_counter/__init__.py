import os

PATH = os.path.abspath(os.path.dirname(__file__))

def read_status():
    with open(os.path.join(PATH,'counter.txt'), 'r') as f:
        return f.readlines()[0]


def write_status(status):
    with open(os.path.join(PATH,'counter.txt'), 'w') as f:
        f.write(status)

