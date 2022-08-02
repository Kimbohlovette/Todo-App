from flask import Flask, render_template, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:abc@localhost:5432/todoapp2'
db = SQLAlchemy(app)

class Todo(db.Model):
  __tablename__ = 'todo'
  id = db.Column(db.Integer(), primary_key=True)
  description = db.Column(db.String(), nullable=False)

  def __repre__ (self):
    return f'<Todo {self.id} {self.description}>'

db.create_all()

@app.route('/todos/create', methods=['POST'])
def add_todo():
  error = False
  body = {}
  try:
    description = request.get_json()['description']
    todo = Todo(description=description)
    db.session.add(todo)
    db.session.commit()
    body['description'] = todo.description
  except:
    error=True
    db.session.rollback()
    print(sys.exc_inf())
  
  finally:
    db.session.close()

  if not error:
    abort(400)
  else:
    return jsonify(body)
    
  

@app.route('/')
def index():
  return render_template('index.html',data=Todo.query.all())





  #Always include this at the bottom of your code (port 3000 is only neccessary in working spaces)

if __name__ == '__main__':
  app.run(host="0.0.0.0", port=3000)
