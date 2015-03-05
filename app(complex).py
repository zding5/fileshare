import os
from flask import Flask, request, redirect, url_for,render_template
from werkzeug import secure_filename

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'doc', 'docx','png', 'jpg', 'jpeg', 'gif', 'ppt'])

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
        print request.form["committee"], request.form["title"], request.form["number"]
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # print os.path.join(app.config['UPLOAD_FOLDER'], filename)
            newfilename = "%s--%s--%s"%(request.form["committee"],request.form["title"],request.form["number"]+" copies")
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], newfilename))
            return redirect('/')
    path = os.path.join(app.config['UPLOAD_FOLDER'])
    print path

    lspath = os.listdir(path)
    tohyp = []
    for i in lspath:
        if not i.startswith('.'):
            print i
            tohyp.append(i)

    return str(render_template('ind.html'))+'''\
    <br> <h2 style="font-family:Times"> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; FILE LIST: </h2> <br> <p style="text-align:center; font-family:Georgia; font-size:140%">'''+'<br>'.join(map(tohyperlink, tohyp))+'</p>'

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