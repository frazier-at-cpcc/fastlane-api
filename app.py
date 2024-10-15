from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Define the base URL for the external API
FAST_LANE_API_URL = "https://www.fastlaneus.com/api/ProductCategories"

# Endpoint to retrieve all top-level categories
@app.route('/categories', methods=['GET'])
def get_categories():
    response = requests.get(FAST_LANE_API_URL)
    if response.status_code == 200:
        data = response.json()
        categories = data.get("data", {}).get("productcategories", {})
        # Only include top-level categories
        return jsonify(categories)
    return jsonify({'error': 'Failed to retrieve categories'}), response.status_code

# Endpoint to retrieve a specific category and its subcategories
@app.route('/categories/<int:id>', methods=['GET'])
def get_category(id):
    response = requests.get(FAST_LANE_API_URL)
    if response.status_code == 200:
        data = response.json()
        category = data.get("data", {}).get("productcategories", {}).get(str(id))
        if category:
            return jsonify(category)
        else:
            return jsonify({'error': 'Category not found'}), 404
    return jsonify({'error': 'Failed to retrieve categories'}), response.status_code

# Endpoint to retrieve all products within a specific category or subcategory
@app.route('/categories/<int:id>/products', methods=['GET'])
def get_category_products(id):
    response = requests.get(FAST_LANE_API_URL)
    if response.status_code == 200:
        data = response.json()
        category = data.get("data", {}).get("productcategories", {}).get(str(id))
        if category:
            products = extract_products(category)
            return jsonify(products)
        else:
            return jsonify({'error': 'Category not found'}), 404
    return jsonify({'error': 'Failed to retrieve categories'}), response.status_code

# Helper function to extract products from nested categories
def extract_products(category):
    products = category.get("products", {})
    subcategories = category.get("productcategories", {})
    for sub_id, subcategory in subcategories.items():
        products.update(extract_products(subcategory))
    return products

# Endpoint to retrieve details about a specific product
@app.route('/products/<int:productid>', methods=['GET'])
def get_product(productid):
    response = requests.get(FAST_LANE_API_URL)
    if response.status_code == 200:
        data = response.json()
        products = extract_all_products(data.get("data", {}).get("productcategories", {}))
        product = products.get(str(productid))
        if product:
            return jsonify(product)
        else:
            return jsonify({'error': 'Product not found'}), 404
    return jsonify({'error': 'Failed to retrieve products'}), response.status_code

# Helper function to extract all products
def extract_all_products(categories):
    products = {}
    for id, category in categories.items():
        products.update(category.get("products", {}))
        subcategories = category.get("productcategories", {})
        products.update(extract_all_products(subcategories))
    return products

# Endpoint to search products by title, product code, or vendor code
@app.route('/products/search', methods=['GET'])
def search_products():
    query = request.args.get('query', '').lower()
    response = requests.get(FAST_LANE_API_URL)
    if response.status_code == 200:
        data = response.json()
        products = extract_all_products(data.get("data", {}).get("productcategories", {}))
        filtered_products = {id: product for id, product in products.items()
                             if query in product.get('title', '').lower() or
                             query in product.get('productcode', '').lower() or
                             query in product.get('vendorcode', '').lower()}
        return jsonify(filtered_products)
    return jsonify({'error': 'Failed to retrieve products'}), response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
