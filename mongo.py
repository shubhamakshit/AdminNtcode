from pymongo import *
class Mongo:
    client = MongoClient('mongodb+srv://akshit:akshit@cluster0.dcipu28.mongodb.net/?retryWrites=true&w=majority')
    db = client['userdata']
    user_collection = db['userlist']
    usercode_collection = db['usercode']

    def __init__(self) -> None:
        pass

    def getUserCollection(self):
        return self.user_collection
    
    def getUserCodeCollection(self):
        return self.usercode_collection
    
    def getDB(self):
        return self.db
    
    def getClient(self):
        return self.client
    
    def getUserByUsername(self, username):
        return self.user_collection.find_one({'username': username})[0]
m = Mongo()