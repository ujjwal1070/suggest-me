import os
from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

app = Flask(__name__)
# app.secret_key = os.environ.get('SECRET')
# add some secret key

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

db = SQLAlchemy(app)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    review = db.Column(db.Text, nullable=True)
    upvotes = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Item %r>' % self.name


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    items = db.relationship('Item', backref='category')
    upvotes = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return '<Category %r>' % self.name


@app.route('/', methods=['GET'])
def index():

    movie_category = Category.query.filter_by(name='movie').first()
    if movie_category:
        try:

            # print(movie_category.id)
            categories = Category.query.all()
            items = Item.query.filter_by(
                category_id=movie_category.id).order_by(Item.upvotes.desc()).all()
            # items = movie_category.items  # foreign relation in model class
            return render_template('index.html', items=items, categories=categories, current_category=movie_category)
        except:
            return render_template('index.html')
    else:
        return render_template('index.html', current_category='')


@app.route('/browse/<string:category>', methods=['POST', 'GET'])
def browseCategory(category):
    if request.method == 'POST':
        favorite_item = request.form['favorite']
        if favorite_item == '':
            flash(f'Invalid empty string. Please add appropriate text.')
            return redirect('/')
        category_string = request.form['item-category']
        review = request.form['review']
        category_id = int(category_string)
        print(f'category id is {category_id}')

        new_item = Item(name=favorite_item,
                        category_id=category_id, review=review)
        try:
            db.session.add(new_item)
            db.session.commit()
            return redirect(f'/browse/{category}')
        except:
            return 'ran into some issue'

    else:
        category = Category.query.filter_by(name=category).first()
        print(category)
        #print(f'these items belongs to category {category.id}')
        items = Item.query.filter_by(
            category_id=category.id).order_by(Item.upvotes.desc()).all()
        # items = category.items  # possible beacause of foreign relation in model class
        categories = Category.query.all()
        return render_template('index.html', items=items, categories=categories, current_category=category)


@app.route('/addCategory', methods=['POST', 'GET'])
def addcategory():
    if request.method == 'POST':
        category = request.form['category']
        new_category = Category(name=category)
        print(category)

        try:
            db.session.add(new_category)
            db.session.commit()
            print(f'{category} added')
            return redirect('/')

        except:
            flash(f'There was an issue adding the category.')
            return redirect('/')

    else:
        return redirect('/')



@app.route('/increment', methods=['POST'])
def increment():
    data = request.get_data(as_text=True)
    item_id = int(data)
    item_selected = Item.query.get_or_404(item_id)
    item_selected.upvotes = item_selected.upvotes + 1
    db.session.commit()

    item_upvotes = Item.query.get_or_404(item_id).upvotes
    return json.dumps({'upvotes': item_upvotes})


@app.route('/decrement', methods=['POST'])
def decrement():
    data = request.get_data(as_text=True)
    item_id = int(data)
    item_selected = Item.query.get_or_404(item_id)
    item_selected.upvotes = item_selected.upvotes - 1
    db.session.commit()

    item_upvotes = Item.query.get_or_404(item_id).upvotes
    return json.dumps({'upvotes': item_upvotes})


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=False)
