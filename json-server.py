import json
from http.server import HTTPServer
from nss_handler import HandleRequests, status

from views import create_user,login_user


class JSONServer(HandleRequests):

    def do_GET(self):
        pass

    def do_POST(self):

        url = self.parse_url(self.path)

        request_body = JSONServer.parse_request_body(self)

        if url['requested_resource'] == 'users':

            response_body = create_user(request_body)

            return self.response(response_body, status.HTTP_201_SUCCESS_CREATED.value)
        
        if url['requested_resource'] == 'login':

            response_body = login_user(request_body)

            return self.response(response_body, status.HTTP_200_SUCCESS.value)


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