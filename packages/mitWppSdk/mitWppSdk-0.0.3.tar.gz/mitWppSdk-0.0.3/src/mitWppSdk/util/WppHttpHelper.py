from requests import post
import requests.exceptions as reqx

from mitWppSdk.WppException import WppException

class WppHttpHelper:
    def __init__(self, endpoint: str) -> None:
        self._endpoint = endpoint

    def post(self, message: str) -> str:
        response = ""
        try:
            response = post(self._endpoint, data=message, 
                headers={"Content-Type": "application/x-www-form-urlencoded", 
                    "Content-Length": str(len(message.encode("utf-8")))})
        except reqx.RequestException as e:
            raise WppException from e
        response.raise_for_status()
        return response.content.decode("utf-8")