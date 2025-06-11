# from pymongo import MongoClient

# def save_meeting_to_db(data):
#     client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
#     db = client["Timesheet"]
#     collection = db["Employee_meetingdetails"]

#     required_fields = ["name", "manager", "month", "year", "isCompleted", "notes"]
#     for field in required_fields:
#         if field not in data:
#             return {"error": f"'{field}' is required"}, 400

#     collection.update_one(
#         {"name": data["name"], "manager": data["manager"]},
#         {"$set": {
#             "month": data["month"],
#             "year": data["year"],
#             "isCompleted": data["isCompleted"],
#             "notes": data["notes"]
#         }},
#         upsert=True
#     )

#     return {"message": "Meeting data saved successfully"}, 200

# # Saves the performace meeting data status
# def save_performance_meeting_to_db(data):
#     client = MongoClient("mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/")
#     db = client["Timesheet"]
#     collection = db["Employee_performance_meeting"]

#     required_fields = ["name", "manager", "month", "year", "isCompleted", "notes"]
#     for field in required_fields:
#         if field not in data:
#             return {"error": f"'{field}' is required"}, 400

#     collection.update_one(
#         {"name": data["name"], "manager": data["manager"]},
#         {"$set": {
#             "month": data["month"],
#             "year": data["year"],
#             "isCompleted": data["isCompleted"],
#             "notes": data["notes"]
#         }},
#         upsert=True
#     )

#     return {"message": "Meeting data saved successfully"}, 200


# # # from pymongo import MongoClient, errors

# # # # ────────────────────────────────────────────────────────────────────────────────
# # # # One-on-one meeting helper
# # # # ────────────────────────────────────────────────────────────────────────────────
# # # def save_meeting_to_db(data: dict):
# # #     """
# # #     Upsert a one-on-one meeting document keyed by
# # #     (name, manager, month, year).

# # #     Returns (dict, http_code)
# # #     """
# # #     required = {"name", "manager", "month", "year", "isCompleted", "notes"}
# # #     if missing := required.difference(data):
# # #         # e.g. {'year'}  →  "'year' is required"
# # #         field = missing.pop()
# # #         return {"error": f"'{field}' is required"}, 400

# # #     try:
# # #         client = MongoClient(
# # #             "mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/"
# # #         )
# # #         collection = client["Timesheet"]["Employee_meetingdetails"]

# # #         # Upsert on the unique (name, manager, month, year) key
# # #         collection.update_one(
# # #             {
# # #                 "name":     data["name"],
# # #                 "manager":  data["manager"],
# # #                 "month":    data["month"],
# # #                 "year":     data["year"],
# # #             },
# # #             {
# # #                 "$set": {
# # #                     "isCompleted": data["isCompleted"],
# # #                     "notes":       data["notes"],
# # #                 }
# # #             },
# # #             upsert=True,
# # #         )
# # #         return {"message": "Meeting data saved/updated successfully"}, 200

# # #     except errors.PyMongoError as exc:
# # #         return {"error": str(exc)}, 500


# # # # ────────────────────────────────────────────────────────────────────────────────
# # # # Performance-meeting helper   (same idea, different collection)
# # # # ────────────────────────────────────────────────────────────────────────────────
# # # def save_performance_meeting_to_db(data: dict):
# # #     """
# # #     Upsert a performance-meeting document keyed by
# # #     (name, manager, month, year).

# # #     Returns (dict, http_code)
# # #     """
# # #     required = {"name", "manager", "month", "year", "isCompleted", "notes"}
# # #     if missing := required.difference(data):
# # #         field = missing.pop()
# # #         return {"error": f"'{field}' is required"}, 400

# # #     try:
# # #         client = MongoClient(
# # #             "mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/"
# # #         )
# # #         collection = client["Timesheet"]["Employee_performance_meeting"]

# # #         collection.update_one(
# # #             {
# # #                 "name":     data["name"],
# # #                 "manager":  data["manager"],
# # #                 "month":    data["month"],
# # #                 "year":     data["year"],
# # #             },
# # #             {
# # #                 "$set": {
# # #                     "isCompleted": data["isCompleted"],
# # #                     "notes":       data["notes"],
# # #                 }
# # #             },
# # #             upsert=True,
# # #         )
# # #         return {"message": "Performance-meeting data saved/updated successfully"}, 200

