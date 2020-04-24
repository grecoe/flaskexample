# Test Flask Application

This code creates a Flask server and also provides a client in which to exercise the code there. 

## Flask Server

### Prerequisites
1. Create a conda environment
```
    > conda env create -f environment.yml
```
2. Activate the environment
```
    > conda activate TestFlask
```
3. Set flask path
```
    > set FLASK_APP=server.py
```
4. Navigate to the /server directory to run the server on local host only. 
    - This will allow you to test the client from the same box. 
    ```
        > flask run
    ```
    - This will allow you to run the server open to the world. In this case, you probably want to creat a newtwork security rule that opens port 5000 ONLY to your external machine thereby blocking all other traffic to the port.  
    ```
        > python server.py
    ```


### Overview
The flask server has two APIs that are exposed.

#### server_url:5000/retrieve

|Method|Payload|
|------|-------|
|POST|JSON object that identifies either an Azure Blob file or a local file.<br><br>Payload is one of the following:<br><br><b>Azure Storage</b><br><br>{<br>'storageContainer': 'container_name',<br>'file':'blob_file'<br>}<br><br><b>Local File</b><br><br>{<br>'path': 'container_name',<br>'file':'blob_file'<br>}

<b>NOTE:</b>
- path for a local file is the full disk path of the file. 
- file for Azure Storage is the full blob path after the container.
- If you are using Azure Blob Storage as a source, you must provide the storage connection string in the variable AZURE_STORAGE_CONNECTION_STRING. 

The return value of this call shold be 200 and the result will have the file content that was requested. 

#### server_url:5000/scoreresults

|Method|Payload|
|------|-------|
|POST|JSON object of your choice.|

It's literally just a stub that prints out the JSON payload. 


## Client

### Prerequisite
- Flask server is running
- Python 3.6 or higher
- IP address of the target machine.
- Network allows the server machine to be reached from the client machine. 

### Overview
The client will exercise the endpoints on the server. 

Both the server code and client code can be run on the same machine. 

You must update the following variables to exercise the client against your server.

|Variable|Value|
|--------|-----|
|SOURCE_MACHINE_IP|The IP address of the server machine.|
|PAYLOAD_PATH|If using a local file, this must be a full disk path to the directory holding the file to retrieve.|
|PAYLOAD_FILE|If retrieving a local file to the server, the file name.<br><br>If retrieving sa blob file from storage, this is the blob name.|
|STORAGE_CONTAINER|If you are retrieving a blob, this is the container name to retrieve from.|
|Line 88|Modify to make the request (local or Azure Storage) that you want.|

The client code will 
1. Call the retrieve API to get a file from the client. 
2. Regardless of what it retrieves, it will call the scoreresult API on the server. 