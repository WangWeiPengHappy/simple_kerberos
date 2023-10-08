# server.py
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
SERVER_KEY="SERVER_KEY"
g_cs_sk=""
class MyHandler(BaseHTTPRequestHandler):
    def SendRep(self, data):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = data
        self.wfile.write(bytes(json.dumps(response), "utf8"))
        return
    
    def verify_client(self, data):
        ST=data['ST']
        if(ST != SERVER_KEY):
            return False
        return True
    
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)

        print('Received data from client:', data)
        ret = self.verify_client(data)
        if(ret == False):
            return
        CS_SK=data['basic']
        rep={'method':'CS', 'basic':CS_SK, 'message':"I am server"}
        self.SendRep(rep)

        # self.send_response(200)
        # self.send_header('Content-type', 'application/json')
        # self.end_headers()
        # response = {'message': 'Received data: ' + str(data)}
        # self.wfile.write(bytes(json.dumps(response), "utf8"))
        return

def run(server_class=HTTPServer, handler_class=MyHandler):
    server_address = ('', 8002)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
