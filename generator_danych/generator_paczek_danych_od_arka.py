from datetime import datetime
from random import randrange
import json


def generate_json_paczka(numer_seryjny):
    sn = numer_seryjny
    a = randrange(0, 9)
    b = randrange(0, 9)
    c = randrange(0, 9)
    z = randrange(0, 9)
    kod = "0000000"

    value = {
        "sn": sn,
        "a": a,
        "b": b,
        "c": c,
        "z": z,
        "kod": kod
    }

    return json.dumps(value)


print(generate_json_paczka("AXZFS213"))