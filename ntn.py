import ntn_models

from datetime import datetime
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from ntn_dns import ntn_dns
from ntn_curl import ntn_curl
from ntn_subnet import ntn_subnet
from ntn_oui import ntn_oui
from ntn_db import db_session
from ntn_pubip import ntn_pubip
from ntn_ping import ntn_ping
from ntn_traceroute import ntn_traceroute

from config import DNS_RECORD_TYPES, DNS_RESOLVER_LIST, DATABASE, DATABASE_KEY

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = DATABASE_KEY


# end database sessions after when the application is ended
@app.teardown_appcontext
def shutdown_session(exception = None):
    db_session.remove()

@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

@app.route('/', methods=['GET', 'POST'])
def main():
    return render_template('index.html', public_ip = ntn_pubip())

@app.route('/dns', methods=['GET', 'POST'])
def dns_check():
    if request.method == 'POST':
        return render_template('dns.html', 
                        dns_results = ntn_dns(request.form['dns_lookup'], request.form['user_resolver'], request.form['record_type']),
                    dns_lookup = request.form['dns_lookup'], record_type = request.form['record_type'])
    return render_template('dns_app.html', dns_record_types = DNS_RECORD_TYPES, dns_resolver_list = DNS_RESOLVER_LIST)

@app.route('/curl', methods=['GET', 'POST'])
def curl():
    if request.method == 'POST':
        results, elapsed_time = ntn_curl(request.form['url'])
        return render_template('curl.html', results = results, elapsed_time = elapsed_time, url = request.form['url'])
    return render_template('curl_app.html')

@app.route('/subnet', methods=['GET', 'POST'])
def subnet():
    if request.method == 'POST':
        return render_template('subnet.html', results = ntn_subnet(request.form['ip_address'], request.form['subnet_mask']),
                        ip_address = request.form['ip_address'], subnet_mask = request.form['subnet_mask'])
    return render_template('subnet_app.html')

@app.route('/oui', methods=['GET', 'POST'])
def oui():
    try:
        if request.method == 'POST':
            return render_template('oui.html', results = ntn_oui(request.form['mac_address']))
    except ValueError as e:
        return render_template('oui.html', error = e)
    return render_template('oui_app.html')


@app.route('/ping', methods=['GET', 'POST'])
def ping():
    if request.method == 'POST':
        return render_template('ping.html', results = ntn_ping(request.form['hostname']), hostname = request.form['hostname'])
    return render_template('ping_app.html')


@app.route('/traceroute', methods=['GET', 'POST'])
def traceroute():
    if request.method == 'POST':
        return render_template('traceroute.html', results = ntn_traceroute(request.form['hostname']), hostname = request.form['hostname'])
    return render_template('traceroute_app.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0')
