class Database:
    
    
    def __init__(self, firebase_admin, firestore):
        self.firebase_admin = firebase_admin
        self.firestore = firestore

        cred = self.firebase_admin.credentials.Certificate('./mylist-bfcc8-firebase-adminsdk-clp01-56982f095d.json')
        self.firebase_admin.initialize_app(cred)

        self.database = self.firestore.client()

    def verify_register(self, collection, field, value):
        reference = self.database.collection(collection)
        table = [row.to_dict() for row in reference.where(field, "==", value).get()]
        return True if len(table) > 0 else False

        
    def insert(self, collection, object):
        reference = self.database.collection(collection)
        reference.document().set(object)

        # check if register is done 
        return True if self.verify_register(collection, 'username', object['username']) else False        

    def read(self, collection, id):
        '''
        '''
    def update(self, collection, register):
        '''
        '''
    def delete(self, collection, id):
        '''
        '''

import firebase_admin
from firebase_admin import firestore
from model.user import User  
if __name__ == '__main__':
    db = Database(firebase_admin, firestore)
    print(db.verify_register('users', 'username', 'luise'))

    user = User("luisedu", "Luis Eduardo", "luiseduardogfranca@gmail.com")
    print(db.insert("users", user.get_user()))

    
    