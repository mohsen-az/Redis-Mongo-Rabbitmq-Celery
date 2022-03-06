import random

from mongo_connection import MongoDatabase

mongo = MongoDatabase()

# Create database
db = mongo.client.users_data

# Create collection
user_records_collection = db.users


def import_users_data(count=100000):
    """
    Write speed for 100000 data: 27.960s
    :param count:
    :return:
    """
    for index in range(count):
        user_records_collection.insert_one(
            {
                f"user_{index}": random.randint(1, 10)
            }
        )
    print(f'{count} users recorded imported successfully.')


if __name__ == '__main__':
    import_users_data()
