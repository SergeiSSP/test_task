import os
from datetime import datetime

from flask import Flask, flash, request, redirect, send_file
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = 'downloads'


app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Cannot read file')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            start = datetime.now()
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            end = datetime.now()
            delta = end - start
            return f'File {filename} is uploaded in {delta} and link is <a href="/uploads/{filename}">Download {filename}</a>'
    return '''
    <!doctype html>
    <title>Load new file</title>
    <h1>Load new file</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    </html>
    '''

@app.route('/uploads/<name>')
def download_file(name):
    filename = os.path.join(app.config['UPLOAD_FOLDER'], name)
    return send_file(filename, as_attachment=True)


if __name__ == "__main__":
    if not os.path.exists('downloads'):
        os.mkdir('downloads')
    else:
        print('Directory already exists')
    app.run()
