from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import binascii
import gzip
import os


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
         return '<Task %r>' % self.id

class BinaryFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(200), nullable=False)
    data = db.Column(db.LargeBinary)

@app.route('/', methods=['POST', 'GET'])
def index():
    files = BinaryFile.query.all()
    return render_template('index.html', files = files)

@app.route('/software_design')
def render_design():
    return render_template('software_design.html')

@app.route('/uploader', methods = ['POST'])
def upload_file():
    f = request.files['file']
    if f.filename == '':
        return redirect('/')

    file_name = f.filename
    new_file = BinaryFile(file_name=file_name, data=f.read())
    try:
        db.session.add(new_file)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        return "Exception uploading file"

@app.route('/delete/<int:id>')
def delete(id):
    file_to_delete = BinaryFile.query.get_or_404(id)
    try:
        db.session.delete(file_to_delete)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        print(e)

@app.route('/compress/<int:id>')
def compress(id):
    return render_template('/compression_result.html')

def read_file():
    f_in = open('sample_ecg_raw.bin', 'rb')
    content = f_in.read()
    print(content)
    f_in.close()

if __name__ == "__main__":
    print("Starting app")
    app.run(debug=True)
