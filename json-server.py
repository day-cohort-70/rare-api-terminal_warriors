import json
from http.server import HTTPServer
from nss_handler import HandleRequests, status

from views import update_user

class JSONServer(HandleRequests):

    def do_GET(self):
        pass

    def do_POST(self):
        pass

    def do_DELETE(self):
        pass

    def do_PUT(self):
        url = self.parse_url(self.path)
        content_len = int(self.headers.get('content-length', 0))
        request_body = self.rfile.read(content_len)
        request_body = json.loads(request_body)
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