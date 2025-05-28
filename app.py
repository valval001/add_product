from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
app.secret_key = app.config['SECRET_KEY']

db = SQLAlchemy(app)

class Product(db.Model):
    __tablename__ = 'products'  # Your actual table name
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(200), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add-product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])
        image_url = request.form['image_url']

        new_product = Product(name=name, description=description, price=price, image_url=image_url)
        db.session.add(new_product)
        db.session.commit()
        flash("Product added successfully!")
        return redirect(url_for('all_products'))

    return render_template('add_product.html')

@app.route('/all-products')
def all_products():
    products = Product.query.all()
    return render_template('all_products.html', products=products)

@app.route('/edit-product/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    product = Product.query.get_or_404(id)
    if request.method == 'POST':
        product.name = request.form['name']
        product.description = request.form['description']
        product.price = float(request.form['price'])
        product.image_url = request.form['image_url']

        db.session.commit()
        flash("Product updated successfully!")
        return redirect(url_for('all_products'))

    return render_template('edit_product.html', product=product)

@app.route('/delete-product/<int:id>', methods=['POST'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash("Product deleted successfully!")
    return redirect(url_for('all_products'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
