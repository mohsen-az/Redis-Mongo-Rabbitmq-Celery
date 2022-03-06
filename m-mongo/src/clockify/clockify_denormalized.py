from datetime import datetime

from bson import ObjectId

from clockify.data import users, projects
from mongo_connection import MongoDatabase

mongo = MongoDatabase()
db = mongo.client.clockify_denormalized

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
            "user": hossein,
            "project": shop,
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
    query_filter = {"user.username": "hossein"}
    for report in reports_collection.find(query_filter):  # hint-1
        user = report.get("user")
        project = report.get("project")
        duration = (report.get('end_time') - report.get('start_time')).seconds

        print(f"Username: {user.get('username')}\n"
              f"Project: {project.get('name')}\n"
              f"Duration: {duration} Seconds")


if __name__ == '__main__':
    # store_one()
    # save_record()
    # set_end_time(object_id="6223ba258cb725b9cdc0628c")
    show_reports()
