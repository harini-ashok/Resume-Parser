import imghdr
import os
from flask import Flask, render_template, request, redirect, url_for, abort, \
    send_from_directory
from werkzeug.utils import secure_filename
from ResumeParser import *
from db import *
from waitress import serve

app = Flask(__name__)
#app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.pdf', '.docx', '.doc']
app.config['UPLOAD_PATH'] = 'resume'

@app.route('/')
def index():
    files = os.listdir(app.config['UPLOAD_PATH'])
    return render_template('index.html', files=files)

@app.route('/', methods=['POST'])
def upload_files():
    uploaded_file = request.files['file']
    name = request.values['name']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            abort(400)
        uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        
        
        parsed_record = parser(extract_using_tesseract(filename))
        
        parsed_record['name'] = name
    
        insert_to_tables(parsed_record)
        ID = get_id('name_db', 'candidate_name', "'"+name+"'")
        record = retrieve(ID)
        record_to_json(record)

        return 'file parsed successfully'
    else:
        return 'wrong filename'

serve(app, host='0.0.0.0', port=8082, threads=1)