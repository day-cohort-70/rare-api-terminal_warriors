#json-server.py
import json
from http.server import HTTPServer
from nss_handler import HandleRequests, status
from views.user import list_users,retrieve_user,delete_user

from views import create_user,login_user


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

        url = self.parse_url(self.path)

        request_body = JSONServer.parse_request_body(self)

        if url['requested_resource'] == 'users':

            response_body = create_user(request_body)

            return self.response(response_body, status.HTTP_201_SUCCESS_CREATED.value)
        
        if url['requested_resource'] == 'login':

            response_body = login_user(request_body)

            return self.response(response_body, status.HTTP_200_SUCCESS.value)


    def do_DELETE(self):
        url=self.parse_url(self.path)
        pk =url["pk"]

        if url["requested_resource"]=='users':
            if pk !=0:
                succesfully_deleted=delete_user(pk)
                if succesfully_deleted:
                    return self.response("",status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value)
                
                return self.response("requested resource not found", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)
        #pass

    def do_PUT(self):
        
       
        
        pass






# ----------------------------------------------
def main():
    host = ""
    port = 8000
    HTTPServer((host, port), JSONServer).serve_forever()


if __name__ == "__main__":
    main()