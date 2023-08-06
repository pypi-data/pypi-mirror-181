import dateutil.parser
import requests

from datetime import datetime, timezone

class MoxfieldAuth(requests.auth.AuthBase):

    def __login(self):
        payload = {
            'userName': self.__username, 
            'password': self.__password
        }

        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Content-Type': 'application/json'
        }

        r = requests.post('https://api2.moxfield.com/v2/account/token', json=payload, headers=headers)
        r.raise_for_status()

        resp = r.json()
        self.__update(resp)

    def __refresh(self):
        payload = {
            'refreshToken': self.refresh_token
        }

        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Content-Type': 'application/json'
        }

        r = requests.post('https://api2.moxfield.com/v2/account/token/refresh', json=payload, headers=headers)

        if r.status_code != 200:
            self.__login()
        else:
            resp = r.json()
            self.__update(resp)

    def __update(self, ref_json):
        self.access_token = ref_json['access_token']
        self.refresh_token = ref_json['refresh_token']
        self.expiration = dateutil.parser.parse(ref_json['expiration'])

    def __init__(self, username: str, password: str):
        self.access_token = None
        self.refresh_token = None
        self.expiration = None
        self.__username = username
        self.__password = password

    def __call__(self, r):
        if self.expiration is None:
            self.__login()

        elif datetime.now(timezone.utc) > self.expiration:
            self.__refresh()

        r.headers['Authorization'] = f'Bearer {self.access_token}'
        r.headers['Origin'] = 'https://www.moxfield.com'
        r.headers['Referrer'] = 'https://www.moxfield.com'
        return r