from flask import Flask, jsonify
import requests

app = Flask(__name__)

# Endpoint to fetch and format product categories
@app.route('/api/product-categories', methods=['GET'])
def get_product_categories():
    # URL for fetching the product categories data
    url = 'https://www.fastlaneus.com/api/ProductCategories'
    
    # Make a GET request to fetch data from the URL
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code != 200:
        return jsonify({'error': 'Failed to fetch data'}), response.status_code
    
    # Parse the JSON response
    data = response.json()
    product_categories = []

    # Function to recursively extract product category details
    def extract_categories(categories):
        for category in categories.values():
            category_info = {
                'id': category.get('id'),
                'name': category.get('name', ''),
                'shortcut': category.get('shortcut', '')
            }
            product_categories.append(category_info)

            # If there are nested product categories, extract them too
            if 'productcategories' in category:
                extract_categories(category['productcategories'])

    # Start the extraction from the top-level categories
    if 'data' in data and 'productcategories' in data['data']:
        extract_categories(data['data']['productcategories'])

    # Return the extracted categories as JSON
    return jsonify(product_categories)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
