"""
    Simple Flask app to retrieve a file from either the local machine or 
    from an Azure Blob Storage account. 

    Pre-requisites:
        Create conda environment on machine to host service
        Activate environment
        From the directory holding the program.py, execute
            > flask run 

    ****************************************************************
    Call Type: POST
    Route: url/retrieve
    ****************************************************************

        Payload is JSON and in the form:

            Azure Storage - Set the AZURE_STORAGE_CONNECTION_STRING variable to 
            your connection string on your account. 

            Provide the container and blob name as the body.

            {
                "storageContainer": 'covid19',
                "file: "dan.jpg" | "dan.jpg"
            }    

        OR
            Local file, provide the full path of the file and the file name as the body.

            {
                "path": "C:\\gitrepogrecoe\\KubernetesExampleFlask\\flask\\data",
                "file: "dan.jpg"
            }


    ****************************************************************
    Call Type: POST
    Route: url/scoreresults
    ****************************************************************

"""
import os
import glob
import json
import mimetypes
from app import app
from flask import request
from flask import send_file
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

'''
    Variables you MUST define (if using Azure Stoarge)
'''
AZURE_STORAGE_CONNECTION_STRING = "YOUR_AZURE_STORAGE_ENDPOINT"
'''
    Variables you MUST define (if using Azure Stoarge)
'''


CONTAINER_KEY = 'storageContainer'
PATH_KEY = "path"
FILE_KEY = "file"

BLOB_DOWNLOAD_PATH = "downloads"

def _flush_temp_file():
    """
        Clear directory where blob files are downloaded to if exists. 
    """
    global BLOB_DOWNLOAD_PATH
    try:
        dirPath = os.path.join(os.getcwd(), BLOB_DOWNLOAD_PATH)
        print("PTH", os.getcwd())
        print("DIR", dirPath)
        if os.path.isdir(dirPath):
            print("CLEAR PATH")
            files = glob.glob(dirPath)
            for f in files:
                os.remove(f)
    except Exception as ex:
        print(str(ex))

def _retrieve_local_file(directory, file_name, mime_type):
    """
        Function to retrieve a local file 
        directory - Full path local directory
        file_name - File to retrieve
    """
    return_value = None

    # Next, if we have a mime type, ensure that the file exists
    requested_file = os.path.join(directory, file_name)
    if os.path.isfile(requested_file):
        return_value = send_file(requested_file, mimetype=mime_type)

    return return_value

def _retrieve_blob_file(container_name, blob_name, mime_type):
    """
        Function to retrieve a blob file 
        container_name - Container holding the file
        file_name - Blob name with whatever path you need.
    """
    global AZURE_STORAGE_CONNECTION_STRING
    global BLOB_DOWNLOAD_PATH
    
    return_value = None
    try:
        download_path = os.path.join(os.getcwd(), BLOB_DOWNLOAD_PATH)
        if not os.path.isdir(download_path):
            os.makedirs(download_path)
        
        download_path = os.path.join(download_path, blob_name)

        blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

        with open(download_path, "wb") as download_file:
            download_file.write(blob_client.download_blob().readall())

        if os.path.isfile(download_path):
            return_value = send_file(download_path, mimetype=mime_type)

    except Exception as ex:
        print(str(ex))

    return return_value

@app.route('/retrieve', methods = ['POST'])
def retrieve():
    """
        Retrieves either a blob storafe file or local file depending on the 
        input. 

        Mime type must be discernable. 
        File must exist.

        If both container and path are supplied, Azure Blob is the default. 
    """
    global PATH_KEY
    global CONTAINER_KEY
    global FILE_KEY

    # Clear out any downloaded files
    _flush_temp_file()

    # Request MUST be JSON
    response = "Invalid Request"
    if request.is_json:
        content = request.get_json(silent=True)

        mime_type = None

        # File must exist for either local or blob
        if FILE_KEY in content.keys():
            file_parts = os.path.splitext(content[FILE_KEY])

            if len(file_parts) == 2:
                if file_parts[1] in mimetypes.types_map:
                    mime_type = mimetypes.types_map[file_parts[1]]
                else:
                    response = "Mime type not found for {}".format(content[FILE_KEY])

        # If file exists and mime type valid, continue.
        # Presence of CONTAINER_KEY will always use blob storage
        if mime_type:
            if  CONTAINER_KEY in content.keys():
                print("STORAGE REQUEST")
                print(content[CONTAINER_KEY], content[FILE_KEY])

                response = _retrieve_blob_file(content[CONTAINER_KEY], content[FILE_KEY], mime_type)
                if not response:
                    response = "Blob not found/error {}".format(content[FILE_KEY])

            elif PATH_KEY in content.keys(): 
                print("LOCAL FILE REQUEST")
                print(content[PATH_KEY], content[FILE_KEY])

                response = _retrieve_local_file(content[PATH_KEY], content[FILE_KEY], mime_type)
                if not response:
                    response = "File not found {}".format(content[FILE_KEY])
    
    return response


@app.route('/scoreresults', methods = ['POST'])
def score():
    if request.is_json:
        content = request.get_json(silent=True)
        
        print("Scoring Result:")
        print(json.dumps(content, indent=4))

    return "Thanks"