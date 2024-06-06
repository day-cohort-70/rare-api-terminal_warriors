#json-server.py
import json
from http.server import HTTPServer
from nss_handler import HandleRequests, status

from views import list_users,retrieve_user, create_user,login_user, update_user, delete_user
from views import list_categories, retrieve_category, create_category,delete_category, update_category
from views import filteredAllPosts
from views import create_tag, list_tags,delete_tag,update_tag
from views import list_post_tags, retrieve_post_tag, create_post_tag, delete_post_tag, update_post_tag


class JSONServer(HandleRequests):

    def do_GET(self):

        url = self.parse_url(self.path)
        requested_resource = url["requested_resource"]
        pk = url["pk"]
        response_body = ""


        if requested_resource == "users":
            if pk != 0:
                response_body = retrieve_user(pk)
            else:
                response_body = list_users(url)

        if requested_resource == "categories":
            if pk != 0:
                response_body = retrieve_category(pk)
            else:
                response_body = list_categories()

        if requested_resource == "tags":
            response_body = list_tags()


        if requested_resource == "posts":
            response_body = filteredAllPosts(url)

        if requested_resource == "post_tags":
            if pk != 0:
                response_body = retrieve_post_tag(pk)
            else:
                response_body = list_post_tags(url)

        if response_body == 'id not found':
            return self.response("", status.HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA.value)
        if response_body:
            return self.response(response_body, status.HTTP_200_SUCCESS.value)
        
        return self.response("",status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)


    def do_POST(self):

        url = self.parse_url(self.path)
        request_body = self.parse_request_body()
        requested_resource = url["requested_resource"]
        response_body=""

        # JSON.dumps() is being invoked in each function
        if requested_resource == 'login':
            response_body = login_user(request_body)
            return self.response(response_body, status.HTTP_200_SUCCESS.value)

        if requested_resource == 'users':
            response_body = create_user(request_body)

        if requested_resource == 'categories':
            response_body = create_category(request_body)

        if requested_resource == 'tags':
            response_body = create_tag(request_body)

        if requested_resource == 'post_tags':
            response_body = create_post_tag(request_body)

        if response_body:
            return self.response(response_body, status.HTTP_201_SUCCESS_CREATED.value)

        return self.response("Not found", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)

    
    def do_DELETE(self):
        url=self.parse_url(self.path)
        requested_resource = url["requested_resource"]
        pk =url["pk"]
        succesfully_deleted = False

        if requested_resource =='users':
            if pk:
                succesfully_deleted = delete_user(pk)

        if requested_resource =='categories':
            if pk:
                succesfully_deleted = delete_category(pk)

        if url["requested_resource"]=='tags':
            if pk:
                succesfully_deleted = delete_tag(pk)

        if url["requested_resource"]=='post_tags':
            if pk:
                succesfully_deleted = delete_post_tag(pk)

        if succesfully_deleted:
            return self.response("",status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value)

        return self.response("requested resource not found", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)


    def do_PUT(self):
        url = self.parse_url(self.path)
        request_body = self.parse_request_body()
        requested_resource = url["requested_resource"]
        pk = url["pk"]
        response_body = ""

        if requested_resource == "users":
            if pk != 0:
                response_body = update_user(pk, request_body)

        if requested_resource == "categories":
            if pk != 0:
                response_body = update_category(pk, request_body)

        if requested_resource == "tags":
            if pk != 0:
                response_body = update_tag(pk, request_body)

        if requested_resource == "post_tags":
            if pk != 0:
                response_body = update_post_tag(pk, request_body)

        if response_body:
            return self.response(response_body, status.HTTP_201_SUCCESS_CREATED.value)

        return self.response("Not found", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)



  

# ----------------------------------------------
def main():
    host = ""
    port = 8000
    HTTPServer((host, port), JSONServer).serve_forever()


if __name__ == "__main__":
    main()

