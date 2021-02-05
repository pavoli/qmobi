import http.server
import socketserver


class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):

    def do_HEAD(self) -> None:
        

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/json')
        self.end_headers()
        self.wfile.write(b"Hello world!!!")


# Create an object of the above class
handler_object = MyHttpRequestHandler
my_server = socketserver.TCPServer(("", 8000), handler_object)

# Star the server
my_server.serve_forever()
