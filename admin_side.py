from pymongo import MongoClient

# # Add inventory items to the collection from the admin side
# def add_inventory_item(item_name, quantity):
#     try:
#         client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
#         db = client["Timesheet"]
#         collection = db["Inventory_stock"]
#         inventory_data = {
#             "item_name": item_name,
#             "quantity": quantity
#         }
#         collection.insert_one(inventory_data)
#         return {"message": "Inventory item added successfully", "item": inventory_data}
#     except Exception as e:
#         return {"error": f"Failed to add inventory item: {str(e)}"}

# # To get all the inventory item 
# def get_all_inventory_stock():
#     client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
#     db = client["Timesheet"]
#     collection = db["Inventory_stock"]
#     items = list(collection.find({}, {"_id": 0})) 
#     return items

# #To get all the inventory items in use
# def get_all_inventory_in_use():
#     client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
#     db = client["Timesheet"]
#     collection = db["Inventory_in_use"]
#     items = list(collection.find({}, {"_id": 0})) 
#     return items

# def assign_inventory_to_employee(employee_name, item_name, quantity):
#     client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
#     db = client["Timesheet"]
#     collection = db["Assigned_inventory"]

#     assigned_data = {
#         "employee_name": employee_name,
#         "item_name": item_name,
#         "quantity": quantity
#     }

#     collection.insert_one(assigned_data)
#     return {"message": "Inventory assigned successfully", "data": assigned_data}


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

from flask import jsonify, request
from pymongo import MongoClient

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


