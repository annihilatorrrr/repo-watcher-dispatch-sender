from pymongo import MongoClient
import datetime
from config import Vars

db_client = MongoClient(Vars.DB_URI)
main_db = db_client["repo_watcher_dispatch_sender"]


class MongoDB:
    """Class for interacting with Bot database."""

    def __init__(self, collection) -> None:
        self.collection = main_db[collection]

    # Insert one entry into collection
    def insert_one(self, document):
        result = self.collection.insert_one(document)
        return repr(result.inserted_id)

    # Find one entry from collection
    def find_one(self, query):
        result = self.collection.find_one(query)
        if result:
            return result
        return False

    # Find entries from collection
    def find_all(self, query=None):
        if query is None:
            query = {}
        return [document for document in self.collection.find(query)]

    # Count entries from collection
    def count(self, query=None):
        if query is None:
            query = {}
        return self.collection.count_documents(query)

    # Delete entry/entries from collection
    def delete_one(self, query):
        self.collection.delete_many(query)
        after_delete = self.collection.count_documents({})
        return after_delete

    # Replace one entry in collection
    def replace(self, query, new_data):
        old = self.collection.find_one(query)
        _id = old["_id"]
        self.collection.replace_one({"_id": _id}, new_data)
        new = self.collection.find_one({"_id": _id})
        return old, new

    # Update one entry from collection
    def update(self, query, update):
        result = self.collection.update_one(query, {"$set": update})
        new_document = self.collection.find_one(query)
        return result.modified_count, new_document

    @staticmethod
    def db_command(command: str):
        return main_db.command(command)


class Repo(MongoDB):
    db_name = "main"

    def __init__(self):
        super().__init__(self.db_name)

    def get_all_repos(self):
        return self.find_all({})

    def update_repo(self, repo: dict, last_commit: datetime.datetime):
        # using '/' could have some issue, so replaced with '_
        src_repo = repo["repo"].replace("/", "_")
        repo_data = self.find_one({"_id": src_repo})
        if not repo_data:
            repo_data = {
                "_id": src_repo,
                "last_commit": last_commit,
            }
            self.insert_one(repo_data)
            return None
        self.update({"_id": src_repo}, {"last_commit": last_commit})
        return repo_data["last_commit"]

    def delete_repo(self, user_id: int):
        return self.delete_one({"_id": user_id})
