from flask import request

def ntn_pubip():

    return(request.remote_addr)
