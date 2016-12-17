import os
import base64

class SessionStore():
    def __init__(self):
        #session data is a dictionary of dictionaries
        self.sessionData = {}
        return

    def createSessionObject(self):
        newSessionID = self.generateSessionID()
        self.sessionData[newSessionID] = {}
        return newSessionID

    def getSessionObject(self, sid):
        print("Data in GSO", self.sessionData)
        if sid in self.sessionData:
            return self.sessionData[sid]
        else:
            return None

    def deleteSessionObject(self, sid):
        self.sessionData[sid] = None

    def generateSessionID(self):
        #generate random 64 number/mess of byte data
        ros = os.urandom(64)
        #convert to base64 string
        rb64 = base64.b64encode(ros)
        #decode string into usable characters (utf8)
        rstr = rb64.decode("utf-8", "strict")
        return rstr
