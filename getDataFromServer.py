"""
This script is used to get data from the pythonanywhere server
"""
# imports
import requests as rq
import json
import pandas as pd
import matplotlib.pyplot as plt

uuid = 1
network_name = "fakeNetwork"
network_password = "I was agent orange that was me"

def testGetAllData():
    obj = {
        "uuid": uuid,
        "network name": network_name,
        "network password": network_password
    }
    resp = rq.post(url="https://www.agripod.co.uk/getAllData/", data=obj)
    resp = json.loads(resp.content.decode("utf-8"))
    resp = pd.DataFrame.from_records(resp)
    print
    del resp["device_id"], resp["network_id"], resp["uuid"]
    df = resp.reindex(columns=["id", "humidity", "moisture", "temperature"])
    return df

def plotData(df:pd.DataFrame,column:str,scatter=False) -> None:
    """
    this function plots a given column from a pandas dataframe
    :param df: dataframe
    :param column: column name
    :param scatter: bool scatter (or plot)
    :return: None
    """
    plt.title(column + " data")
    if not scatter:
        plt.plot(range(len(df)), df[column])
    else:
        plt.scatter(range(len(df)), df[column])
    plt.show()
if __name__ == '__main__':
    df = testGetAllData()
    plotData(df, "moisture", True)