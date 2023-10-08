# kdc server

from http.server import BaseHTTPRequestHandler, HTTPServer
import json

CLIENT_KEY="CLIENT_KEY"
TGS_KEY="TGS_KEY"
SERVER_KEY="SERVER_KEY"
CT_SK="CT_SK"
CS_SK="CS_SK"

DATA_SERVER='http://localhost:8002'


class MyHandler(BaseHTTPRequestHandler):
    def SendRep(self, data):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = data
        self.wfile.write(bytes(json.dumps(response), "utf8"))
        return
        
    def AS_module(self,data):
        basic= data['basic']
        #query client info from db
        #Encry info with client key
        rep={'method':'AS', 'basic':CLIENT_KEY,'TGT': TGS_KEY, "CT_SK":CT_SK}
        self.SendRep(rep)
        return
    
    def TGS_module(self, data):
        #query from db to check if support the server
        server=data['server']
        if(server!= DATA_SERVER):
            return
        
        #verify client basic info
        basic=data['basic']
        if(basic != CT_SK):
            return
        
        TGT=data['TGT']
        if(TGT != TGS_KEY):
            return
        
        rep={'method':'TGS', 'basic':CT_SK,'ST':SERVER_KEY , "CS_SK":CS_SK}
        self.SendRep(rep)
        return
    
    def handle_data(self, data):
        method = data['method']
        if(method=="AS"):
            self.AS_module(data)
        elif(method=="TGS"):
            self.TGS_module(data)
        else:
            print("Can not support the method:", method)

        return
    

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)

        print('Received data from client:', data)
        self.handle_data(data)

        # self.send_response(200)
        # self.send_header('Content-type', 'application/json')
        # self.end_headers()
        # response = {'message': 'Received data: ' + str(data)}
        # self.wfile.write(bytes(json.dumps(response), "utf8"))
        return

def run(server_class=HTTPServer, handler_class=MyHandler):
    server_address = ('', 8001)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
