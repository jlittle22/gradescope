import pymongo
from random import randint
import json

class DBManager:
    
    def _db_insert(self, collectionName, obj):
        return self.db[collectionName].insert_one(obj)    

    def insert(self, courseId, assignmentJSON):
        return self._db_insert(courseId, assignmentJSON)
    
    def listAssignmntIds(self, courseId):
        # assignmentId is subject to change
        result = self.db[courseId].aggregate([
            {"$project": {"id": "$assignmentId"}},
            {"$unwind": "$id"}
        ])
        
        return list(map(lambda elm: elm["id"], list(result)))
    
    def getAssignment(self, courseId, assignmentId):
        # assignmentId subject to change
        result = self.db[courseId].find_one({"assignmentId": assignmentId})
        return result
    
    def __init__(self):
        print("connecting to DB...", end="")
        client = pymongo.MongoClient("mongodb+srv://gs_user:gradescopeUser1@cluster0.ayfa8.mongodb.net/courses?retryWrites=true&w=majority")
        print("connected")
        self.db = client.courses
        
    
    

if __name__ == "__main__":
    manager = DBManager()
    # with open("./gs_web_api/test_data/test.json") as test_json:
    #     print("test insert")
    #     manager.insert("test_class", json.loads(test_json.read()))
    #     print("done")
    print(manager.listAssignmntIds("test_class"))
    print(manager.getAssignment("test_class", 1))
   
# gradescopeUser1     