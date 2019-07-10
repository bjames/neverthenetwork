from re import sub

from config import OUI_FILES
from ntn_models import OUI_MAL, OUI_MAM, OUI_MAS
from ntn_db import db_session


def mal_lookup(mac_address, Session):

    return(Session.query(OUI_MAL).filter(OUI_MAL.assignment == mac_address[:6]).all())


def mam_lookup(mac_address, Session):

    return(Session.query(OUI_MAM).filter(OUI_MAM.assignment == mac_address[:7]).all())


def mas_lookup(mac_address, Session):

    return(Session.query(OUI_MAS).filter(OUI_MAS.assignment == mac_address[:9]).all())


def ntn_oui(mac_address):

    Session = db_session()

    # make the mac_address uppercase to match the database 
    mac_address = mac_address.upper()

    # strip all non-alpha numeric characters
    mac_address = sub('\W+', '', mac_address)

    try:

        int(mac_address, 16)

    except ValueError:

        raise ValueError('Invalid input, MAC addresses should only contain hexidecimal values')

    results = mal_lookup(mac_address, Session)

    for result in results:

        if 'IEEE' in result.organization:

            result = mam_lookup(mac_address, Session)

            if len(result) == 0:

                result = mas_lookup(mac_address, Session)

    return results


if __name__ == '__main__':

    # This one returns three values
    print(ntn_oui('08:00:30:de:ad:de'))

    # This one returns two values
    print(ntn_oui('0001c8000000'))

    print(ntn_oui('00:22:72:de:ad:de'))

    # Requires a lookup into the MAS table    
    print(ntn_oui('2085.93BD.EAD0'))

    # Requires a lookup into the MAM table
    print(ntn_oui('70B3.D556.F000'))