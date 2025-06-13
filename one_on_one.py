# from pymongo import MongoClient

# def get_one_on_one_mapping():
#     client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
#     db = client["Timesheet"]
#     employees = db.Employee_meetingdetails.find()

#     manager_map = {}
#     for emp in employees:
#         manager = emp.get("manager")
#         employee_name = emp.get("name")
#         designation = emp.get("designation", "")
#         if manager:
#             manager_map.setdefault(manager, []).append({
#                 "name": employee_name,
#                 "designation": designation
#             })
#     return manager_map


# def save_meeting(data):
#     client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
#     db = client["Timesheet"]

#     manager = data["manager_name"]
#     employee = data["employee_name"]
#     designation = data["designation"]
#     month = data["month"]
#     year = int(data["year"])
#     date = data["date"]

#     status_doc = db.One_on_one_status.find_one({
#         "manager": manager,
#         "month": month,
#         "year": year
#     })

#     if status_doc:
#         for emp in status_doc.get("employees", []):
#             if emp["name"] == employee:
#                 return False, "This one-on-one meeting record already exists"

#         db.One_on_one_status.update_one(
#             {"manager": manager, "month": month, "year": year},
#             {"$push": {
#                 "employees": {
#                     "name": employee,
#                     "designation": designation,
#                     "status": "completed",
#                     "date": date
#                 }
#             }}
#         )
#     else:
#         db.One_on_one_status.insert_one({
#             "manager": manager,
#             "month": month,
#             "year": year,
#             "employees": [{
#                 "name": employee,
#                 "designation": designation,
#                 "status": "completed",
#                 "date": date
#             }]
#         })
#     return True, "One-on-one meeting saved successfully"


# def get_meeting_status(manager_name, month, year):
#     client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
#     db = client["Timesheet"]

#     static_employees = list(db.Employee_meetingdetails.find({"manager": manager_name}))
#     meeting_doc = db.One_on_one_status.find_one({
#         "manager": manager_name,
#         "month": month,
#         "year": int(year)
#     })

#     completed_lookup = {
#         emp["name"]: True
#         for emp in meeting_doc.get("employees", [])
#         if emp.get("status") == "completed"
#     } if meeting_doc else {}

#     result = []
#     for emp in static_employees:
#         name = emp.get("name")
#         status = "completed" if name in completed_lookup else "pending"
#         result.append({
#             "name": name,
#             "designation": emp.get("designation", ""),
#             "manager": emp.get("manager", ""),
#             "status": status
#         })

#     return {
#         "manager": manager_name,
#         "month": month,
#         "year": year,
#         "employees": result
#     }
