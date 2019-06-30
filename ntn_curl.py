import requests

def ntn_curl(url):

    try:
        return requests.get(url).headers
    except requests.exceptions.MissingSchema:
        return ntn_curl('https://' + url)
    except requests.exceptions.SSLError:
        return {'Error':'Invalid SSL Certificate'}
    except requests.exceptions.ConnectionError:
        return {'Error':'Connection timed out'}