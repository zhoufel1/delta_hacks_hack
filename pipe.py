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
        self.bbox = "-90:-180,90:180"

    def get_tenant(self):
        return self.tenant

    def fetch_token(self):
        self.token = requests.get("https://auth.aa.cityiq.io/oauth/token?grant_type=client_credentials",
                auth=HTTPBasicAuth(AUTH_ID, AUTH_PASS)).json()['access_token']

    def set_token(self, token):
        self.token = token

    def get_token(self):
        return self.token

    def get_bbox(self):
        return self.bbox

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


if __name__ == '__main__':
    pipe = Pipe()
    pipe.fetch_token()
    print(pipe.fetch_metadata("pedestrian"))
    print(pipe.fetch_pedestrian_data("f6057765-ae16-4b8a-b0b8-c48de3b193c6", "1579935736167", "1580022136167"))
