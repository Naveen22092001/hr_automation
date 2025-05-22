from pymongo import MongoClient

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
    
def submit_inventory_request(employee_name, item_name, quantity, request_reason):
    client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
    db = client["Timesheet"]
    collection = db["Inventory_requests"]

    request_data = {
        "employee_name": employee_name,
        "item_name": item_name,
        "quantity": quantity,
        "request_reason": request_reason
    }

    collection.insert_one(request_data)
    return {"message": "Inventory request submitted successfully", "request": request_data}
    