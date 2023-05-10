import sqlite3
from flask import Flask, request, jsonify, render_template, redirect, url_for
from forms import LoginForm
from flask import flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from models import create_tables
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
db = SQLAlchemy(app)

Customer, Employee, Product, Purchase, PurchaseItem, Topping, ProductTopping = create_tables(db)
##########################
### authenticate users ###
##########################

@app.route('/login', methods=['GET', 'POST'])
def authenticate_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Perform validation and authentication logic here

        # If the user is authenticated, redirect to another page
        return redirect(url_for('home'))

    return render_template('login.html')


####################
### Login Routes ###
####################
# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        employee = Employee.query.filter_by(email=form.email.data).first()

        if employee and employee.check_password(form.password.data):
            login_user(employee)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))

        flash('Invalid email or password', 'danger')

    return render_template('login.html', form=form)

# check the user's credentials to determine whether to show an 
# error message or redirect to a different page.
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        # Replace the following line with your own user authentication logic
        if not authenticate_user(email):
            error = 'Invalid email address.'
        else:
            # Redirect to another page if the login is successful
            return redirect(url_for('dashboard'))
    return render_template('login.html', error=error)


#####################
### LogOut Routes ###
#####################
# LogOut Page
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

#######################
### Customer Routes ###
#######################
# Get all customers
@app.route('/customers', methods=['GET'])
def get_customers():
    customers = Customer.query.all()
    return jsonify([customer.serialize() for customer in customers])

# Create a new customer
@app.route('/customers', methods=['POST'])
def add_customer():
    name = request.form['name']
    email = request.form['email']
    address = request.form['address']

    new_customer = Customer(name=name, email=email, address=address)
    db.session.add(new_customer)
    db.session.commit()

    return jsonify(new_customer.serialize()), 201

