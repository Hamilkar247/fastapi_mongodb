import random


def generataVector():
    array_data = []
    array_data.clear()
    a = random.randint(0, 50)
    b = random.randrange(0, 50)
    c = random.randint(0, 50)
    d = random.randint(0, 50)
    e = random.randint(0, 50)
    f = random.randint(0, 50)
    array_data.append(a)
    array_data.append(b)
    array_data.append(c)
    array_data.append(d)
    array_data.append(e)
    array_data.append(f)
    print(f"print array: {array_data}")
    return array_data