# # #     except errors.PyMongoError as exc:
# # #         return {"error": str(exc)}, 500


# # from pymongo import MongoClient, errors
# # from datetime import datetime
# # import calendar

# # # ──────────────────────────────────────────────────────────────
# # # Utility – validate month / year are not in the future
# # # ──────────────────────────────────────────────────────────────
# # def _validate_month_year(month_str: str, year_str: str):
# #     """
# #     Returns (is_valid: bool, month_num: int, year_int: int, err_msg: str|None)
# #     """
# #     month_str = month_str.strip()
# #     try:
# #         year_int = int(year_str)
# #     except ValueError:
# #         return False, None, None, "Year must be a number"

# #     # Accept "June" or "6"
# #     if month_str.isdigit():
# #         month_num = int(month_str)
# #         if not 1 <= month_num <= 12:
# #             return False, None, None, "Month number must be 1-12"
# #     else:
# #         month_title = month_str.title()
# #         if month_title not in calendar.month_name:
# #             return False, None, None, "Invalid month name"
# #         month_num = list(calendar.month_name).index(month_title)

# #     input_date   = datetime(year_int, month_num, 1)
# #     current_date = datetime.now().replace(day=1)

# #     if input_date > current_date:
# #         return False, None, None, "Cannot save data for a future month"

# #     return True, month_num, year_int, None


# # # ──────────────────────────────────────────────────────────────
# # # One-on-one meeting helper
# # # ──────────────────────────────────────────────────────────────
# # def save_meeting_to_db(data: dict):
# #     required = {"name", "manager", "month", "year", "isCompleted", "notes"}
# #     if missing := required.difference(data):
# #         return {"error": f"'{missing.pop()}' is required"}, 400

# #     ok, _, _, err = _validate_month_year(data["month"], str(data["year"]))
# #     if not ok:
# #         return {"error": err}, 400

# #     try:
# #         client = MongoClient(
# #             "mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/"
# #         )
# #         col = client["Timesheet"]["Employee_meetingdetails"]

# #         # Upsert keyed by (name, manager, month, year)
# #         col.update_one(
# #             {
# #                 "name":    data["name"],
# #                 "manager": data["manager"],
# #                 "month":   data["month"],
# #                 "year":    data["year"],
# #             },
# #             {
# #                 "$set": {
# #                     "isCompleted": data["isCompleted"],
# #                     "notes":       data["notes"],
# #                 }
# #             },
# #             upsert=True,
# #         )
# #         return {"message": "Meeting record saved / updated"}, 200

# #     except errors.PyMongoError as exc:
# #         return {"error": str(exc)}, 500


# # # ──────────────────────────────────────────────────────────────
# # # Performance-meeting helper  (same logic, other collection)
# # # ──────────────────────────────────────────────────────────────
# # def save_performance_meeting_to_db(data: dict):
# #     required = {"name", "manager", "month", "year", "isCompleted", "notes"}
# #     if missing := required.difference(data):
# #         return {"error": f"'{missing.pop()}' is required"}, 400

# #     ok, _, _, err = _validate_month_year(data["month"], str(data["year"]))
# #     if not ok:
# #         return {"error": err}, 400

# #     try:
# #         client = MongoClient(
# #             "mongodb+srv://timesheetsystem:SinghAutomation2025@cluster0.alcdn.mongodb.net/"
# #         )
# #         col = client["Timesheet"]["Employee_performance_meeting"]

# #         col.update_one(
# #             {
# #                 "name":    data["name"],
# #                 "manager": data["manager"],
# #                 "month":   data["month"],
# #                 "year":    data["year"],
# #             },
# #             {
# #                 "$set": {
# #                     "isCompleted": data["isCompleted"],
# #                     "notes":       data["notes"],
# #                 }
# #             },
# #             upsert=True,
# #         )
# #         return {"message": "Performance-meeting record saved / updated"}, 200

# #     except errors.PyMongoError as exc:
# #         return {"error": str(exc)}, 500
