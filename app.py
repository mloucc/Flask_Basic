import os
from flask import Flask, render_template, request, url_for, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Category(db.Model):
    __tablename__ = 'Category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    item = db.relationship('Item', backref='Category')

    def __repr__(self):
        return "{\"id\":" + str(self.id) + ", \"name\":\"" + self.name + "\"}"
        # return "{\"id\":" + self.id + "," + "\"name\":\"" + self.name + "\"}"
        # return f'<Category {self.name}>'


class Item(db.Model):
    __tablename__ = 'Item'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    content = db.Column(db.String(100), nullable=False, default='')
    done = db.Column(db.Boolean, nullable=False, default=False)
    cat_id = db.Column(db.Integer, db.ForeignKey('Category.id'), nullable=False)

    def __repr__(self):
        if self.done:
            xdone = 1
        else:
            xdone = 0
        return "{\"id\":" + str(self.id) + ", \"title\":\"" + self.title + "\", \"content\":\"" + \
               self.content + "\", \"done\":" + str(xdone) + ", \"cat_id\":" + str(self.cat_id) + "}"
        # return f'<Item {self.title}>'


@app.route("/category")
def another():
    allcat = str(Category.query.all())
    return allcat


@app.route("/todos/<int:id>")
def todos(id):
    print("query id: " + str(id))
    allcat = str(Item.query.filter_by(cat_id=id).all())
    return allcat


@app.route("/del_todo", methods=['GET', 'POST'])
def del_todo():
    if request.method == 'POST':
        del_id = request.get_json()['id']
        print("del id: " + str(del_id))
        del_item = Item.query.filter_by(id=del_id).first()
        db.session.delete(del_item)
        db.session.commit()
        return 'OK'


@app.route("/")
def hello_world():
    user_agent = request.headers.get('User-Agent')
    return '<p>Your browser is %s</p>' % user_agent


@app.route('/new_cat', methods=['GET', 'POST'])
def new_cat():
    if request.method == 'POST':
        print("good till now")
        new_cat = request.get_json()['new_cat']
        print(new_cat)
        newcat = Category(name=new_cat)
        db.session.add(newcat)
        db.session.commit()
        return 'OK'

    else:
        return 'Content-Type not supported!'


@app.route('/add_todo', methods=['GET', 'POST'])
def add_todo():
    if request.method == 'POST':
        print("good till now")
        new_title = request.get_json()['title']
        print(new_title)
        cat_id = request.get_json()['cat_id']
        print(cat_id)
        newitem = Item(title=new_title, cat_id=cat_id)
        db.session.add(newitem)
        db.session.commit()
        return 'OK'

    else:
        return 'Content-Type not supported!'


@app.route('/del_cat', methods=['GET', 'POST'])
def del_cat():
    if request.method == 'POST':
        print("good till now")
        cat_id = request.get_json()['cat_id']
        print(cat_id)
        delcat = Category.query.filter_by(id=cat_id).first()
        db.session.delete(delcat)
        db.session.commit()
        return 'OK'

    else:
        return 'Content-Type not supported!'


app.run("0.0.0.0", 5000)
