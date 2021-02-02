import requests
import json

# Default header, as probably no other is used (for now).
default_header = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}

# Sends a request with given url, verb and body.
def send_req(job):
    url = job["url"]
    verb = job["verb"]
    body = job["body"]
    print ("%s: \"%s\"" % (url, verb), end=": ")
    r = "unhandled verb"
    if verb == "post":
        r = requests.post(url, data=body, headers=default_header)
    elif verb == "patch": 
        r = requests.patch(url, data=body, headers=default_header)
    elif verb == "get": 
        r = requests.get(url, data=body)
    elif verb == "delete": 
        r = requests.delete(url, data=body)
    print(r)
    return r
        


