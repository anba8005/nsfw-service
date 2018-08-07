import PIL.Image as Image
from nsfw import classify

import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

from datetime import datetime

UPLOAD_FOLDER = '/tmp'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

def allowed_file(filename):
    return '.' in filename and \
       filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def analyze_file(filename):
    image = Image.open(filename)
    sfw, nsfw = classify(image)
    return nsfw

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    #
    if request.method == 'POST':
       # check if the post request has the file part
       if 'file' not in request.files:
           flash('No file part')
           return redirect(request.url)
       file = request.files['file']
       # if user does not select file, browser also
       # submit an empty part without filename
       if file.filename == '':
           flash('No selected file')
           return redirect(request.url)
       if file and allowed_file(file.filename):
           # all good in da hood :)
           filename = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
           file.save(filename)
           start = datetime.now()
           nsfw = analyze_file(filename)
           end = datetime.now()
           os.remove(filename)
           if nsfw >= 0.8:
               flash('NUDITY detected (NSFW >= 0.8)')
           flash("NSFW Probability: {}".format(nsfw))
           flash("Processing time {} seconds".format((end-start).total_seconds()))
           return redirect(request.url)
       else:
           flash('Invalid file type')
           return redirect(request.url)
    #
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
