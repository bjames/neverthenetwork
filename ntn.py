from flask import Flask, request, render_template
from ntn_dns import ntn_dns

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def dns_check():
    if request.method == 'POST':
        return render_template('index.html', 
                        dns_results = ntn_dns(request.form['dns_lookup'],
                        request.form['record_type'])
                    )
    return render_template('index.html')