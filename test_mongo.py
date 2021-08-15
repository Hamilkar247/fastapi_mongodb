import pymongo
from models_miernik import db_miernik

myclient = pymongo.MongoClient("mongodb://localhost:27017")
mydb = myclient["mydatebase"]
mycol = mydb["customers"]

print(mydb.list_collection_names())

# mydict = { "name" : "Erich", "address" : "11 September" }

mylist = [
    {"name": "Amy", "address": "Apple st 652"},
    {"name": "Hannah", "address": "Mountain 21"},
    {"name": "Michael", "address": "Valley 345"},
    {"name": "Sandy", "address": "Ocean blvd 2"},
    {"name": "Betty", "address": "Green Grass 1"},
    {"name": "Richard", "address": "Sky st 331"},
    {"name": "Susan", "address": "One way 98"},
    {"name": "Vicky", "address": "Yellow Garden 2"},
    {"name": "Ben", "address": "Park Lane 38"},
    {"name": "William", "address": "Central st 954"},
    {"name": "Chuck", "address": "Main Road 989"},
    {"name": "Viola", "address": "Sideway 1633"}
]

# mylist = [
# { "_id": 1, "name": "John", "address": "Highway 37"},
# { "_id": 2, "name": "Peter", "address": "Lowstreet 27"},
# { "_id": 3, "name": "Amy", "address": "Apple st 652"},
# { "_id": 4, "name": "Hannah", "address": "Mountain 21"},
# { "_id": 5, "name": "Michael", "address": "Valley 345"},
# { "_id": 6, "name": "Sandy", "address": "Ocean blvd 2"},
# { "_id": 7, "name": "Betty", "address": "Green Grass 1"},
# { "_id": 8, "name": "Richard", "address": "Sky st 331"},
# { "_id": 9, "name": "Susan", "address": "One way 98"},
# { "_id": 10, "name": "Vicky", "address": "Yellow Garden 2"},
# { "_id": 11, "name": "Ben", "address": "Park Lane 38"},
# { "_id": 12, "name": "William", "address": "Central st 954"},
# { "_id": 13, "name": "Chuck", "address": "Main Road 989"},
# { "_id": 14, "name": "Viola", "address": "Sideway 1633"}
# ]

# x = mycol.insert_one(mydict)
x = mycol.insert_many(mylist)

# x = mycol.find_one()

print(x.inserted_ids)

print(x)

# Return all documents in the "customers" collection, and print each document:
print("### zwroc wszystko z dokumentu customers kolekcji i wydrukuj")
for x in mycol.find():
    print(x)

# drukuj ale bez id
print("### drukuj ale bez id")
for x in mycol.find({}, {"_id": 0, "name": 1, "address": 1}):
    print(x)

# wydrukuj wszystko bez adresu
print("### wydrukuj wszystko bez adresu")
for x in mycol.find({}, {"address": 0}):
    print(x)

# You get an error if you specify both 0 and 1 values in the same object
# (except if one of the fields is the _id field):
# for x in mycol.find({}, {"name": 1, "address": 0}):
#    print(x)

######## proste zapytanie
print("### Proste zapytanie")
myquery = {"address": "Park Lane 38"}
mydoc = mycol.find(myquery)
#
for x in mydoc:
    print(x)


###### nieco bardziej skomplikowane zapytanie - wyszukuje zapytania zaczynajace sie litera "S"
# myquery = {"address": {"$regex": "^S"}}
#
# mydoc = mycol.find(myquery)
#
# for x in mydoc:
#    print(x)

######sortowanie
# jakby co
# sort("name", 1) #ascending
# sort("name", -1) #descending
# mydoc = mycol.find().sort("name")
#
# for x in mydoc:
#    print(x)

##### Usuwanie jednego dokukumentu z adresem 21
# myquery = { "address": "Mountain 21" }
# mycol.delete_one(myquery)

####### Usuwanie wielu dokumentów
# myquery = {"address": {"$regex": "^S"}}
# x = mycol.delete_many(myquery)
# print(x.deleted_count, " documents deleted.")

# usunie stworzone kolekcje
# print(mycol.drop())

########### update jednego rekordu
# myquery = {"address": "Highway 37"}
# newvalues = {"$set": {"address": "11 Listopada"}}
#
# mycol.update_one(myquery, newvalues)
#
## print "customers" after the update
# for x in mycol.find():
#    print(x)


############ uodate wiele rekordów
# myquery = {"address": {"$regex": "^S"}}
# newvalues = {"$set": {"name": "Minnie"}}
# x = mycol.update_many(myquery, newvalues)
#
# print(x.modified_count, "documents updated.")


############ ograniczenie liczby zlapanych rekordow z bazy
# myresult = mycol.find().limit(5)
#
##print the result:
# for x in myresult:
#  print(x)


def def_db_miernik():
    print("--------------")
    my_result = db_miernik.zbior_sesji.find()
    for x in my_result:
        print(x)
        print(x['czy_aktywna'])


def_db_miernik()
