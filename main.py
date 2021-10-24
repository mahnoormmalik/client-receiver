import random
# import urllib.request
import http.client
from flask import Flask
from flask import request, escape

app = Flask(__name__)

@app.route("/")
def index():
    clientURL = request.args.get("ClientURL", "")
    if clientURL:
        conn = http.client.HTTPConnection(clientURL)
        conn.request('GET', '/')

        resp = conn.getresponse()
        content = resp.read()

        conn.close()

        text = content.decode('utf-8')
    
        ID_arr = text.split(" ")
        print(ID_arr)
    return (
        """<form action="" method="get">
                <input type="text" name="ClientURL">
                <input type="submit" value="Fetch Data">
            </form>"""
        + clientURL
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=6001, debug=True)

# def get_client_ID():

#     conn = http.client.HTTPConnection('127.0.0.1:5002')
#     conn.request('GET', '/')

#     resp = conn.getresponse()
#     content = resp.read()

#     conn.close()

#     text = content.decode('utf-8')
    
#     ID_arr = text.split(" ")
#     print(ID_arr)


# if __name__ == "__main__":
#     ID = get_client_ID()