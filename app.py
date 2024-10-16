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

# Endpoint to fetch product-category lookup
@app.route('/api/product-category-lookup', methods=['GET'])
def get_product_category_lookup():
    url = 'https://www.fastlaneus.com/api/ProductCategories'
    response = requests.get(url)
    
    if response.status_code != 200:
        return jsonify({'error': 'Failed to fetch product categories data'}), response.status_code
    
    data = response.json()
    product_category_lookup = []

    def extract_product_category(categories):
        for category in categories.values():
            category_id = category.get('id')
            
            # Extract each product under the current category
            if 'products' in category:
                for product in category['products'].values():
                    product_category_lookup.append({
                        'product_id': product.get('productid'),
                        'category_id': category_id
                    })

            # Recursively check nested categories
            if 'productcategories' in category:
                extract_product_category(category['productcategories'])

    # Start the extraction from the top-level categories
    if 'data' in data and 'productcategories' in data['data']:
        extract_product_category(data['data']['productcategories'])

    return jsonify(product_category_lookup)
    
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

@app.route('/api/events-lookup', methods=['GET'])
def get_events_lookup():
    url = 'https://www.fastlaneus.com/api/Events?country=US&limit=0'
    response = requests.get(url)
    
    if response.status_code != 200:
        return jsonify({'error': 'Failed to fetch events data'}), response.status_code
    
    data = response.json()
    events_data = []

    # Extract necessary event details
    for event in data['data']:
        event_info = {
            'event_id': event.get('eventid'),
            'product_id': event.get('productid'),
            'facility_id': event.get('facilityid'),
            'country_code': event.get('country'),
            'language': event.get('language'),
            'plm': event.get('plm'),
            'product_version': event.get('productversion'),
            'start_date': event.get('start'),
            'start_time': event.get('starttime'),
            'end_date': event.get('end'),
            'end_time': event.get('endtime'),
            'status': event.get('status'),
            'timezone': event.get('timezone'),
            'max_participants': event.get('maxparticipants'),
            'free_seats': event.get('freeseats'),
            'vlearning': event.get('vlearning'),
            'reseller': event.get('reseller'),
            'reseller_name': event.get('resellername'),
            'last_changed': event.get('lastchanged')
        }
        events_data.append(event_info)

@app.route('/api/facilities', methods=['GET'])
def get_facilities():
    url = 'https://www.fastlaneus.com/api/Facilities?country=US&limit=0'
    response = requests.get(url)
    
    if response.status_code != 200:
        return jsonify({'error': 'Failed to fetch facilities data'}), response.status_code
    
    data = response.json()
    facilities_data = []

    # Extract necessary facility details
    for facility in data['data']:
        facility_info = {
            'facility_id': facility.get('facilityid'),
            'country_code': facility.get('country'),
            'title': facility.get('title'),
            'company': facility.get('company'),
            'street': facility.get('street'),
            'postcode': facility.get('postcode'),
            'town': facility.get('town'),
            'state_abbr': facility.get('stateabbr'),
            'state_name': facility.get('statename'),
            'metro_code': facility.get('metrocode'),
            'metro_name': facility.get('metroname'),
            'timezone': facility.get('timezone'),
            'last_changed': facility.get('lastchanged')
        }
        facilities_data.append(facility_info)

    return jsonify(facilities_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
