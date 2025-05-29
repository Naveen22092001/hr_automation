from pymongo import MongoClient
from flask import jsonify, request
from pymongo import MongoClient

def get_inventory_collection():
    client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
    db = client["Timesheet"]
    return db["Employee_Inventory_details"]

def fetch_all_inventory_details():
    """
    Fetch and format inventory data from the Employee_Inventory_details collection.
    Returns:
        List[Dict]: A list of formatted inventory dictionaries.
    """
    collection = get_inventory_collection()
    raw_data = list(collection.find({}, {"_id": 0}))  # Exclude MongoDB _id

    formatted_data = [
        {"inventory": employee}
        for employee in raw_data
    ]
    return formatted_data

def add_available_inventory():
    """
    Adds or increments an item in the Available_inventory collection.
    Expects JSON with 'action', 'item', and 'quantity'.
    """
    try:
        data = request.get_json()
        action = data.get("action")
        item = data.get("item")
        quantity = data.get("quantity")

        if not all([action, item, quantity]):
            return jsonify({"success": False, "message": "Missing required fields"}), 400

        if action != "add":
            return jsonify({"success": False, "message": "Unsupported action"}), 400

        # MongoDB connection and collection
        client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
        db = client["Timesheet"]
        collection = db["Available_Inventory"]

        # Increment or add the item
        collection.update_one(
            {},  # Using a single document to track all inventory items
            {"$inc": {item: quantity}},
            upsert=True
        )

        return jsonify({"success": True, "message": f"{item} added with quantity {quantity}"}), 200

    except Exception as e:
        return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500


# def fetch_available_inventory_data():
#     """
#     Connects to MongoDB and retrieves all available inventory items from the Available_Inventory collection.
#     Returns:
#         List[Dict]: A list of available inventory items without MongoDB _id field.
#     """
#     client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
#     db = client["Timesheet"]
#     collection = db["Available_Inventory"]

#     # Fetch all inventory items and exclude the _id field
#     inventory_data = list(collection.find({}, {"_id": 0}))
#     return inventory_data

def fetch_available_inventory_data():
    """
    Connects to MongoDB and retrieves all available inventory items from the Available_Inventory collection.
    Returns:
        Dict: A dictionary mapping item names to their quantities.
    """
    client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
    db = client["Timesheet"]
    collection = db["Available_Inventory"]

    inventory_data = collection.find({})
    inventory_dict = {}

    for item in inventory_data:
        for key, value in item.items():
            if key != "_id":
                inventory_dict[key] = value

    return inventory_dict