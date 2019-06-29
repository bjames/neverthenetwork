import requests

def ntn_curl(url):

    try:
        return requests.get(url).headers
    except requests.exceptions.MissingSchema:
        return ntn_curl('https://' + url)
    except requests.exceptions.SSLError:
        return 'SSL Error'