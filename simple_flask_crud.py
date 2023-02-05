from flask import Flask, request
from flask_restful import Api, Resource
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'project_manager'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Initialize MySQL
mysql = MySQL(app)

# Initialize Flask-RESTful
api = Api(app)

# Define a Product resource
class Product(Resource):
    def get(self, id=None):
        # Get all products
        if id is None:
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM product_master")
            products = cur.fetchall()
            cur.close()
            print("working")
            return {'products': [dict(row) for row in products]}
        else:
            # Get a single product
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM product_master WHERE id=%s", (id,))
            product = cur.fetchone()
            cur.close()
            return product
    
    def post(self):
        # Create a new product
        data = request.get_json()
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO product_master (name) VALUES (%s)", (data['name']))
        mysql.connection.commit()
        cur.close()
        return {'message': 'Product created successfully'}, 201

    def put(self, id):
        # Update an existing product
        data = request.get_json()
        cur = mysql.connection.cursor()
        cur.execute("UPDATE product_master SET name=%s WHERE id=%s", (data['name'], id))
        mysql.connection.commit()
        cur.close()
        return {'message': 'Product updated successfully'}, 200

    def delete(self, id):
        # Delete a product
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM product_master WHERE id=%s", (id,))
        mysql.connection.commit()
        cur.close()
        return {'message': 'Product deleted successfully'}, 200

# Add the Product resource to the API
api.add_resource(Product, '/api/products', '/api/products/<int:id>')

if __name__ == '__main__':
    app.run(debug=True)
