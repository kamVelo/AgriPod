"""
This script is used to get data from the pythonanywhere server
"""
# imports
import requests as rq
import json
import pandas as pd


uuid = 1
network_name = "fakeNetwork"
network_password = "I was agent orange that was me"

def testGetAllData():
    obj = {
        "uuid": uuid,
        "network name": network_name,
        "network password": network_password
    }
    resp = rq.post(url="http://127.0.0.1:5000/getAllData/", data=obj)
    resp = json.loads(resp.content.decode("utf-8"))
    resp = pd.DataFrame.from_records(resp)
    print
    del resp["device_id"], resp["network_id"], resp["uuid"]
    df = resp.reindex(columns=["id", "humidity", "moisture", "temperature"])
    print(df)

testGetAllData()