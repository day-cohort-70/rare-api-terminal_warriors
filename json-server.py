#json-server.py
import json
from http.server import HTTPServer
from nss_handler import HandleRequests, status
from views.user import list_users,retrieve_user

from views import create_user,login_user, update_user, delete_user
from views import list_categories, retrieve_category

class JSONServer(HandleRequests):

    def do_GET(self):

        response_body = ""
        url = self.parse_url(self.path)

        if url["requested_resource"] == "users":
            if url["pk"]:
                response_body = retrieve_user(url["pk"])
            else:
                response_body = list_users()

        if url["requested_resource"] == "categories":
            if url["pk"]:
                response_body = retrieve_category(url["pk"])
            else:
                response_body = list_categories()

        if response_body == 'id not found':
            return self.response("", status.HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA.value)
        elif response_body:
            return self.response(response_body, status.HTTP_200_SUCCESS.value)
        else:
            return self.response("",status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)

    def do_POST(self):

        response_body=""
        url = self.parse_url(self.path)
        request_body = JSONServer.parse_request_body(self)

        if url['requested_resource'] == 'login':
            response_body = login_user(request_body)
            return self.response(response_body, status.HTTP_200_SUCCESS.value)

        if url['requested_resource'] == 'users':
            response_body = create_user(request_body)
            return self.response(response_body, status.HTTP_201_SUCCESS_CREATED.value)


        return self.response("Not found", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)


    def do_DELETE(self):
        url=self.parse_url(self.path)
        pk =url["pk"]

        if url["requested_resource"]=='users':
            if pk !=0:
                succesfully_deleted = delete_user(pk)
                if succesfully_deleted:
                    return self.response("",status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value)

                return self.response("requested resource not found", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)


    def do_PUT(self):
        url = self.parse_url(self.path)
        request_body = JSONServer.parse_request_body(self)
        resource_type = url["requested_resource"]
        pk = url["pk"]

        if resource_type in ["users", "posts", "tags", "comments"]:
            if pk != 0:
                response_body = self.update_resource(resource_type, pk, request_body)
                if response_body:
                    return self.response("", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value)
            return self.response("Request resource not found", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)
        return self.response("Not found", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)


    def update_resource(self, resource_type, pk, request_body):
        if resource_type == "users":
            return update_user(pk, request_body)
        elif resource_type == "posts":
            return False  # Replace with update_posts
        elif resource_type == "tag":
            return False  # Replace with update_tags
        elif resource_type == "comment":
            return False  # Replace with update_comment
        else:
            return False  # Resource type not supported






# ----------------------------------------------
def main():
    host = ""
    port = 8000
    HTTPServer((host, port), JSONServer).serve_forever()


if __name__ == "__main__":
    main()