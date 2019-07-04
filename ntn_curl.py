import requests
from urllib3.util.url import parse_url

def ntn_curl(url):

    try:
        response = requests.head(url)
    except requests.exceptions.MissingSchema:
        return ntn_curl('https://' + url)

    try:
        return response.headers, response.elapsed.total_seconds()
    except requests.exceptions.SSLError:
        return {'Error':'Invalid SSL Certificate'}, response.elapsed.total_seconds()
    except requests.exceptions.ConnectionError:
        return {'Error':'Connection timed out'}, response.elapsed.total_seconds()