from ntntools import ntncurl, ntndns, ntnsubnet, ntnping, ntntraceroute, ntnpubip, ntnoui, ntnmodels
from ntntools.ntndb import db_session

from datetime import datetime
from flask import Flask, request, render_template, redirect
from flask_flatpages import FlatPages, pygments_style_defs

from ntntools.config import DNS_RECORD_TYPES, DNS_RESOLVER_LIST, DATABASE, DATABASE_KEY

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['FLATPAGES_EXTENSION'] = '.md'
app.config['FLATPAGES_MARKDOWN_EXTENSIONS'] = ['codehilite', 'fenced_code']
app.secret_key = DATABASE_KEY

# chrome likes to add trailing slashes to links for some reason
app.url_map.strict_slashes = False


pages = FlatPages(app)


# end database sessions when the application is ended
@app.teardown_appcontext
def shutdown_session(exception = None):
    db_session.remove()


@app.context_processor
def inject_now():
    return {'now': datetime.utcnow(),
            'public_ip': request.environ.get('HTTP_X_REAL_IP', request.remote_addr)}

@app.route('/', methods=['GET', 'POST'])
def main():
    return render_template('index.html')

@app.route('/tools', methods=['GET', 'POST'])
def tools():
    return render_template('index.html')

@app.route('/tools/dns', methods=['GET', 'POST'])
def dns_check():
    if request.method == 'POST':
        return render_template('tools/dns_results.html', 
                        dns_results = ntndns.dnslookup(request.form['url'], request.form['user_resolver'],request.form['record_type']),
                    url = request.form['url'], record_type = request.form['record_type'])

    if request.is_xhr:
        return render_template('tools/dns_app.html', dns_record_types = DNS_RECORD_TYPES, dns_resolver_list = DNS_RESOLVER_LIST)
    else:
        return render_template('tools/dns.html', dns_record_types = DNS_RECORD_TYPES, dns_resolver_list = DNS_RESOLVER_LIST)


@app.route('/tools/curl', methods=['GET', 'POST'])
def curl():
    if request.method == 'POST':
        headers, status_code, elapsed_time = ntncurl.curl(request.form['url'])
        
        render_buffer = render_template('tools/curl_results.html', headers = headers, status_code = status_code, elapsed_time = elapsed_time, url = request.form['url'])
        
        # JQuery returns a string instead of a bool
        if 'true' in request.form['follow_redirects']:

            counter = 1        

            while status_code == 301 or status_code == 302 or status_code == 303 or status_code == 307 or status_code == 308:
                new_url = headers['location']
                headers, status_code, elapsed_time = ntncurl.curl(headers['location'])
                render_buffer += render_template('tools/curl_results.html', headers = headers, status_code = status_code, elapsed_time = elapsed_time, url = new_url)
                render_buffer += ' Redirect Count {}\n'.format(counter)
                counter += 1

                if counter == 30:

                    render_buffer += 'MAX REDIRECTS EXCEEDED'

        return render_buffer

    if request.is_xhr:
        return render_template('tools/curl_app.html')
    else:
        return render_template('tools/curl.html')


@app.route('/tools/subnet', methods=['GET', 'POST'])
def subnet():
    if request.method == 'POST':
        return render_template('tools/subnet_results.html', results = ntnsubnet.subnet(request.form['ip_address'], request.form['subnet_mask']),
                        ip_address = request.form['ip_address'], subnet_mask = request.form['subnet_mask'])
    if request.is_xhr:
        return render_template('tools/subnet_app.html')
    else:
        return render_template('tools/subnet.html')

@app.route('/tools/oui', methods=['GET', 'POST'])
def oui():
    try:
        if request.method == 'POST':
            return render_template('tools/oui_results.html', results = ntnoui.ouilookup(request.form['mac_address']), mac_address = request.form['mac_address'])
    except ValueError as e:
        return render_template('tools/oui_results.html', error=e)
    if request.is_xhr:
        return render_template('tools/oui_app.html')
    else:
        return render_template('tools/oui.html')


@app.route('/tools/ping', methods=['GET', 'POST'])
def ping():
    if request.method == 'POST':
        return render_template('tools/ping_results.html', results=ntnping.ping(request.form['hostname']), hostname=request.form['hostname'])
    if request.is_xhr:
        return render_template('tools/ping_app.html')
    else:
        return render_template('tools/ping.html')

