#json-server.py
import json
from http.server import HTTPServer
from nss_handler import HandleRequests, status
from views.user import list_users,retrieve_user



class JSONServer(HandleRequests):

    def do_GET(self):
        """Handle GET requests from a client"""

        response_body = ""
        url = self.parse_url(self.path)
        
        if url["requested_resource"] == "users":
            if url["pk"] != 0:
                response_body = retrieve_user(url["pk"])
                return self.response(response_body, status.HTTP_200_SUCCESS.value)
            
            response_body = list_users()
            return self.response(response_body, status.HTTP_200_SUCCESS.value)
        
        else:
            return self.response("",status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)

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