from mongomantic import connect, BaseRepository, MongoDBModel, Index
from mongomantic.utils.safe_repository import SafeRepository


connect("localhost:27017", "test_db")


class User(MongoDBModel):
    first_name: str
    last_name: str


class UserRepository(SafeRepository):
    class Meta:
        model = User
        collection = "user"
        indexes = [
            Index(fields=["+first_name"]),
            Index(fields=["+first_name", "-last_name"], unique=True)
        ]


user = User(first_name="John", last_name="Smith")

user = UserRepository.save(user)

print(user.first_name)

#print(user.id)

#user = UserRepository.get(id="123") #DoesNotExist error handled

#assert user is None