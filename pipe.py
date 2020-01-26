import requests
import credentials
import os
from requests.auth import HTTPBasicAuth
from tinydb import TinyDB, Query, where

AUTH_ID = "Hackathon.CITM.Hamilton"
AUTH_PASS = "Wm,yb&G`KB\\2}d<s"
BBOX = "-90:-180,90:180"


if not os.path.exists("../delta_hacks/db.json"):
    db = TinyDB("../delta_hacks/db.json")
    db.insert({"item": "ped", "count": 0, "history": []})
db = TinyDB("../delta_hacks/db.json")
dbquery = Query()

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
            "pageSize": 10,
            "eventType": 'PEDEVT',
            "startTime": start,
            "endTime": end
        }

        headers = {'Authorization': 'Bearer ' + self.token, 'Predix-Zone-Id': zone}
        response = requests.request("GET", self.tenant["event"]+"/assets/" + uid + "/events", headers=headers, params=query).json()['content']
        for item in response:
            if item['measures']['pedestrianCount'] != 0.0:
                old = int(db.search(dbquery.item == "ped")[0]['count'])
                db.update({"count": old + item['measures']['pedestrianCount']}, where("item") == 'ped')
            old = db.search(dbquery.item == "ped")[0]['history']
            old.append({"time": item['timestamp'], "total": item['measures']['pedestrianCount']})
            db.update({"history": old})
        return response



if __name__ == '__main__':
    pipe = Pipe()
    pipe.fetch_token()
    # print(pipe.fetch_metadata('pedestrian'))
    response = pipe.fetch_pedestrian_data("f6057765-ae16-4b8a-b0b8-c48de3b193c6", 1579937852293, 1580024252293)
    u = Query()
    print(db.search(u.item == "ped")[0]['history'])
