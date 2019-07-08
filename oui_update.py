import requests
import sqlite3

from config import OUI_FILES

def download_oui_lists():


    for oui_file in OUI_FILES:

        response = requests.get(oui_file['url'])

        if response.status_code == 200:

            with open(oui_file['file_name'], 'wb') as outfile:
                
                outfile.write(response.content)


if __name__ == "__main__":

    download_oui_lists()