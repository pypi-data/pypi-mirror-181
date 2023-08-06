import json
import requests

from datetime import datetime

from elna.exceptions import *

class API(object):
    """ Class used for communication with the SmartMeter API """

    # Client configuration
    __app_type = 'com.elna.smartmeter.client'
    __user_agent = 'Dart/2.10 (dart:io)'

    # Use a session to reuse one TCP connection instead of creating a new
    # connection for every call to the API
    __session = None
    __timeout = 4

    def __init__(self, hostname):
        """ Class constructor initializes all URL variables. """

        # Set connection specific details
        self.__hostname = hostname

        self.__url_base = 'http://' + self.__hostname

        # API endpoints
        self.__url_info         = self.__url_base + '/info'
        self.__url_meter_now    = self.__url_base + '/meter/now'
        self.__url_wlan_info    = self.__url_base + '/wlan/info'

        # Create a new session
        self.__session = requests.session()

    def __send_request(self, url, with_session_token=True, with_user_token=True, data_json=None, request_type='GET'):
        """ Send a GET or POST request to the server. """

        # Prepare the headers to be sent
        headers = {
            'Host': self.__hostname,
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'User-Agent': self.__user_agent,
        }

        # Only needed for POST requests
        if request_type == 'POST':
            headers['Content-Type'] = 'application/json'
            headers['Content-Length'] = str(len(data_json))

        # Perform the request and raise an exception
        # if the response is not OK (HTML 200)
        try:
            if request_type == 'GET':
                response = self.__session.get(url, headers=headers, timeout=self.__timeout)
            elif request_type == 'POST':
                response = self.__session.post(url, headers=headers, data=data_json, timeout=self.__timeout)
            response.raise_for_status()
        except requests.exceptions.ConnectionError:
            raise NewConnectionError(f"Failed to establish a new connection to '{url}'.")
            return None
        except requests.exceptions.ConnectTimeout:
            raise ConnectionTimeoutError(f"Connection to '{self.__hostname}' timed out after {str(self.__timeout)} seconds.")
            return None
        except:
            raise

        # Check HTTP response code
        if response.status_code == requests.codes.ok:
            return json.loads(response.content.decode('utf-8'))
        else:
            return None

    ######################
    # Public API methods #
    ######################

    @property
    def hostname(self):
        """ Property to keep track of the API servers hostname. """
        return self.__hostname

    def get_info(self):
        """ Get the general information about the device. """
        return self.__send_request(self.__url_info, request_type='GET')

    def get_meter_now(self):
        """ Get the power statistics of the device. """
        return self.__send_request(self.__url_meter_now, request_type='GET')

    def get_wlan_info(self):
        """ Get the WLAN information of the device. """
        return self.__send_request(self.__url_wlan_info, request_type='GET')

    def send_get(self, url):
        """ Send a custom POST request. """
        return self.__send_request(url, request_type='GET')

    def send_post(self, url, data):
        """ Send a custom POST request. """
        data_json = json.dumps(data, separators=(',', ':'))
        return self.__send_request(url, data_json=data_json, request_type='POST')
