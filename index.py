import os
from flask import Flask, request, redirect, url_for, send_from_directory, render_template
from werkzeug import secure_filename
from resnet50 import run_model
UPLOAD_FOLDER = 'D:/Web/try_opencv'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','PNG'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            a = run_model(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            print('a',a)
            return redirect(url_for('uploaded_file', filename=filename,a=a))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

# @app.route('/show/<filename>')
# def uploaded_file(filename,a):
#     filename = 'http://127.0.0.1:5000/uploads/' + filename
#     return render_template('up_file.html', filename=filename,a=a)
@app.route('/show/<filename>/<a>')
def uploaded_file(filename,a):
    print('a2',a)
    # print(request.args.get('a'))
    filename = 'http://127.0.0.1:5000/uploads/' + filename
    return render_template('up_file.html', filename=filename,a=a)

@app.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)



if __name__ == '__main__':
    app.run()