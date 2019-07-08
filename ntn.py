from flask import Flask, request, render_template
from config import DNS_RECORD_TYPES, DNS_RESOLVER_LIST
from ntn_dns import ntn_dns
from ntn_curl import ntn_curl
from ntn_subnet import ntn_subnet

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def main():
    return render_template('index.html')

@app.route('/dns', methods=['GET', 'POST'])
def dns_check():
    if request.method == 'POST':
        return render_template('dns.html', 
                        dns_results = ntn_dns(request.form['dns_lookup'], request.form['user_resolver'], request.form['record_type']),
                    dns_lookup = request.form['dns_lookup'],record_type = request.form['record_type'])
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


if __name__ == "__main__":
    app.run(host='0.0.0.0')
