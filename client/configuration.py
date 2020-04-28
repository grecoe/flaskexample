
from enum import Enum

# HTTP Information
STANDARD_SOURCE_REQUEST_TYPE = 'http'
SECURE_SOURCE_REQUEST_TYPE = 'https'
DEFAULT_SOURCE_MACHINE_IP   = '127.0.0.1' 
DEFAULT_SOURCE_MACHINE_PORT = 5000



class FlaskRoute(Enum):
    RetrieveImage = 'retrieve'
    ScoreImage = 'scoreresults'


class FlaskRequestInformation:
    # Request URL Template
    URL_TEMPLATE = '{}://{}:{}/{}'
    DEFAULT_PAYLOAD_TYPE = "application/json"
    
    def __init__(self):
        pass
    
    @staticmethod
    def get_json_content_headers():
        return {
                 "Content-Type" : FlaskRequestInformation.DEFAULT_PAYLOAD_TYPE
            }

    @staticmethod
    def get_request_url(
        use_ssl=True, 
        server_ip=DEFAULT_SOURCE_MACHINE_IP,
        server_port=DEFAULT_SOURCE_MACHINE_PORT, 
        flask_route=FlaskRoute.RetrieveImage):

        return FlaskRequestInformation.URL_TEMPLATE.format(
            SECURE_SOURCE_REQUEST_TYPE if use_ssl else STANDARD_SOURCE_REQUEST_TYPE,
            server_ip,
            str(server_port),
            flask_route.value
        )