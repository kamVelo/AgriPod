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

    del resp["device_id"], resp["network_id"], resp["uuid"], resp["time"]
    df = resp.reindex(columns=["id", "humidity", "moisture", "temperature"])
    moisture = df["moisture"]
    newMoisture = []
    for m in moisture:
        newMoisture.append(round((1-(m/4096)) * 100))

    df["moisture"] = newMoisture
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

    # all data up till id 9985 has humidity between 0 and 1 (i.e needs to be multiplied by 100)
    print(df)
    humidity = list(df["humidity"].values)
    factor = lambda x: x*100 if x < 1 else x
    humidity =[factor(h) for h in humidity]
    df["humidity"] = humidity
    df.to_csv("data.csv")
    plotData(df, "temperature", True)