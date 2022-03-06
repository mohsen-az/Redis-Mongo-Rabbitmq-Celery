from datetime import datetime

from bson import ObjectId

from clockify.data import users, projects
from mongo_connection import MongoDatabase

mongo = MongoDatabase()
db = mongo.client.clockify_normalized

users_collection = db.users
projects_collection = db.projects
reports_collection = db.reports


def store_one():
    """Just run at the first run of the script"""
    if users_collection.count_documents({}) == 0:
        print("Save data in users collection")
        users_collection.insert_many(users)
    if projects_collection.count_documents({}) == 0:
        print("Save data in projects collection")
        projects_collection.insert_many(projects)


def save_record():
    hossein = users_collection.find_one({"username": "hossein"})
    shop = projects_collection.find_one({'name': "Online Shop"})

    report = reports_collection.insert_one(
        {
            "user": hossein.get("_id"),
            "project": shop.get("_id"),
            "start_time": datetime.now()
        }
    )
    return report


def set_end_time(object_id):
    query_filter = {"_id": ObjectId(object_id)}
    update = {"$set": {'end_time': datetime.now()}}
    reports_collection.update_one(
        filter=query_filter,
        update=update
    )


def show_reports():
    query_filter = users_collection.find_one({"username": "hossein"})
    pipeline = [
        {"$match": {"user": query_filter.get("_id")}},
        {"$lookup": {"from": "users", "localField": "user", "foreignField": "_id", "as": "user"}},
        {"$unwind": "$user"},
        {"$lookup": {"from": "projects", "localField": "project", "foreignField": "_id", "as": "project"}},
        {"$unwind": "$project"},
    ]
    query = reports_collection.aggregate(pipeline=pipeline)

    for report in query:
        duration = (report.get('end_time') - report.get('start_time')).seconds

        print(f"Username: {report.get('user').get('username')}\n"
              f"Project: {report.get('project').get('name')}\n"
              f"Duration: {duration} Seconds")

    print("######################################")

    query_filter = users_collection.find_one({"username": "hossein"})  # hint-1
    for report in reports_collection.find({"user": query_filter.get("_id")}):  # hint-2
        user = users_collection.find_one({"_id": ObjectId(report.get('user'))})  # hint-3
        project = projects_collection.find_one({"_id": ObjectId(report.get("project"))})  # hint-4
        duration = (report.get('end_time') - report.get('start_time')).seconds

        print(f"Username: {user.get('username')}\n"
              f"Project: {project.get('name')}\n"
              f"Duration: {duration} Seconds")


if __name__ == '__main__':
    # store_one()
    # save_record()
    # set_end_time(object_id="6223c4bb7fa9d10dacb85f41")
    show_reports()
