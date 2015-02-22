import os
from flask import Flask, request, redirect, url_for
from werkzeug import secure_filename

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'doc', 'docx','png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def tohyperlink(filename):
    return '<a href="/uploads/%s">%s</a>'%(filename, filename)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        print request.form["committee"], request.form["title"]
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # print os.path.join(app.config['UPLOAD_FOLDER'], filename)
            newfilename = "%s-%s-%s"%(request.form["committee"],request.form["title"],filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], newfilename))
            return redirect('/')
    path = os.path.join(app.config['UPLOAD_FOLDER'])
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file><br>
      	Please put in your committee name (required)<input type=text name=committee required><br>
      	Please put in your file title (required)   <input type=text name=title required><br>
        <input type=submit value=Upload>
    </form>
    %s
    '''%"<br>".join(map(tohyperlink, os.listdir(path)))

from flask import send_from_directory

@app.route("/filelist")
def filelist():
	path = os.path.join(app.config['UPLOAD_FOLDER'])
	print path
	return "<br>".join(os.listdir(path))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


if __name__ == '__main__':
    app.debug = True
    app.run("0.0.0.0")