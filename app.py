import json
import requests
from flask import Flask, jsonify

app = Flask(__name__)

# Fast Lane API endpoint
FASTLANE_API_URL = "https://www.fastlaneus.com/api/ProductCategories"

def flatten_categories(data):
    """Flatten nested product categories and products into a single list."""
    flattened_data = []
    
    def recurse_categories(categories, parent_name=""):
        for category_id, category_info in categories.items():
            category_name = category_info.get("name", "")
            full_name = f"{parent_name} > {category_name}" if parent_name else category_name
            
            # Check if there are products in this category
            if "products" in category_info:
                for product_id, product_info in category_info["products"].items():
                    flattened_data.append({
                        "category": full_name,
                        "product_id": product_id,
                        "product_name": product_info.get("title", ""),
                        "product_code": product_info.get("productcode", ""),
                        "vendor_code": product_info.get("vendorcode", "")
                    })
            
            # Recurse into sub-categories if they exist
            if "productcategories" in category_info:
                recurse_categories(category_info["productcategories"], full_name)

    # Start recursion
    recurse_categories(data["data"]["productcategories"])
    return flattened_data

@app.route('/api/product_categories', methods=['GET'])
def get_product_categories():
    response = requests.get(FASTLANE_API_URL)
    if response.status_code == 200:
        data = response.json()
        flattened_data = flatten_categories(data)
        return jsonify(flattened_data)
    else:
        return jsonify({"error": "Failed to fetch data from Fast Lane API"}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)
