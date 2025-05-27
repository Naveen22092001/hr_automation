import logging
from flask import jsonify
from pymongo import MongoClient

from mail import send_inventory_email_to_manager

def employee_login(emp_name,emp_password):
    client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
    db = client["Timesheet"]
    collection = db["Employee_credentials"]
    user = collection.find_one({"Username": emp_name}) 
    #for data in user:
    username = user["Username"]
    password = user["Password"]
    if username==emp_name and password==emp_password:
        if username=="admin":
    #if user and check_password_hash(user["Password"], emp_password):  # Verify hashed password
            return {"Username": user["Username"], "message": "Admin login successful"}
        else:
            return {"Username":user["Username"],"message":"Login successful"}   
    else:
        return None
    
def get_manager_details(emp_name):
    client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
    db = client["Timesheet"]
    collection = db["Employee_data"]
    data = collection.find_one({"name": emp_name})
    if data:
        return data.get("manager"), data.get("manager_email")
    else:
        print(f"No manager found for employee: {emp_name}")
        return None, None
    
    
def submit_inventory_request(employee_name, tool_needed, reason):
    client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
    db = client["Timesheet"]
    collection = db["Inventory_requests"]

    request_data = {
        "employee_name": employee_name,
        "tool_needed": tool_needed,
        "reason": reason
    }

    collection.insert_one(request_data)

    manager_name, manager_email = get_manager_details(employee_name)
    if manager_name and manager_email:
        send_inventory_email_to_manager(
            employee_name,
            tool_needed,
            reason,
            manager_name,
            manager_email
        )

    return {"message": "Inventory request submitted successfully", "request": request_data}


def get_inventory_collection():
    client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
    db = client["Timesheet"]
    return db["Employee_Inventory_details"]

# Fetch all inventory items
def get_inventory():
    logging.info("Fetching all inventory items from the database.")
    collection = get_inventory_collection()
    items = list(collection.find({}, {"_id": 0}))
    logging.info(f"{len(items)} inventory items retrieved.")
    return jsonify({"assets": items})

# Add a new inventory item
def add_inventory(data):
    item_name = data.get("item")
    quantity = data.get("quantity")
    logging.info(f"Adding new inventory item: {item_name} with quantity: {quantity}")

    collection = get_inventory_collection()
    if collection.find_one({"item": item_name}):
        logging.warning(f"Item '{item_name}' already exists in inventory.")
        return jsonify({"success": False, "message": "Item already exists"}), 400

    collection.insert_one({"item": item_name, "quantity": quantity})
    logging.info(f"Item '{item_name}' added successfully to inventory.")
    return jsonify({"success": True, "asset": {"item": item_name, "quantity": quantity}})

# Update an existing inventory item
def edit_inventory(data):
    item_name = data.get("item")
    quantity = data.get("quantity")
    logging.info(f"Updating inventory item: {item_name} to new quantity: {quantity}")

    collection = get_inventory_collection()
    result = collection.update_one({"item": item_name}, {"$set": {"quantity": quantity}})
    if result.matched_count == 0:
        logging.error(f"Item '{item_name}' not found in inventory for update.")
        return jsonify({"success": False, "message": "Item not found"}), 404

    logging.info(f"Inventory item '{item_name}' updated successfully.")
    return jsonify({"success": True, "message": "Asset updated"})

# Delete an inventory item
def delete_inventory(data):
    item_name = data.get("item")
    logging.info(f"Deleting inventory item: {item_name}")

    collection = get_inventory_collection()
    result = collection.delete_one({"item": item_name})
    if result.deleted_count == 0:
        logging.error(f"Item '{item_name}' not found in inventory for deletion.")
        return jsonify({"success": False, "message": "Item not found"}), 404

    logging.info(f"Inventory item '{item_name}' deleted successfully.")
    return jsonify({"success": True, "deleted_item": item_name})