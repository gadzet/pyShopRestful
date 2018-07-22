from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.product import Product, ProductList

app = Flask(__name__)
app.secret_key = 'longandcomplicated'
api = Api(app)

jwt = JWT(app, authenticate, identity)

api.add_resource(ProductList, '/products')
api.add_resource(Product, '/product/<string:name>')
api.add_resource(UserRegister, '/register')

app.run(port=5000, debug=True)
