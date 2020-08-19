

import json 
import socket
import http.server
import socketserver
import webbrowser
import face

PORT = 8080

class Handler(http.server.SimpleHTTPRequestHandler):


    def do_POST(self):

        resp = {}
        if self.path == "/api/learn":
            try:
                print("Request : Learn")
                Data = (self.rfile.read(int(self.headers['content-length']))).decode('utf-8')
                jsondata = json.loads(Data)
                Name = jsondata['name']
            except:
                print("error parsing json data")
                resp = {"status":0}
                self.send_response(500)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(resp).encode())
                return
            res = face.learn(Name)
            resp = {"status":res}
            if res:
                self.send_response(200)
            else:
                self.send_response(500)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(resp).encode())
            return


        if self.path != "/api/upload":
            print("Request : Uplad image")
            resp = {"status":0}
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(resp).encode())
            return

        try:
            print("Downloading temp file...")
            Data = (self.rfile.read(int(self.headers['content-length'])))
            newFile = open("temp.jpg", "wb")
            newFile.write(Data)
            newFile.close()
            print("File saved")
        except:
            print("Error saveing file")
            resp = {"status":0}
            self.send_response(500)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(resp).encode())
            return

        resp = {"status":1}
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(resp).encode())

    def do_GET(self):
        # swich on path:


        if self.path == "/api/names":
            print("Request : Names")
            print("checking names...")
            resp = {"status":1,"list":face.getNames()}
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(resp).encode())
            return

        if self.path == "/api/test":
            print("Request : Test")
            print("Test Api : Application is running")
            resp = {"status":1}
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header("Location", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(resp).encode())
            return

        if self.path == "/api/check":
            print("Request : Check")
            r = face.Check()
            resp = {"status":0}
            if len(r) == 0:
                print("list was empty: Bad inmage")
                resp = {"status":0,"list":r}
                self.send_response(500)
            else:
                print("Sending list of labels...")
                resp = {"status":1,"list":r}
                self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(resp).encode())
            return
        http.server.SimpleHTTPRequestHandler.do_GET(self)







myserver =  socketserver.TCPServer(("", PORT), Handler)
print("\r\nServer Started")
url = "http://" + socket.gethostname() + ":" + str(PORT)
print("URL: " + url)
webbrowser.open(url)
myserver.serve_forever()