# Get a specific customer by ID
@app.route('/customers/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    return jsonify(customer.serialize())

# Update an existing customer
@app.route('/customers/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    
    name = request.form['name']
    email = request.form['email']
    address = request.form['address']

    customer.name = name
    customer.email = email
    customer.address = address

    db.session.commit()
    return jsonify(customer.serialize())

# Delete a customer
@app.route('/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    db.session.delete(customer)
    db.session.commit()

    return jsonify({"message": "Customer deleted"}), 200

#######################
### Employee Routes ###
#######################
# Get all employees
@app.route('/employees', methods=['GET'])
def get_employees():
    employees = Employee.query.all()
    return jsonify([employee.serialize() for employee in employees])

# Create a new employee
@app.route('/employees', methods=['POST'])
def add_employee():
    name = request.form['name']
    email = request.form['email']
    password_hash = request.form['password_hash']
    role = request.form['role']

    new_employee = Employee(name=name, email=email, password_hash=password_hash, role=role)
    db.session.add(new_employee)
    db.session.commit()

    return jsonify(new_employee.serialize()), 201

# Get a specific employee by ID
@app.route('/employees/<int:employee_id>', methods=['GET'])
def get_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    return jsonify(employee.serialize())

# Update an existing employee
@app.route('/employees/<int:employee_id>', methods=['PUT'])
def update_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    
    name = request.form['name']
    email = request.form['email']
    role = request.form['role']

    employee.name = name
    employee.email = email
    employee.role = role

    db.session.commit()
    return jsonify(employee.serialize())

# Delete an employee
@app.route('/employees/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    db.session.delete(employee)
    db.session.commit()

    return jsonify({"message": "Employee deleted"}), 200

######################
### Product Routes ###
######################
# Get all products
@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([product.serialize() for product in products])

# Create a new product
@app.route('/products', methods=['POST'])
def add_product():
    product_name = request.form['product_name']
    description = request.form['description']
    price = request.form['price']
    image_url = request.form['image_url']

    new_product = Product(product_name=product_name, description=description, price=price, image_url=image_url)
    db.session.add(new_product)
    db.session.commit()

    return jsonify(new_product.serialize()), 201

# Get a specific product by ID
@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify(product.serialize())

# Update an existing product
@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = Product.query.get_or_404(product_id)
    
    product_name = request.form['product_name']
    description = request.form['description']
    price = request.form['price']
    image_url = request.form['image_url']

    product.product_name = product_name
    product.description = description
    product.price = price
    product.image_url = image_url

    db.session.commit()
    return jsonify(product.serialize())

# Delete a product
@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()

    return jsonify({"message": "Product deleted"}), 200

# This route renders this template and passes the necessary data
@app.route('/manage_products')
def manage_products():
    products_list = get_products()  # Fetch products from the database or other sources
    orders_list = get_orders()  # Fetch orders from the database or other sources
    return render_template('Product_Orders.html', products=products_list, orders=orders_list)



#######################
### Purchase Routes ###
#######################
# Get all purchases
@app.route('/purchases', methods=['GET'])
def get_purchases():
    purchases = Purchase.query.all()
    return jsonify([purchase.serialize() for purchase in purchases])

# Create a new purchase
@app.route('/purchases', methods=['POST'])
def add_purchase():
    customer_id = request.form['customer_id']

    new_purchase = Purchase(customer_id=customer_id)
    db.session.add(new_purchase)
    db.session.commit()

    return jsonify(new_purchase.serialize()), 201

# Get a specific purchase by ID
@app.route('/purchases/<int:purchase_id>', methods=['GET'])
def get_purchase(purchase_id):
    purchase = Purchase.query.get_or_404(purchase_id)
    return jsonify(purchase.serialize())

# Update an existing purchase
@app.route('/purchases/<int:purchase_id>', methods=['PUT'])
def update_purchase(purchase_id):
    purchase = Purchase.query.get_or_404(purchase_id)
    
    customer_id = request.form['customer_id']

    purchase.customer_id = customer_id

    db.session.commit()
    return jsonify(purchase.serialize())

# Delete a purchase
@app.route('/purchases/<int:purchase_id>', methods=['DELETE'])
def delete_purchase(purchase_id):
    purchase = Purchase.query.get_or_404(purchase_id)
    db.session.delete(purchase)
    db.session.commit()

    return jsonify({"message": "Purchase deleted"}), 200

###########################
### PurchaseItem Routes ###
###########################

# Get all purchase items
@app.route('/purchase_items', methods=['GET'])
def get_purchase_items():
    purchase_items = PurchaseItem.query.all()
    return jsonify([purchase_item.serialize() for purchase_item in purchase_items])

# Create a new purchase item
@app.route('/purchase_items', methods=['POST'])
def add_purchase_item():
    purchase_id = request.form['purchase_id']
    product_id = request.form['product_id']
    quantity = request.form['quantity']

    new_purchase_item = PurchaseItem(purchase_id=purchase_id, product_id=product_id, quantity=quantity)
    db.session.add(new_purchase_item)
    db.session.commit()

    return jsonify(new_purchase_item.serialize()), 201

# Get a specific purchase item by ID
@app.route('/purchase_items/<int:purchase_item_id>', methods=['GET'])
def get_purchase_item(purchase_item_id):
    purchase_item = PurchaseItem.query.get_or_404(purchase_item_id)
    return jsonify(purchase_item.serialize())

# Update an existing purchase item
@app.route('/purchase_items/<int:purchase_item_id>', methods=['PUT'])
def update_purchase_item(purchase_item_id):
    purchase_item = PurchaseItem.query.get_or_404(purchase_item_id)
    
    purchase_id = request.form['purchase_id']
    product_id = request.form['product_id']
    quantity = request.form['quantity']

    purchase_item.purchase_id = purchase_id
    purchase_item.product_id = product_id
    purchase_item.quantity = quantity

    db.session.commit()
    return jsonify(purchase_item.serialize())

# Delete a purchase item
@app.route('/purchase_items/<int:purchase_item_id>', methods=['DELETE'])
def delete_purchase_item(purchase_item_id):
    purchase_item = PurchaseItem.query.get_or_404(purchase_item_id)
    db.session.delete(purchase_item)
    db.session.commit()

    return jsonify({"message": "Purchase item deleted"}), 200

#######################
### Topping Routes  ###
#######################

# Get all toppings
@app.route('/toppings', methods=['GET'])
def get_toppings():
    toppings = Topping.query.all()
    return jsonify([topping.serialize() for topping in toppings])

# Create a new topping
@app.route('/toppings', methods=['POST'])
def add_topping():
    topping_name = request.form['topping_name']
    price = request.form['price']

    new_topping = Topping(topping_name=topping_name, price=price)
    db.session.add(new_topping)
    db.session.commit()

    return jsonify(new_topping.serialize()), 201

# Get a specific topping by ID
@app.route('/toppings/<int:topping_id>', methods=['GET'])
def get_topping(topping_id):
    topping = Topping.query.get_or_404(topping_id)
    return jsonify(topping.serialize())

# Update an existing topping
@app.route('/toppings/<int:topping_id>', methods=['PUT'])
def update_topping(topping_id):
    topping = Topping.query.get_or_404(topping_id)
    
    topping_name = request.form['topping_name']
    price = request.form['price']

    topping.topping_name = topping_name
    topping.price = price

    db.session.commit()
    return jsonify(topping.serialize())

# Delete a topping
@app.route('/toppings/<int:topping_id>', methods=['DELETE'])
def delete_topping(topping_id):
    topping = Topping.query.get_or_404(topping_id)
    db.session.delete(topping)
    db.session.commit()

    return jsonify({"message": "Topping deleted"}), 200

##############################
### render template Routes ###
###     Sales Report       ###
##############################
@app.route('/sales-report')
def sales_report():
    # Connect to the SQLite database
    conn = sqlite3.connect('mydb.db') 
    c = conn.cursor()

    # Execute a query to fetch data from the sales_report view
    c.execute('SELECT * FROM sales_report')
    db_orders = c.fetchall()

    # Close the connection
    conn.close()

    # Create a list of orders based on the data fetched from the database
    orders = []
    for order in db_orders:
        orders.append({
            'id': order[0],
            'purchase_date': order[1],
            'name': order[2],
            'email': order[3],
            'product_name': order[4],
            'quantity': order[5],
            'price': order[6],
            'total_price': order[7]
        })

    return render_template('salesReport.html', orders=orders)


#############################
### ProductTopping Routes ###
#############################
# Get all product-toppings
@app.route('/product_toppings', methods=['GET'])
def get_product_toppings():
    product_toppings = ProductTopping.query.all()
    return jsonify([product_topping.serialize() for product_topping in product_toppings])

# Create a new product-topping association
@app.route('/product_toppings', methods=['POST'])
def add_product_topping():
    product_id = request.form['product_id']
    topping_id = request.form['topping_id']

    new_product_topping = ProductTopping(product_id=product_id, topping_id=topping_id)
    db.session.add(new_product_topping)
    db.session.commit()

    return jsonify(new_product_topping.serialize()), 201

# Get a specific product-topping association by product_id and topping_id
@app.route('/product_toppings/<int:product_id>/<int:topping_id>', methods=['GET'])
def get_product_topping(product_id, topping_id):
    product_topping = ProductTopping.query.filter_by(product_id=product_id, topping_id=topping_id).first_or_404()
    return jsonify(product_topping.serialize())

# Delete a product-topping association
@app.route('/product_toppings/<int:product_id>/<int:topping_id>', methods=['DELETE'])
def delete_product_topping(product_id, topping_id):
    product_topping = ProductTopping.query.filter_by(product_id=product_id, topping_id=topping_id).first_or_404()
    db.session.delete(product_topping)
    db.session.commit()

    return jsonify({"message": "Product-Topping association deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)

def register_routes(app):
    # Register all your routes here
    # For example: 
    app.add_url_rule('/login', 'login', login, methods=['GET', 'POST'])

