from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory data store (for demonstration purposes)
# In a real application, you'd use a database.
items = [
    {"id": 1, "name": "Item A", "description": "This is item A"},
    {"id": 2, "name": "Item B", "description": "This is item B"},
]
next_id = 3

@app.route('/')
def home():
    """
    A simple home endpoint.
    """
    return "Welcome to the Flask API!"

@app.route('/items', methods=['GET'])
def get_items():
    """
    Retrieves all items.
    """
    return jsonify(items)

@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    """
    Retrieves a single item by its ID.
    """
    item = next((item for item in items if item['id'] == item_id), None)
    if item:
        return jsonify(item)
    return jsonify({"message": "Item not found"}), 404

@app.route('/items', methods=['POST'])
def create_item():
    """
    Creates a new item.
    Expects JSON payload like: {"name": "New Item", "description": "Description"}
    """
    global next_id # Declare next_id as global to modify it

    if not request.is_json:
        return jsonify({"message": "Request must be JSON"}), 400

    data = request.get_json()

    if 'name' not in data or 'description' not in data:
        return jsonify({"message": "Missing 'name' or 'description' in request"}), 400

    new_item = {
        "id": next_id,
        "name": data['name'],
        "description": data['description']
    }
    items.append(new_item)
    next_id += 1
    return jsonify(new_item), 201 # 201 Created

@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    """
    Updates an existing item.
    Expects JSON payload like: {"name": "Updated Name", "description": "Updated Description"}
    """
    if not request.is_json:
        return jsonify({"message": "Request must be JSON"}), 400

    data = request.get_json()
    item = next((item for item in items if item['id'] == item_id), None)

    if not item:
        return jsonify({"message": "Item not found"}), 404

    item.update(data) # Update existing fields
    return jsonify(item)

@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    """
    Deletes an item by its ID.
    """
    global items
    original_len = len(items)
    items = [item for item in items if item['id'] != item_id]

    if len(items) < original_len:
        return jsonify({"message": "Item deleted successfully"}), 200
    return jsonify({"message": "Item not found"}), 404


if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)
