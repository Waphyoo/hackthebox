import random
from faker import Faker
from pymongo import MongoClient

from application.config import Config

fake = Faker()
client = MongoClient(Config.MONGO_URI)
db = client[Config.DB_NAME]
users_collection = db["users"]

def generate_random_user():
    email = fake.email()
    password = fake.password()
    return {
        "email": email,
        "password": password
    }


def start_migration():
    num_users = 10
    for _ in range(num_users):
        random_user = generate_random_user()
        users_collection.insert_one(random_user)


if __name__ == "__main__":
    start_migration()
    print(f"Inserted {users_collection.count_documents({})} users into the database.")
    print("Migration completed successfully.")
    print("You can now run the application and log in with one of the generated users.")
    print("Example user credentials:")
    for user in users_collection.find():
        print(f"Email: {user['email']}, Password: {user['password']}")
    print("Remember to change the password after logging in for security reasons.")
    print("Good luck and have fun with the challenge!")
    print("If you need to reset the database, you can drop the 'users' collection and run this script again.")