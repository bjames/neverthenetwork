from flask import Flask, request, render_template
from ntn_dns import ntn_dns
from ntn_curl import ntn_curl
from ntn_subnet import ntn_subnet

app = Flask(__name__)


@app.route('/', methods=['GET'])
def main():
    return render_template('index.html')

@app.route('/dnslookup', methods=['GET', 'POST'])
def dns_check():
    if request.method == 'POST':
        return render_template('dns.html', 
                        dns_results = ntn_dns(request.form['dns_lookup'],request.form['record_type']),
                    dns_lookup = request.form['dns_lookup'],record_type = request.form['record_type'], dns_active=True)
    return render_template('dns.html', dns_active=True)

@app.route('/curl', methods=['GET', 'POST'])
def curl():
    if request.method == 'POST':
        return render_template('curl.html', results = ntn_curl(request.form['url']),
                        url = request.form['url'], curl_active=True)
    return render_template('curl.html', curl_active=True)

@app.route('/subnet', methods=['GET', 'POST'])
def subnet():
    if request.method == 'POST':
        return render_template('subnet.html', results = ntn_subnet(request.form['ip_address'], request.form['subnet_mask']),
                        ip_address = request.form['ip_address'], subnet_mask = request.form['subnet_mask'], subnet_active=True)
    return render_template('subnet.html', subnet_active=True)