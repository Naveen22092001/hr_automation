from pymongo import MongoClient

def save_meeting_to_db(data):
    client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
    db = client["Timesheet"]
    collection = db["Employee_meetingdetails"]

    required_fields = ["name", "manager", "month", "year", "isCompleted", "notes"]
    for field in required_fields:
        if field not in data:
            return {"error": f"'{field}' is required"}, 400

    collection.update_one(
        {"name": data["name"], "manager": data["manager"]},
        {"$set": {
            "month": data["month"],
            "year": data["year"],
            "isCompleted": data["isCompleted"],
            "notes": data["notes"]
        }},
        upsert=True
    )

    return {"message": "Meeting data saved successfully"}, 200

def save_performance_meeting_to_db(data):
    client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
    db = client["Timesheet"]
    collection = db["Employee_meetingdetails"]

    required_fields = ["name", "manager", "month", "year", "isCompleted", "notes"]
    for field in required_fields:
        if field not in data:
            return {"error": f"'{field}' is required"}, 400

    collection.update_one(
        {"name": data["name"], "manager": data["manager"]},
        {"$set": {
            "month": data["month"],
            "year": data["year"],
            "isCompleted": data["isCompleted"],
            "notes": data["notes"]
        }},
        upsert=True
    )

    return {"message": "Meeting data saved successfully"}, 200