import requests
import credentials
from requests.auth import HTTPBasicAuth

AUTH_ID = "Hackathon.CITM.Hamilton"
AUTH_PASS = "Wm,yb&G`KB\\2}d<s"
BBOX = "-90:-180,90:180"


class Pipe:
    def __init__(self):
        self.tenant = credentials.credentials["City"]
        self.token = None

    def get_tenant(self):
        return self.tenant

    def fetch_token(self):
        self.token = requests.get("https://auth.aa.cityiq.io/oauth/token?grant_type=client_credentials",
                auth=HTTPBasicAuth(AUTH_ID, AUTH_PASS)).json()['access_token']

    def set_token(self, token):
        self.token = token

    def get_token(self):
        return self.token

    def fetch_metadata(self, zone):
        # Zone takes parking, traffic, pedestrian, bicycle.
        headers = {'Authorization': 'Bearer ' + self.token, 'Predix-Zone-Id': self.tenant[zone]}
        return requests.request("GET", self.tenant["metadata"] + "/assets/search", headers=headers).json()['content']

    def fetch_pedestrian_data(self, uid, start, end):
        zone = self.tenant['pedestrian']

        query = {
            "pageSize": 100,
            "eventType": 'PEDEVT',
            "startTime": start,
            "endTime": end
        }

        headers = {'Authorization': 'Bearer ' + self.token, 'Predix-Zone-Id': zone}
        return requests.request("GET", self.tenant["event"]+"/assets/" + uid + "/events", headers=headers, params=query).json()['content']

    def fetch_bike_data(self, uid, start, end):
        zone = self.tenant['BICYCLE']

        query = {
            "pageSize": 100,
            "eventType": 'BICYCLE',
            "startTime": start,
            "endTime": end
        }
        headers = {'Authorization': 'Bearer ' + self.token, 'Predix-Zone-Id': zone}
        return requests.request("GET", self.tenant["event"]+"/assets/" + uid + "/events", headers=headers, params=query).json()['content']
    
    def fetch_temperature_data(self, uid, start, end):
        zone = self.tenant['TEMPERATURE']

        query = {
            "pageSize": 100,
            "eventType": 'TEMPERATURE',
            "startTime": start,
            "endTime": end 
        }
        headers = {'Authorization': 'Bearer ' + self.token, 'Predix-Zone-Id': zone}
        return requests.request("GET", self.tenant["event"]+"/assets/" + uid + "/events", headers=headers, params=query).json()['content']


if __name__ == '__main__':
    pass
