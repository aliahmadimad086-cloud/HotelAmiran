# server.py
# این فایل را با دستور python server.py اجرا کنید
from http.server import HTTPServer, SimpleHTTPRequestHandler
import urllib.request
import json

PORT = 8000
API_URL = "https://api.avalai.ir/v1/chat/completions"
API_KEY = "aa-3vWad2v3MDJQyheXOTSSNEmTBd9mtb13e4Ye6rOHvxD9wtCQ"

class ProxyHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/api/chat':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            # Forward request to AvalAI from backend (No CORS issues!)
            req = urllib.request.Request(
                API_URL,
                data=post_data,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {API_KEY}"
                }
            )
            try:
                with urllib.request.urlopen(req) as response:
                    res_body = response.read()
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(res_body)
            except urllib.error.HTTPError as e:
                err_body = e.read()
                self.send_response(e.code)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(err_body)
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
        else:
            self.send_error(404)

print(f"Server is running at http://localhost:{PORT}")
httpd = HTTPServer(('127.0.0.1', PORT), ProxyHandler)
httpd.serve_forever()
