import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

class Product(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="Price cannot be blank."
    )
    #@jwt_required()
    def get(self, name):
        product = self.find_by_name(name)
        if product:
            return product
        return {'message': 'Product not found'}, 404

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM products WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()
        if row:
            return {'product': {'name': row[1], 'price': row[2]}}

    def post(self, name):
        if self.find_by_name(name):
            return {'message': "An item with name '{}' already exists".format(name)}, 400

        data = Product.parser.parse_args()

        product = {'name': name, 'price': data['price']}

        try:
            self.insert(product)
        except:
            return {'message': 'Error occured inserting the item.'}, 500

        return product, 201

    @classmethod
    def insert(cls, product):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO products VALUES(NULL, ?, ?)"
        cursor.execute(query, (product['name'], product['price'])) #todo remove args
        connection.commit()
        connection.close()

    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "DELETE FROM products WHERE name=?"

        cursor.execute(query, (name,)) #todo remove args
        connection.commit()
        connection.close()
        return {'message': 'Item deleted'}

    def put(self, name):
        payload = Product.parser.parse_args()
        product = self.find_by_name(name)
        updated_product = {'name': name, 'price': payload['price']}

        if product is None:
            try:
                self.insert(updated_product)
            except:
                return {'message': 'An error occured inserting the item'}, 500
        else:
            try:
                self.update(updated_product)
            except:
                return {'message': 'An error occured updating the item'}, 500

        return updated_product

    @classmethod
    def update(cls, product):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "UPDATE products SET price=? WHERE name=?"

        cursor.execute(query, (product['price'], product['name'])) #todo remove args
        connection.commit()
        connection.close()

class ProductList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM products"
        result = cursor.execute(query)
        products = []
        for row in result:
            products.append({'name': row[0], 'price': row[1]})

        connection.commit()
        connection.close()

        return {'products': products}
