from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS
import logging
import os
from user_side import employee_login, submit_inventory_request

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
    
@application.route("/api/inventory-request", methods=["POST"])
def api_inventory_request():
    data = request.json
    result = submit_inventory_request(
        employee_name=data["employee_name"],
        item_name=data["item_name"],
        quantity=data["quantity"],
        request_reason=data["request_reason"]
    )
    return jsonify(result)
###########################################################################################################

