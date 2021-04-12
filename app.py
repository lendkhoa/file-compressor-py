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
    blob = db.Column(db.LargeBinary)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        task_content = request.form['content']
        new_task = Todo(content=task_content)
        # push to db
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(e)
            return "Exception"
    else:
        # query the table
        tasks = Todo.query.order_by(Todo.date_created).all()
        files = BinaryFile.query.all()
        return render_template('index.html', tasks=tasks, files = files)

@app.route('/software_design')
def render_design():
    return render_template('software_design.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      file_name = f.filename
      with open(file_name, 'br') as f:
          content = f.read()
          print(type(content))
          hexa = binascii.hexlify(content)
          print(type(hexa))

      #new_file = BinaryFile(file_name=file_name, )
      return hexa

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        print(e)

def read_file():
    f_in = open('sample_ecg_raw.bin', 'rb')
    content = f_in.read()
    print(content)
    f_in.close()

if __name__ == "__main__":
    print("Starting app")
    app.run(debug=True)
