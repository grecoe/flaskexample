import os
import requests 
import json
import mimetypes
from configuration import FlaskRequestInformation, FlaskRoute

'''
    Variables you must specify for your application.
    STORAGE_CONTAINER - The storage container that has the file
                        being requested. 
    PAYLOAD_PATH      - The local file directory on the server 
                        that has the file being requested.
    REQUESTED_FILE_NAME - The actual file or blob name that is 
                        being requested.

    DOWNLOAD_DIRECTORY_PATH - The directory in which to place retrieved
                              files. 
'''
STORAGE_CONTAINER = 'YOUR_STORAGE_CONTAINER'
PAYLOAD_PATH = "C:\\Users\\grecoe\\Pictures"
REQUESTED_FILE_NAME = "dan.jpg"

DOWNLOAD_DIRECTORY_PATH = 'retrieved'
'''
    Variables you must specify for your application.
'''

REQUEST_IMAGE_PAYLOAD = {
    "path": PAYLOAD_PATH,
    "file": REQUESTED_FILE_NAME
}    

REQUEST_IMAGE_PAYLOAD_STORAGE = {
    "storageContainer": STORAGE_CONTAINER,
    "file": REQUESTED_FILE_NAME
}    

def request_file(url, headers, payload, output_directory, file_name):
    """
        Make the request to load a file
    """

    return_value = None

    request_result = requests.post(url, headers=headers, json=payload)

    if request_result :
        # We have some result, so lets print a little bit out. Remember, we know what the 
        # backend code looks like so we know what to look for in the body. 
        if(request_result.status_code == 200):
            path = os.path.join(os.getcwd(), output_directory)
            if not os.path.isdir(path):
                os.makedirs(path)

            path = os.path.join(path, file_name)

            with open(path, "wb") as retrieved_content:
                retrieved_content.write(request_result.content)

            return_value = path
        else:
            print("Request call failed : {}".format(request_result.status_code))

    return return_value

def post_score(url, headers, payload):
    request_result = requests.post(url, headers=headers, json=payload)

    return_response = None
    if request_result :
        return_response = request_result.status_code
        print("SCORE CONTENT", request_result.content)

    return return_response


# Header types for all calls.....
json_content_header = FlaskRequestInformation.get_json_content_headers()

downloaded = request_file(
    FlaskRequestInformation.get_request_url(use_ssl=False),
    json_content_header,
    #REQUEST_IMAGE_PAYLOAD_STORAGE,
    REQUEST_IMAGE_PAYLOAD,
    DOWNLOAD_DIRECTORY_PATH,
    REQUESTED_FILE_NAME
)

print("Requested File Payload Location:")
print(downloaded)


# Send anything into score because we don't really know 
# what would be needed at this point. 
score_payload = {
    "some" : "value"
}

response = post_score(
    FlaskRequestInformation.get_request_url(use_ssl=False, flask_route=FlaskRoute.ScoreImage),
    json_content_header,
    score_payload
)

print("\nScore response : {}".format(response))