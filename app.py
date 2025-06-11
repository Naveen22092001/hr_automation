from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS
import logging
import os
from meetings import fetch_meetings_for_month, save_meeting_status
from one_on_one import save_meeting_to_db,save_performance_meeting_to_db
from user_side import add_inventory, delete_inventory, edit_inventory, employee_login, get_inventory, submit_inventory_request
from admin_side import add_available_inventory, delete_inventory_items, edit_inventory_item, fetch_all_inventory_details, fetch_available_inventory_data, get_inventory_collection, modify_available_inventory
application = Flask(__name__)

# Logging setup
CORS(application)


@application.route("/")
def home():
    return jsonify({"message": "Backend is running successfully!"})
###########################################################################

# Route to fetch all available API routes
@application.route("/api/routes", methods=["GET"])
def get_routes():
    return jsonify([str(rule) for rule in application.url_map.iter_rules()])
logging.basicConfig(level=logging.DEBUG)
#############################################################################################

@application.route("/api/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("email")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    user_data = employee_login(username, password)  # Check credentials

    if user_data:
        if username =="admin":
            return jsonify({"user": user_data, "message": "Admin login successful"}), 200
        else:
            return jsonify({"user": user_data, "message": "Login successful"}), 200
    else:
        return jsonify({"error": "Invalid username or password"}), 401
######################################################################################################
    
@application.route("/api/inventory_request", methods=["POST"])
def api_inventory_request():
    data = request.json
    employee_name = data.get("name")
    tool_needed = data.get("tool_needed")
    reason = data.get("reason")

    if not all([employee_name, tool_needed, reason]):
        return jsonify({"error": "Missing required fields"}), 400

    result = submit_inventory_request(employee_name, tool_needed, reason)
    return jsonify(result), 200
###########################################################################################################
@application.route('/api/inventory_details', methods=['GET', 'POST'])
def inventory_details():
    if request.method == 'GET':
        return get_inventory()

    data = request.get_json()

    if request.method == 'POST':
        return add_inventory(data)
    # elif request.method == 'PUT':
    #     return edit_inventory(data)
    # elif request.method == 'DELETE':
    #     return delete_inventory(data)

    logging.warning("Invalid HTTP method used on /api/inventory_details endpoint.")
    return jsonify({"success": False, "message": "Invalid request method"}), 405
    
###################################################################################################################
#This is used to get the inventory details in admin side of the employees
@application.route('/api/inventory_management', methods=['GET'])
def get_inventory_management():
    try:
        name = request.args.get("name")
        if name:
            # If name is provided, return a single employee's inventory
            collection = get_inventory_collection()
            employee = collection.find_one({"name": name}, {"_id": 0, "name": 1, "inventory_details": 1})
            if not employee:
                return jsonify({"success": False, "message": "Employee not found"}), 404
            return jsonify({"success": True, "inventory": employee}), 200
        else:
            # Otherwise, return all inventory records
            inventories = fetch_all_inventory_details()
            return jsonify({"inventories": inventories}), 200
    except Exception as e:
        return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500
    
######################################################################################################################
@application.route('/api/inventory_management', methods=['POST'])
def handle_inventory_management():
    return add_available_inventory()
######################################################################################################################

@application.route('/api/inventory_available', methods=['GET'])
def get_available_inventory():
    try:
        inventory = fetch_available_inventory_data()
        return jsonify({
            "success": True,
            "inventory": inventory
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Server error: {str(e)}"
        }), 500
    
########################################################################################################################
@application.route('/api/inventory_available', methods=['POST'])
def handle_inventory_modification():
    return modify_available_inventory()
##########################################################################################################################
@application.route("/api/inventory_management", methods=["PUT", "DELETE"])
def inventory_management():
    data = request.get_json()
    name = data.get("name")

    if request.method == "PUT":
        action = data.get("action")
        original_item = data.get("original_item")
        new_item = data.get("item")
        quantity = data.get("quantity")

        if action != "edit" or not all([name, original_item, new_item, quantity is not None]):
            return jsonify({"success": False, "message": "Invalid PUT data"}), 400

        result, status_code = edit_inventory_item(name, original_item, new_item, quantity)
        return jsonify(result), status_code

    elif request.method == "DELETE":
        inventory_details = data.get("inventory_details")
        if not inventory_details or not isinstance(inventory_details, dict):
            return jsonify({"success": False, "message": "Invalid DELETE payload"}), 400

        result, status_code = delete_inventory_items(name, inventory_details)
        return jsonify(result), status_code

    return jsonify({"success": False, "message": "Unsupported HTTP method"}), 405
#####################################################################################################################################

# @application.route("/api/one_on_one_meetings", methods=["GET"])
# def get_all_meeting_details():
#     client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
#     db = client["Timesheet"]
#     collection = db["Employee_meetingdetails"]

#     meetings = list(collection.find({}, {"_id": 0}))  # Exclude _id from results

#     return jsonify({"meetings": meetings}), 200


# @application.route("/api/performance_meetings", methods=["GET"])
# def get_all_performance_meeting_details():
#     client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
#     db = client["Timesheet"]
#     collection = db["Employee_performance_meeting"]

#     meetings = list(collection.find({}, {"_id": 0}))  # Exclude _id from results

#     return jsonify({"meetings": meetings}), 200

# @application.route("/api/one_on_one_meetings", methods=["POST"])
# def save_one_on_one_meeting():
#     data = request.get_json()
#     response, status_code = save_meeting_to_db(data)
#     return jsonify(response), status_code

# @application.route("/api/performance_meetings", methods=["POST"])
# def save_performance_meeting():
#     data = request.get_json()
#     response, status_code =save_performance_meeting_to_db(data)
#     return jsonify(response), status_code

@application.route("/api/one_on_one_meetings", methods=["GET"])
def api_get_meetings():
    manager = request.args.get("manager")  # optional filter
    month   = request.args.get("month")
    year    = request.args.get("year")

    if not (month and year):
        return jsonify({"error": "month & year query params are required"}), 400

    data = fetch_meetings_for_month(manager, month, year)
    return jsonify({"meetings": data}), 200


# -------- POST /api/one_on_one_meetings --------------------------------
@application.route("/api/one_on_one_meetings", methods=["POST"])
def api_save_status():
    payload = request.get_json() or {}
    resp, code = save_meeting_status(payload)
    return jsonify(resp), code