"""
Authour: Ali Kamel
This script simulates an AgriPod base-station communicating with the server.py and tests responses
"""

import requests as rq
from string import ascii_letters
import random
def randomString(l=6):
    """
    this function creates a random string
    :param l: length of random string
    :return: random string
    """


    nums = [str(x) for x in list(range(0,9))]
    alphas = nums + list(ascii_letters)
    string = ""
    for i in range(l):
        string += random.choice(alphas)
    return string
def sendPostData():
    """
    sends random string to the server and tests that the server returns the same thing
    :return: None
    """
    dataStr = randomString()
    obj = {
        "test": True,
        "data" : dataStr
    }
    resp = rq.post(url="http://127.0.0.1:5000/inputData/",data=obj)
    assert resp.text == dataStr

if __name__ == '__main__':
    sendPostData()