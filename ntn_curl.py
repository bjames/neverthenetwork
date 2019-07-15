import requests
from urllib3.util.url import parse_url

def ntn_curl(url):

    try:
        response = requests.head(url)
        return response.headers, response.elapsed.total_seconds()

    except requests.exceptions.MissingSchema:
        return ntn_curl('https://' + url)

    except requests.exceptions.SSLError:
        return {'Error':'Invalid SSL Certificate'}

    except requests.exceptions.ConnectionError as e:

        error_str = str(e)

        if 'timed' in error_str:
            return {'Error':'Connection timed out'}
        elif 'refused' in error_str:
            return {'Error':'Connection refused'}
        elif 'Name or service' in error_str:
            return {'Error':'DNS resolution failed'}
        elif 'Invalid' in error_str:
            return {'Error':'Check provided hostname, valid input includes IP addresses and hostnames'}
        else:
            return {'Error': error_str}


if __name__ == '__main__':

    print(ntn_curl('https://neverthenetwork.com'))
    print(ntn_curl('https://beta.neverthenetwork.com'))
    print(ntn_curl('0.0.0.1'))
    print(ntn_curl('http://neverthenetwork.com/thisisatest'))
    print(ntn_curl('192.168.1.1'))