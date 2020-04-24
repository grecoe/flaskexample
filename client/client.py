import requests 
import json
import mimetypes

import os

'''
    Variables you must specify for your application.
'''
SOURCE_MACHINE_IP   = 'YOUR_FLASK_SERVER_IP' 

STORAGE_CONTAINER = 'YOUR_STORAGE_CONTAINER'
PAYLOAD_PATH = "VALID_FULL_PATH_ON_SERVER"
PAYLOAD_FILE = "FILE_NAME_TO_RETRIEVE"
'''
    Variables you must specify for your application.
'''



OUTPUT_PATH = 'retrieved'

SOURCE_REQUEST_TYPE = 'http'
SOURCE_MACHINE_PORT = 5000
SOURCE_ROUTE = 'retrieve'
SCORE_ROUTE = 'scoreresults'

REQUEST_SERVICE_URL = '{}://{}:{}/{}'.format(
    SOURCE_REQUEST_TYPE,
    SOURCE_MACHINE_IP,
    SOURCE_MACHINE_PORT,
    SOURCE_ROUTE
)

SCORE_SERVICE_URL = '{}://{}:{}/{}'.format(
    SOURCE_REQUEST_TYPE,
    SOURCE_MACHINE_IP,
    SOURCE_MACHINE_PORT,
    SCORE_ROUTE
)

POST_PAYLOAD_TYPE = "application/json"

REQUEST_IMAGE_PAYLOAD = {
    "path": PAYLOAD_PATH,
    "file": PAYLOAD_FILE
}    

REQUEST_IMAGE_PAYLOAD_STORAGE = {
    "storageContainer": STORAGE_CONTAINER,
    "file": PAYLOAD_FILE
}    

POST_PAYLOAD_HEADERS = {
    "Content-Type" : POST_PAYLOAD_TYPE
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
        print("RETRIEVE CALL STATUS -", request_result.status_code)

        if(request_result.status_code == 200):
            path = os.path.join(os.getcwd(), output_directory)
            if not os.path.isdir(path):
                os.makedirs(path)

            path = os.path.join(path, file_name)

            with open(path, "+wb") as retrieved_content:
                retrieved_content.write(request_result.content)

            return_value = path

    return return_value

def post_score(url, headers, payload):
    request_result = requests.post(url, headers=headers, json=payload)

    if request_result :
        print("SCORE CALL STATUS -", request_result.status_code)
        print("CONTENT", request_result.content)


downloaded = request_file(
    REQUEST_SERVICE_URL,
    POST_PAYLOAD_HEADERS,
    #REQUEST_IMAGE_PAYLOAD_STORAGE,
    REQUEST_IMAGE_PAYLOAD,
    OUTPUT_PATH,
    PAYLOAD_FILE
)

score_payload = {
    "some" : "value"
}


post_score(
    SCORE_SERVICE_URL,
    POST_PAYLOAD_HEADERS,
    score_payload
)
