import random
import requests
import http.client
import numpy as np
from flask import Flask
from flask import request, escape

app = Flask(__name__)

def getData(ID, ID_Data):
    """ Converts the data sent by the server into the original message

    Parameters
    ----------
    ID : list(:float)
        ID of the client
    ID_Data: list(:float)
        Array containing ID embedded with data

    Returns
    -------
    str
        The data which was published by the client with the specified ID

    """
    data = np.divide(np.array(ID_Data) - np.array(ID), np.array(ID))
    curr = ""
    data[np.isclose(data, -1)] = 0
    dataBinary = []
    for i in range(len(data)):
        
        if i and  i % 8 == 0:
            dataBinary.append(curr)
            curr = ""
        curr += str(int(data[i]))
    dataString1 = list(map(lambda x: chr(int(x, 2)), dataBinary))
    return "".join(dataString1)

def fetchDataFromPubServer(ID_arr):
    """ Sends the client ID to the Pub/Sub server to fetch the published data

    Parameters
    ----------
    ID_arr : list(:float)
        ID of the client

    Returns
    -------
    str
        The data which was published by the client with the sppecified ID

    """
    pubSubURL = "http://localhost:7001/fetchData"
    myData = {"ID": ID_arr}
    clientIDData = requests.post(pubSubURL, json=myData).json()["data"]

    data = getData(ID_arr, clientIDData)
    print(data)
    return data

def fetchIDFromClientURL(clientURL: str):
    """ Fetches Client ID from the specified client URL

    Parameters
    ----------
    clientURL : str
        URL of the client to fetch ID from

    Returns
    -------
    list(:float)
        A float array containing the ID

    """
    conn = http.client.HTTPConnection(clientURL)
    conn.request('GET', '/')

    resp = conn.getresponse()
    content = resp.read()

    conn.close()

    text = content.decode('utf-8')

    ID_arr = text.split(" ")
    ID_arr = list(map(float, ID_arr))
    return ID_arr


@app.route("/")
def index():
    """
    The function index is a callback for when a user lands on the homepage URL: 127.0.0.1:6001

    It loads an input form to enter the URL of the client. It then fetched the ID from that URL
    and queries the Publish Subscribe server to fetch the Data
    """
    clientURL = request.args.get("ClientURL", "")
    if clientURL:
        ID_arr = fetchIDFromClientURL(clientURL)
        data = fetchDataFromPubServer(ID_arr)
    return (
        """<form action="" method="get">
                <input type="text" name="ClientURL">
                <input type="submit" value="Fetch Data">
            </form>"""
        + clientURL
        + data
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=6001, debug=True)
