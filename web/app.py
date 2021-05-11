from flask import Flask, render_template, request, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@db:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Product(db.Model):
    __tablename__ = 'store'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    category = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def __init__(self, name, category, price):
        self.name = name
        self.category = category
        self.price = price

@app.route('/store', methods=['GET','POST'])
def add_product():
    if request.method=='GET':
       products = Product.query.all()
       
       results = [
            {
                "name": product.name,
                "category": product.category,
                "price": product.price
            } for product in products]
       return {"count": len(results), "products": results}

    elif request.method=='POST':    
      try:
        if request.is_json:
          data = request.get_json()
          new_product = Product(name=data['name'], category=data['category'], price=data['price'])
          db.session.add(new_product)
          db.session.commit()
          return {"message": f"Product {new_product.name} has been created successfully."}
        else:
          return {"error": "The request payload is not in JSON format"}
      except exc.IntegrityError:
         db.session.rollback()
         return {"error": "Uniqe key name already in the database, database rollback"}

@app.route('/store/<product_name>', methods=['GET','PUT','DELETE'])
def handle_product(product_name):
    product = Product.query.get_or_404(product_name)
 
    if request.method == 'GET':
      result = {
            "name": product.name,
            "category": product.category,
            "price": product.price
      }
      return {"message": "success", "product": (result)}  

    elif request.method == 'PUT':
        data = request.get_json()
        product.name = data['name']
        product.category = data['category']
        product.price = data['price']
        db.session.add(product)
        db.session.commit()
        return {"message": f"Product {product.name} successfully updated"}

    elif request.method == 'DELETE':
        db.session.delete(product)
        db.session.commit()
        return {"message": f"Product {product.name} successfully deleted."}

if __name__ == '__main__':
    db.init_app(app)
    db.create_all()
    app.run(host='0.0.0.0')



