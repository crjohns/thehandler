import thehandler
import json
import random


names = None

def loadNames():
    global names
    f = open('data/names.json').read()
    names = json.loads(f)


def getName(gender):
    if not names:
        loadNames()

    firsts = filter(lambda x: x['gender'] == gender and x['part'] == 'first', names)
    anylast = filter(lambda x: x['part'] == 'last' and (x['gender'] in ['any',gender]), names)

    first = random.sample(firsts,1)[0]['name'].capitalize()
    last = random.sample(anylast,1)[0]['name'].capitalize()

    return (str(first), str(last))



