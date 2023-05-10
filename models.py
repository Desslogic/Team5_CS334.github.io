from datetime import datetime
from flask_login import UserMixin

def create_tables(db):

    class Customer(db.Model):
        customer_id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String, nullable=False)
        email = db.Column(db.String, unique=True, nullable=False)
        address = db.Column(db.String, nullable=False)
        purchases = db.relationship('Purchase', backref='customer', lazy=True)
        
        def serialize(self):
            return {
                "customer_id": self.customer_id,
                "name": self.name,
                "email": self.email,
                "address": self.address
            }


    class Employee(db.Model, UserMixin):
        employee_id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String, nullable=False)
        email = db.Column(db.String, unique=True, nullable=False)
        password_hash = db.Column(db.String, nullable=False)
        role = db.Column(db.String, nullable=False)
        
        def serialize(self):
            return {
                "employee_id": self.employee_id,
                "name": self.name,
                "email": self.email,
                "role": self.role
            }
    class Product(db.Model):
        product_id = db.Column(db.Integer, primary_key=True)
        product_name = db.Column(db.String, nullable=False)
        description = db.Column(db.Text)
        price = db.Column(db.Float, nullable=False)
        image_url = db.Column(db.String)
        purchase_items = db.relationship('PurchaseItem', backref='product', lazy=True)
        product_toppings = db.relationship('ProductTopping', backref='product', lazy=True)
        
        def serialize(self):
            return {
                "product_id": self.product_id,
                "product_name": self.product_name,
                "description": self.description,
                "price": self.price,
                "image_url": self.image_url
            }

    class Purchase(db.Model):
        purchase_id = db.Column(db.Integer, primary_key=True)
        customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'), nullable=False)
        purchase_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
        purchase_items = db.relationship('PurchaseItem', backref='purchase', lazy=True)

        def serialize(self):
            return {
                "purchase_id": self.purchase_id,
                "customer_id": self.customer_id,
                "purchase_date": self.purchase_date.isoformat()
            }

    class PurchaseItem(db.Model):
        purchase_item_id = db.Column(db.Integer, primary_key=True)
        purchase_id = db.Column(db.Integer, db.ForeignKey('purchase.purchase_id'), nullable=False)
        product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'), nullable=False)
        quantity = db.Column(db.Integer, nullable=False)
    
        def serialize(self):
            return {
                "purchase_item_id": self.purchase_item_id,
                "purchase_id": self.purchase_id,
                "product_id": self.product_id,
                "quantity": self.quantity
            }


    class Topping(db.Model):
        topping_id = db.Column(db.Integer, primary_key=True)
        topping_name = db.Column(db.String, nullable=False)
        price = db.Column(db.Float, nullable=False)
        product_toppings = db.relationship('ProductTopping', backref='topping', lazy=True)
        
        def serialize(self):
            return {
                "topping_id": self.topping_id,
                "topping_name": self.topping_name,
                "price": self.price
            }

    class ProductTopping(db.Model):
        product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'), primary_key=True)
        topping_id = db.Column(db.Integer, db.ForeignKey('topping.topping_id'), primary_key=True)
    
        def serialize(self):
            return {
                "product_id": self.product_id,
                "topping_id": self.topping_id
            }
            
    return Customer, Employee, Product, Purchase, PurchaseItem, Topping, ProductTopping
