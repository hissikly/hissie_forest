from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
db = SQLAlchemy(app)

class Article(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	text = db.Column(db.Text, nullable=False)
	price = db.Column(db.Integer, nullable=False)
	category = db.Column(db.String(30), nullable=False)
	date = db.Column(db.DateTime, default=datetime.utcnow)

	def __repr__(self):
		return '<Article %r>' % self.id

@app.route('/')
def index():
	return render_template("index.html")

@app.route('/products')
def products_list():
	articles = Article.query.order_by(Article.date.desc()).all()
	return render_template("products.html", articles=articles)

@app.route('/add-product', methods=['POST', 'GET'])
def add_products():
	if request.method == "POST":
		title = request.form["title"]
		text = request.form["text"]
		price = request.form["price"]
		category = request.form["category"]

		article = Article(title=title, text=text, price=price, category=category)

		try:
			db.session.add(article)
			db.session.commit()
			return redirect('/products')
		except:
			return "При публикации товара произошла ошибка"
	else:
		return render_template("add-product.html")
	
@app.route("/products/<int:id>")
def check_details(id):
	article = Article.query.get(id)
	return render_template("product_detail.html", article=article)

@app.route('/products/<int:id>/delete')
def product_delete(id):
    article = Article.query.get_or_404(id)

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/products')
    except:
        return "При удалении товара произошла ошибка"

@app.route('/products/<string:category>')
def category_navigator(category):
	articles = Article.query.order_by(Article.date.desc()).all()
	cat_dict = {'Семьям': 'for-family', 'Для себя': 'for-me', 'Для комании': 'for-friends'}
	return render_template("/category-navigator.html", category=category, articles=articles, cat_dict=cat_dict)

if __name__ == "__main__":
    app.run(debug=True)