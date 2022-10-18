import logging
import json
import pathlib
import requests
import time
import os
from datetime import datetime

from lib.Token_info import Token_info

class Syncer:
    """ Class SYNCER handles the communnication between Trakt API """

    def __init__(self, test: bool = False):
        """
        Parameters
        -----------
        test : bool
            if true will commuicate to test URL
        """
        logging.info(f"Syncer started in testing mode: {test}")
        
        # self.WAIT_TIME = 1 # Time to wait between calls
        self.client_id = ""
        self.client_secret = ""
        self.token_info = Token_info()
        self.PATH = str(pathlib.Path(__file__).parent.resolve()) + "/../"

        self.api_endpoint = "https://api.trakt.tv/"
        if test: self.api_endpoint = "https://api-staging.trakt.tv"

        self.__read_config()

        if self.client_id == "INSERT ID": 
            logging.error("Missing client id in config.json")
            exit("Missing client id in config.json")
        if self.client_secret == "INSERT SECRET": 
            logging.error("Missing client secret in config.json")
            exit("Missing client secret in config.json")
        
        logging.info("Syncer Initialized")


# --------------------- AUTHENTICATION --------------------------------
    def authenticate(self):
        """
        Starts the authentication process, the app retrieves the code and wait until the user
        authorizes the app or the code expires.
        
        The objective of this function is to obtain the token used to authenticate in the API calls
        """
        
        # If we already have a valid token, i.e., with more than a day before expiration date, we skip authentication
        if self.token_info.has_values is True:
            now = int(time.time())
            expire_date = self.token_info.created_at + self.token_info.expires_in

            if expire_date - now >= 24*60*60:
                logging.info(f"Skipping authentication, valid token expires at {datetime.fromtimestamp(expire_date)}")
                return
            else:
                #TODO Call for a token refresh
                None

        (device_code, interval, expires_in) = self.__get_code()
        now = 0
        
        while now < expires_in:
            print("Waiting for authentication...", end="\r")
            time.sleep(interval)
            ret, token = self.__get_token(device_code)
            if ret: 
                self.token_info.from_dict(token)
                break
            now += interval
        
        self.__write_config()
        logging.info("Authenticated")

    def __get_code(self): 
        """Interacts with API Call 'GET CODE', returning the Code for the get_token function"""
        
        url = self.api_endpoint + "/oauth/device/code"
        header = {"Content-Type": "application/json"}
        data = {"client_id": self.client_id}

        resp = requests.post(url= url, headers= header, json= data)
        if resp.status_code != 200:
            logging.error(f"Error during http request in __get_code: status {resp.status_code}")
            exit("There was an Error during authentication #GET-CODE-ERROR-{}\nRetry Later!".format(resp.status_code))

        content = resp.json()
        print("==================================================================================================")
        print("Please Authorize the App by inserting: '{}' at the following link: {} ".format(content["user_code"], content["verification_url"]))
        print("==================================================================================================")

        return (content["device_code"], content["interval"], content["expires_in"])
    
    def __get_token(self, device_code: str):
        """Simply Interacts with API Call 'GET TOKEN', """

        url = self.api_endpoint + "/oauth/device/token"
        header = {"Content-Type": "application/json"}
        data = {
            "code": device_code,
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        resp = requests.post(url= url, headers= header, json= data)

        if resp.status_code == 400:
            return (False, {})
        elif resp.status_code != 200:
            logging.error(f"Error during http request in __get_token: status {resp.status_code}")
            exit("There was an Error during authentication #GET-TOKEN-ERROR-{}\nRetry Later!".format(resp.status_code))

        return (True, resp.json())
# ---------------------------------------------- REAL STUFF ----------------------------------------------------

    def add_to_history(self, data: dict):
        """
        It adds a dictionary of films/episodes to the history, returns the status code of the request:
        201 if successful, otherwise it didn't succeded

        Params
        --------------
        data : dict
            a dictionary with the tv shows episodes or movies to add to trakt history
        """
        url = self.api_endpoint + "/sync/history"
        header = {
            "Content-Type": "application/json",
            "Authorization": f"{self.token_info.token_type} {self.token_info.access_token}",
            "trakt-api-version": "2",
            "trakt-api-key": f"{self.client_id}"
        }

        resp = requests.post(url= url, headers= header, json= data)
        logging.debug(f"Status: {resp.status_code}, Content: {resp.json()}")

        return (resp, resp.json())
    
    def add_ratings(self):
        #TODO
        None

    def add_to_watchlist(self):
        #TODO
        None

# ---------------------------------------------- UTILS ----------------------------------------------------
    def __read_config(self):
        
        if not os.path.exists(self.PATH + "config.json"):
            # If there isn't any config.json, it creates one
            config = {
                "client_id": "INSERT ID",
                "client_secret": "INSERT SECRET"
            }
            with open(self.PATH + "config.json", "w") as file:
                json.dump(config, file)


        with open(self.PATH + "config.json") as file: 
            jdump = json.load(file)
            self.client_id = jdump["client_id"]
            self.client_secret = jdump["client_secret"]

            if "token_info" in jdump:
                self.token_info.from_dict(jdump["token_info"])
                logging.debug("Retrived token info from config")
        
    
    def __write_config(self):

        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "token_info": self.token_info.to_dict()
        }

        with open(self.PATH + "config.json", "w") as file:
            json.dump(data, file, indent=4)
        
        logging.debug("'config.json saved'")
    


