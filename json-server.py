import json
from http.server import HTTPServer
from nss_handler import HandleRequests, status



class JSONServer(HandleRequests):

    def do_GET(self):
        pass

    def do_POST(self):
        pass

    def do_DELETE(self):
        pass

    def do_PUT(self):
        pass






# ----------------------------------------------
def main():
    host = ""
    port = 8000
    HTTPServer((host, port), JSONServer).serve_forever()


if __name__ == "__main__":
    main()