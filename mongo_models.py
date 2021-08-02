import pymongo
import generateData

myclient = pymongo.MongoClient("mongodb://localhost:27017")
db_miernik = myclient["miernik"]
pomiar = db_miernik["pomiar"]
print(pomiar.drop())

wektor_danych = []
wektor_danych.append(generateData.generataVector())


dane_pomiarowe = {
     "temperatura": wektor_danych.__getitem__(0)[0],
     "pm2_5": wektor_danych.__getitem__(0)[1],
     "pm5": wektor_danych.__getitem__(0)[2],
     "pm10": wektor_danych.__getitem__(0)[3],
     "hydroetyl": wektor_danych.__getitem__(0)[4],
     "tlen": wektor_danych.__getitem__(0)[5]
}

print(dane_pomiarowe)
print(db_miernik.list_collection_names())

x = pomiar.insert_one(dane_pomiarowe)

print(x.inserted_id)
print(db_miernik.list_collection_names())

for x in pomiar.find():
    print(x)

#print(pomiar.drop())
print(db_miernik.list_collection_names())