from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from forms import LoginForm

import models
import routes

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
db = SQLAlchemy(app)

# Call the create_models function to define the models with the `db` object
Customer, Employee, Product, Purchase, PurchaseItem, Topping, ProductTopping = models.create_models(db)

# Register routes with the app
routes.register_routes(app)

# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User Loader
@login_manager.user_loader
def load_user(employee_id):
    return Employee.query.get(int(employee_id))

if __name__ == '__main__':
    app.run(debug=True)