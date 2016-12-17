import json
import sys
from http import cookies
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from session_store import SessionStore
from userdb import UserDB
from messagedb import MessageDB
from passlib.hash import bcrypt
from datetime import datetime

#hash = bcrypt.encrypt("password")
#bcrypt.verify("password", hash)

#Full user data tuple format:
# 0:ID  1:email  2:encpass  3:fname  4:lname

#big, scary global variable
#CS3005 student [TRIGGERED]
gSessionStore = SessionStore()

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.load_cookie()
        if self.path.startswith('/messages'):
            self.load_session()
            session_id = self.cookie["sessionid"].value
            session_data = gSessionStore.getSessionObject(session_id)
            message = "Error getting user data from session."
            if "userid" in session_data:
                self.send_response(200)
##                userData = self.getUserByID(session_data["userid"])
##                message = "Welcome, " + userData[3] + " " + userData[4] + "."
                ##Row factory creates list of dictionaries from database tuples to send as JSON data
                messages = self.getAllMessages()
                msglist = []
                for m in messages:
                    # m[0] is the id, value is list of attributes
                    # 0 id, 1 timestamp, 2 sender, 3 message
                    msgdict = {"id":m[0], "timestamp":m[1], "sender": m[2], "message":m[3]}
                    msglist.append(msgdict)
                jsondata = json.dumps(msglist)
                self.send_header('Content-Type','application/json')
                self.send_cookie()
                self.sendCORSHeaders()
                self.end_headers()
                self.wfile.write(bytes(jsondata, "utf-8"))
            else:
                message = "Not logged in"
                self.handle401(message)
        else:
            self.handle404()

    def do_POST(self):
        self.load_cookie()
        self.load_session()
        session_id = self.cookie["sessionid"].value
        session_data = gSessionStore.getSessionObject(session_id)
        if self.path.startswith("/users"):
            #function that reads incoming text/form data
            parsed_data = self.parseInputData()
            try:
                email = parsed_data['email'][0]
                encpass = bcrypt.encrypt(parsed_data['encpass'][0])
                print(encpass)
                firstname = parsed_data['firstname'][0]
                lastname = parsed_data['lastname'][0]
            except:
                print("ERROR. User creation error. Invalid data.")
                self.handle401("Insufficient or invalid input.")
                return
            if self.emailExists(email):
                self.handle422("User with that email already exists.")
            else:
                self.createUser(email,encpass,firstname,lastname)
                self.send_response(201)
                self.send_cookie()
                self.sendCORSHeaders()
                self.end_headers()
        elif self.path.startswith("/session"):
            parsed_data = self.parseInputData()
            try:
                email = parsed_data['email'][0]
                encpass = parsed_data['encpass'][0]
                #print(encpass)
            except:
                print("ERROR. User authentication error. Invalid data.")
                self.handle401("Insufficient or invalid input.")
                return
            userData = self.getUserByEmail(email)
            # Could use emailExists method but then I'd be
            # accessing the DB twice for no reason. Save them millis yo.
            if userData is not None:
                #print(userData)
                if bcrypt.verify(encpass,userData[2]):
                    self.send_response(200)
                    session_data["userid"] = userData[0]
                    session_data["userfirstname"] = userData[3]
                    self.send_cookie()
                    self.sendCORSHeaders()
                    self.end_headers()
                    print("Correct login credentials.")
                else:
                    self.handle401("Incorrect username or password.")
            else:
                self.handle401("Incorrect username or password.")
                
        elif self.path.startswith("/messages"):
            parsed_data = self.parseInputData()
            try:
                timestamp = parsed_data['timestamp'][0]
                message = parsed_data['message'][0]
            except:
                print("ERROR. Message post error. Invalid data.")
                self.handle401("Insufficient or invalid input.")
                return
            if "userid" in session_data:
                self.insertMessage(timestamp, session_data["userfirstname"], message)
                self.send_response(201)
                self.send_cookie()
                self.sendCORSHeaders()
                self.end_headers()
            else:
                self.handle401("Must be logged in to send messages. Please refresh the page.")
            
        else:
            self.handle404()

    def sendCORSHeaders(self):
        self.send_header('Access-Control-Allow-Origin',self.headers["Origin"])
        self.send_header("Access-Control-Allow-Credentials", "true")

    def handle404(self):
        self.send_response(404)
        self.sendCORSHeaders()
        self.send_header('Content-Type','text/plain')
        self.send_cookie()
        self.end_headers()
        self.wfile.write(bytes("Error 404: Page not found.","utf-8"))

    def handle422(self, message):
        self.send_response(422)
        self.sendCORSHeaders()
        self.send_header('Content-Type','text/plain')
        self.send_cookie()
        self.end_headers()
        self.wfile.write(bytes("Error 422: "+message,"utf-8"))

    def handle401(self, message):
        self.send_response(401)
        self.sendCORSHeaders()
        self.send_header('Content-Type','text/plain')
        self.send_cookie()
        self.end_headers()
        self.wfile.write(bytes("Error 401: "+message,"utf-8"))

    def parseInputData(self):
        readlength = int(self.headers['Content-Length'])
        rawdata = self.rfile.read(readlength).decode("utf-8")
        parsed_data = parse_qs(rawdata)
        print(parsed_data)
        return parsed_data
            
    def load_cookie(self):
        if 'Cookie' in self.headers:
            self.cookie = cookies.SimpleCookie(self.headers['Cookie'])
        else:
            self.cookie = cookies.SimpleCookie()

    def load_session(self):
        ##check for cookie
        if "sessionid" in self.cookie:
            ##try to load session object using session id
            session_id = self.cookie["sessionid"].value
            session_data = gSessionStore.getSessionObject(session_id)
            print("sesData:",session_data)
            if session_data is not None:
                print("Got some data.")
            else:
                ##create session object
                ##store id in cookie
                print("No session data found. Creating session object.")
                sid = gSessionStore.createSessionObject()
                self.cookie["sessionid"] = sid
                print("New session ID:",sid)
        else:
            print("No session cookie found. Creating session.")
            sid = gSessionStore.createSessionObject()
            self.cookie["sessionid"] = sid
            print("New session ID:",sid)
            
    def send_cookie(self):
        for morsel in self.cookie.values():
            self.send_header("Set-Cookie", morsel.OutputString())

    ## Database Methods
    def createUser(self,email,encpass,firstname,lastname):
        db = UserDB()
        db.createUser(email,encpass,firstname,lastname)

    def emailExists(self,email):
        db = UserDB()
        return db.emailExists(email)

    def getUserByEmail(self, email):
        db = UserDB()
        return db.getUserByEmail(email)

    def getUserByID(self, userid):
        db = UserDB()
        return db.getUserByID(userid)

    def getAllMessages(self):
        db = MessageDB()
        return db.getAllMessages()

    def insertMessage(self, timestamp, sender, message):
        db = MessageDB()
        db.insertMessage(timestamp, sender, message)   

def run():
    port = 8080
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    listen = ('0.0.0.0',port)
    server = HTTPServer(listen, MyServer)

    db = UserDB()
    db.createTableUsers()
    db = None
    
    db2 = MessageDB()
    db2.createTableMessages()
    db2 = None
    
    print("Listening...")
    server.serve_forever()

run()
















