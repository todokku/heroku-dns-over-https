import http.server
import socketserver
import sys
from urllib.parse import urlparse
from urllib.parse import parse_qs
PORT = int(sys.argv[1])

def handleDns(path):
	path=urlparse(path)
	query=parse_qs(path.query)
	path=path.path
	qclass,qquery="IN","SOA"
	qclass=query.get('c',qclass)
	qclass=query.get('C',qclass)
	qquery=query.get('q',qquery)
	qquery=query.get('Q',qquery)
	print(query)
	print(qquery,'q')
	print(qclass,'c')
	qclass,qquery=qclass.upper(),qquery.upper()
	return path+"\t"+qclass+"\t"+qquery

class SimpleHandler(http.server.BaseHTTPRequestHandler):
	def do_HEAD(self):
		self.send_response(200)
		self.send_header("Content-type", "text/plain")
		self.end_headers()
	def do_GET(self):
		self.send_response(200)
		self.send_header("Content-type", "text/plain")
		self.end_headers()
		self.wfile.write(handleDns(self.path).encode("utf-8"))
		self.wfile.close()
	def do_POST(self):
		self.send_response(400)
		self.send_header("Content-type", "text/plain")
		self.end_headers()
		self.wfile.write("400 Bad Request".encode("utf-8"))
		self.wfile.close()
try:
	server = http.server.HTTPServer(('0.0.0.0',PORT),SimpleHandler)
	print('Started http server')
	server.serve_forever()
except KeyboardInterrupt:
	print('^C received, shutting down server')
	server.socket.close()
