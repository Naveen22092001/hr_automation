import datetime
from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS
import logging
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


###########################################################################################################################################
@application.route('/api/one_on_one_meetings', methods=['GET'])
def map_managers_to_employees():
    # Connect to MongoDB
    client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
    db = client["Timesheet"]

    # Fetch all employee records
    employees = db.Employee_meetingdetails.find()

    # Manager to employees map
    manager_map = {}

    for emp in employees:
        manager = emp.get("manager")
        employee_name = emp.get("name")
        designation = emp.get("designation", "")  # Default to empty string if not present

        if manager:
            if manager not in manager_map:
                manager_map[manager] = []

            # Add name + designation
            manager_map[manager].append({
                "name": employee_name,
                "designation": designation
            })

    return jsonify({
        "success": True,
        "manager_employee_map": manager_map
    })


@application.route("/api/performance_meetings", methods=['GET'])
def map_managers_to_employees_for_performance():
    # Connect to MongoDB
    client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
    db = client["Timesheet"]

    # Fetch all employee records
    employees = db.Employee_meetingdetails.find()

    # Manager to employees map
    manager_map = {}

    for emp in employees:
        manager = emp.get("manager")
        employee_name = emp.get("name")
        designation = emp.get("designation", "")  # Default to empty string if not present

        if manager:
            if manager not in manager_map:
                manager_map[manager] = []

            # Add name + designation
            manager_map[manager].append({
                "name": employee_name,
                "designation": designation
            })

    return jsonify({
        "success": True,
        "manager_employee_map": manager_map
    })


@application.route('/api/one_on_one_meetings', methods=['GET'])
def get_one_on_one_meetings():
    client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
    db = client["Timesheet"]

    # Get query params for filtering (optional but recommended)
    month = request.args.get('month')
    year = request.args.get('year')

    # Fetch static employee list
    employees = list(db.Employee_meetingdetails.find())

    # Fetch completed records
    completed = db.One_on_one_status.find({
        "month": month,
        "year": year
    })

    # Convert completed status to lookup
    completed_lookup = {
        (c['name'], c['month'], c['year']): c['isCompleted']
        for c in completed
    }

    # Combine both: static list + dynamic completion
    result = []
    for emp in employees:
        emp_name = emp.get("name")
        emp_manager = emp.get("manager")
        emp_designation = emp.get("designation")

        is_completed = completed_lookup.get((emp_name, month, year), False)

        result.append({
            "name": emp_name,
            "manager": emp_manager,
            "designation": emp_designation,
            "month": month,
            "year": year,
            "isCompleted": is_completed
        })

    return jsonify({
        "success": True,
        "meetings": result
    })


# @application.route('/api/one_on_one_meetings', methods=['POST'])
# def save_one_on_one_meetings():
#     data = request.get_json(force=True)

#     # Validate required fields
#     required = ["month", "year", "manager", "employees"]
#     if not all(key in data for key in required):
#         return jsonify({
#             "success": False,
#             "message": "Missing required fields: month, year, manager, employees"
#         }), 400

#     month = data["month"]
#     year = int(data["year"])
#     manager = data["manager"]
#     employees = data["employees"]

#     # Get today's date in YYYY-MM-DD format
#     today_date = datetime.today().strftime("%Y-%m-%d")

#     # Ensure each employee has a date (only date, no time)
#     for emp in employees:
#         emp["date"] = emp.get("date", today_date)

#     # Connect to MongoDB
#     client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
#     db = client["Timesheet"]

#     # Upsert (update if exists, insert if not)
#     result = db.One_on_one_status.update_one(
#         {"manager": manager, "month": month, "year": year},
#         {
#             "$set": {
#                 "employees": employees
#             }
#         },
#         upsert=True
#     )

#     return jsonify({
#         "success": True,
#         "message": "Saved successfully",
#         "updated": bool(result.modified_count),
#         "inserted": bool(result.upserted_id)
#     }), 200

@application.route('/api/one_on_one_meetings', methods=['POST'])
def save_one_on_one_meetings():
    data = request.get_json(force=True)

    # -------- validate body --------
    required = ["month", "year", "manager", "employees"]
    if not all(k in data for k in required):
        return jsonify({
            "success": False,
            "message": "Missing required fields: month, year, manager, employees"
        }), 400

    month     = data["month"]
    year      = int(data["year"])      # your sample body has "year" as string → convert to int
    manager   = data["manager"]
    employees = data["employees"]

    # -------- ensure each employee has a date (YYYY-MM-DD) --------
    today_str = datetime.today().strftime("%Y-%m-%d")
    for emp in employees:
        emp["date"] = emp.get("date", today_str)

    # -------- Mongo connection --------
    client = MongoClient(
        "mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/"
    )
    db = client["Timesheet"]

    # -------- upsert the record --------
    result = db.One_on_one_status.update_one(
        {"manager": manager, "month": month, "year": year},
        {"$set": {"employees": employees}},
        upsert=True
    )

    return jsonify({
        "success": True,
        "message": "Saved successfully",
        "updated": bool(result.modified_count),
        "inserted": bool(result.upserted_id)
    }), 200