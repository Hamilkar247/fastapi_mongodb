from pydantic import BaseModel


class Person(BaseModel):
    first: str
    last: str
    zip_code: str

    def __str__(self):
        return "%s %s: %s" % (self.first, self.last, self.zip_code)


#person = Person(first="Bruce", last="Wayne", zip_code="10021")
####inna opcje
person_dict = {
    "first": "Bruce",
    "last": "Wayne",
    "zip_code": "10021"
}
#person = Person(
#    first = person_dict["first"],
#    last = person_dict["last"],
#    zip_code = person_dict["zip_code"]
#)

### to wyżej mozna zastapic  ** - pythonowym operatorem rozpakowania
person = Person(**person_dict)

#print(person)