@app.route('/tools/traceroute', methods=['GET', 'POST'])
def traceroute():
    if request.method == 'POST':
        return render_template('tools/traceroute_results.html', results=ntntraceroute.traceroute(request.form['hostname']), hostname=request.form['hostname'])
    if request.is_xhr:
        return render_template('tools/traceroute_app.html')
    else:
        return render_template('tools/traceroute.html')

@app.route('/notes/latest')
def latest():
    return redirect('/notes', code=302)

@app.route('/notes/programming')
def programming():
    # Only published articles
    all_articles = (p for p in pages if 'published' in p.meta)

    articles = (p for p in all_articles if 'Programming' in p.meta['category'])
    # Show the 10 most recent articles, most recent first.
    latest = sorted(articles, reverse=True,
                    key=lambda p: p.meta['published'])
    return render_template('notes/notes.html', pages=latest[:10], active='programming')

@app.route('/notes/automation')
def automation():
    # Only published articles
    all_articles = (p for p in pages if 'published' in p.meta)
    # articles are pages in the automation category
    articles = (p for p in all_articles if 'Automation' in p.meta['category'])
    # Show the 10 most recent articles, most recent first.
    latest = sorted(articles, reverse=True,
                    key=lambda p: p.meta['published'])
    return render_template('notes/notes.html', pages=latest[:10], active='automation')


@app.route('/notes/routeswitch')
def routeswitch():
    # Only published articles
    all_articles = (p for p in pages if 'published' in p.meta)
    
    articles = (p for p in all_articles if 'Route/Switch' in p.meta['category'])
    # Show the 10 most recent articles, most recent first.
    latest = sorted(articles, reverse=True,
                    key=lambda p: p.meta['published'])
    return render_template('notes/notes.html', pages=latest[:10], active='routeswitch')


@app.route('/notes/security')
def security():
    # Only published articles
    all_articles = (p for p in pages if 'published' in p.meta)
    
    articles = (p for p in all_articles if 'Security' in p.meta['category'])
    # Show the 10 most recent articles, most recent first.
    latest = sorted(articles, reverse=True,
                    key=lambda p: p.meta['published'])
    return render_template('notes/notes.html', pages=latest[:10], active='security')

@app.route('/notes/web')
def web():
    # Only published articles
    all_articles = (p for p in pages if 'published' in p.meta)
    
    articles = (p for p in all_articles if 'Web' in p.meta['category'])
    # Show the 10 most recent articles, most recent first.
    latest = sorted(articles, reverse=True,
                    key=lambda p: p.meta['published'])
    return render_template('notes/notes.html', pages=latest[:10], active='web')


@app.route('/notes/ntn')
def ntnnotes():
    # Only published articles
    all_articles = (p for p in pages if 'published' in p.meta)
    
    articles = (p for p in all_articles if 'NTN' in p.meta['category'])
    # Show the 10 most recent articles, most recent first.
    latest = sorted(articles, reverse=True,
                    key=lambda p: p.meta['published'])
    return render_template('notes/notes.html', pages=latest[:10], active='ntn')


@app.route('/notes/cheatsheets')
def cheatsheets():
    # Only published articles
    all_articles = (p for p in pages if 'published' in p.meta)
    
    articles = (p for p in all_articles if 'Cheatsheets' in p.meta['category'])
    # Show the 10 most recent articles, most recent first.
    latest = sorted(articles, reverse=True,
                    key=lambda p: p.meta['published'])
    return render_template('notes/notes.html', pages=latest[:10], active='cheatsheets')


@app.route('/notes/wireless')
def wireless():
    # Only published articles
    all_articles = (p for p in pages if 'published' in p.meta)
    
    articles = (p for p in all_articles if 'Wireless' in p.meta['category'])
    # Show the 10 most recent articles, most recent first.
    latest = sorted(articles, reverse=True,
                    key=lambda p: p.meta['published'])
    return render_template('notes/notes.html', pages=latest[:10], active='wireless')

@app.route('/notes')
def notes():
    # Articles are pages with a publication date
    articles = (p for p in pages if 'published' in p.meta)
    # Show the 10 most recent articles, most recent first.
    latest = sorted(articles, reverse=True,
                    key=lambda p: p.meta['published'])
    return render_template('notes/notes.html', pages=latest[:7], active='latest')

@app.route('/notes/<path:path>/')
def page(path):
    page = pages.get_or_404(path)
    template = page.meta.get('template', 'notes/note.html')
    return render_template(template, page=page)

# required for syntax highlighting with flatpages
@app.route('/pygments.css')
def pygments_css():
    return pygments_style_defs('tango'), 200, {'Content-Type': 'text/css'}

if __name__ == "__main__":
    app.run(host='0.0.0.0')
