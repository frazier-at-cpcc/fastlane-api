from flask import Flask, jsonify
import requests

app = Flask(__name__)

# Endpoint to fetch and format product categories
@app.route('/api/product-categories', methods=['GET'])
def get_product_categories():
    url = 'https://www.fastlaneus.com/api/ProductCategories'
    response = requests.get(url)
    
    if response.status_code != 200:
        return jsonify({'error': 'Failed to fetch product categories data'}), response.status_code
    
    data = response.json()
    product_categories = []

    def extract_categories(categories, parent_id=None):
        for category in categories.values():
            category_info = {
                'id': category.get('id'),
                'name': category.get('name', ''),
                'shortcut': category.get('shortcut', ''),
                'parent_id': parent_id
            }
            product_categories.append(category_info)
            if 'productcategories' in category:
                extract_categories(category['productcategories'], parent_id=category['id'])

    if 'data' in data and 'productcategories' in data['data']:
        extract_categories(data['data']['productcategories'])

    return jsonify(product_categories)

# Endpoint to fetch and format course data
@app.route('/api/products', methods=['GET'])
def get_products():
    url = 'https://www.fastlaneus.com/api/Products?limit=0'
    response = requests.get(url)
    
    if response.status_code != 200:
        return jsonify({'error': 'Failed to fetch products data'}), response.status_code
    
    data = response.json()
    products = []

    for product in data['data']:
        product_info = {
            'product_id': product.get('productid'),
            'category_id': product.get('categoryid'),
            'modality': product.get('modality'),
            'active': product.get('active'),
            'language': product.get('language'),
            'title': product.get('title'),
            'product_code': product.get('productcode'),
            'vendor_code': product.get('vendorcode'),
            'vendor_name': product.get('vendorname'),
            'url': product.get('url'),
            'objective': product.get('objective_plain'),
            'essentials': product.get('essentials_plain'),
            'audience': product.get('audience_plain'),
            'outline': product.get('outline_plain'),
            'summary': product.get('summary_plain'),
            'course_duration': product.get('duration', {}).get('formatted'),
            'last_changed': product.get('lastchanged')
        }
        products.append(product_info)

    return jsonify(products)

# Endpoint to correlate product IDs with category IDs
@app.route('/api/product-category-lookup', methods=['GET'])
def get_product_category_correlation():
    url = 'https://www.fastlaneus.com/api/Products?limit=0'
    response = requests.get(url)
    
    if response.status_code != 200:
        return jsonify({'error': 'Failed to fetch products data'}), response.status_code
    
    data = response.json()
    correlation_data = []

    # Extract product ID and category ID for each product
    for product in data['data']:
        correlation_info = {
            'product_id': product.get('productid'),
            'category_id': product.get('categoryid')
        }
        correlation_data.append(correlation_info)

    return jsonify(correlation_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
