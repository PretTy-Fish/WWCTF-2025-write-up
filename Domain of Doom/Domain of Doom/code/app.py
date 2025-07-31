import subprocess, re
import os
from flask import Flask, render_template, request, flash
from uuid import uuid4
app = Flask(__name__)
app.secret_key = uuid4().hex

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/flag')
def flag():
    flag = os.environ.get('FLAG', 'WWF{placeholder_flag}')
    return render_template('index.html', flag=flag)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    def safe_domain_check(domain):
        is_safe = re.search(r'^([a-z]+.)?[a-z\d\- ]+(\.(com|org|net|sa)){1,2}', domain)
        return is_safe.group(0) if is_safe else None

    if request.method == 'POST':
        subject_domain = request.form.get('subject', '').lower()
        
        if not subject_domain:
            flash('Subject / Ticket Number is required.', 'danger')
            return render_template('contact.html')

        safe_domain = safe_domain_check(subject_domain)

        if safe_domain:
            command = f'dig +short -t A {safe_domain}'
            resolve_result = subprocess.Popen(
                command, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.STDOUT, 
                shell=True
            ).communicate()[0].strip().decode() or 'Could not resolve the provided domain/ticket!'
            
            return render_template('contact.html', resolve_result=resolve_result, submitted_domain=safe_domain)
        else:
            flash("Invalid or malicious domain/ticket has been detected.", 'danger')
            return render_template('contact.html')

    return render_template('contact.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)