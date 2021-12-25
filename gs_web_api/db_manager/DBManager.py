import pymongo
from random import randint
import json

class DBManager:
    def _db_insert(self, db, collectionName, obj):
        return db[collectionName].insert_one(obj)    

    def insertAssignment(self, courseId, assignmentJSON):
        return self._db_insert(self.courses, courseId, assignmentJSON)

    def insertSourceData(self, statisticsJSON):
        # inserts / updates current statistics document
        pass

    def setTargetAssignment(self, cid, aid):
        pass 
    
    def listAssignmentIds(self, courseId):
        # assignmentId is subject to change
        result = self.client.courses[courseId].aggregate([
            {"$project": {"id": "$assignmentId"}},
            {"$unwind": "$id"}
        ])
        
        return list(map(lambda elm: elm["id"], list(result)))
    
    def getAssignment(self, courseId, assignmentId):
        # assignmentId subject to change
        result = self.client.courses[courseId].find_one({"assignmentId": assignmentId})
        return result
    
    def __init__(self):
        print("connecting to DB...", end="")
        self.client = pymongo.MongoClient("mongodb+srv://gs_user:gradescopeUser1@cluster0.ayfa8.mongodb.net/courses?retryWrites=true&w=majority")
        print("connected")
    

if __name__ == "__main__":
    manager = DBManager()
    print(manager.listAssignmentIds("test_class"))
    print(manager.getAssignment("test_class", 1))
   
# gradescopeUser1     