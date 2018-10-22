import firebase_admin
from firebase_admin import firestore
from model.user import User
import datetime


class Database:
    def __init__(self, firebase_admin, firestore):
        self.firebase_admin = firebase_admin
        self.firestore = firestore

        cred = self.firebase_admin.credentials.Certificate(
            "./mylist-bfcc8-firebase-adminsdk-clp01-56982f095d.json"
        )
        self.firebase_admin.initialize_app(cred)

        self.database = self.firestore.client()

    def verify_register(self, collection, field, value):
        reference = self.database.collection(collection)
        table = [row.to_dict() for row in reference.where(field, "==", value).get()]
        return True if len(table) > 0 else False

    def create_id(self, collection):
        return self.database.collection(collection).document().id

    def insert(self, collection, object):
        reference = self.database.collection(collection)
        reference.document(object["id"]).set(object)

        # check if register is done
        return True if self.verify_register(collection, "id", object["id"]) else False

    def read(self, collection, field, value):
        reference = self.database.collection(collection)
        objects = [row.to_dict() for row in reference.where(field, "==", value).get()]
        return objects

    def update(self, collection, id, object):
        reference = self.database.collection(collection)

        # update
        if self.verify_register(collection, "id", id):
            reference.document(id).update(object)
            return True

        else:
            return False

    def delete(self, collection, id):

        # check if register is done
        if self.verify_register(collection, "id", id):
            self.database.collection(collection).document(id).delete()

            # check if register has deleted
            return False if self.verify_register(collection, "id", id) else True

        else:
            return False

db = Database(firebase_admin, firestore)

if __name__ == "__main__":
    id = db.create_id("users")
    date = datetime.datetime.now()
    user = User(id, "edugf", "MASSA", "luiseduardogfranca@gmail.com", datetime.__str__())
    db.insert("users", user.to_dict())
