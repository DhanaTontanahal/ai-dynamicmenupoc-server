from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
import json
from collections import defaultdict
from llama_model import get_ranked_menus_with_llama  # Import the LLaMA logic


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",  
    password="yourpassword", 
    database="menu_logger"
)

# Cursor for database operations
cursor = db.cursor(dictionary=True)

# Function to fetch click data for the LLaMA model
def fetch_click_data_for_llama(user_id):
    """
    Fetch click data from the database to send to the LLaMA model.
    """
    cursor.execute("SELECT menu_name, SUM(click_count) AS total_clicks FROM click_logs WHERE user_id=%s GROUP BY menu_name", (user_id,))
    records = cursor.fetchall()
    input_data = [{"menu_name": record["menu_name"], "click_count": int(record["total_clicks"])} for record in records]
    return input_data

# Function to log menu clicks
def log_menu_click(user_id, menu_name, timestamp):
    click_date = timestamp.split("T")[0]  # Extract date from ISO timestamp

    # Check if there's already an entry for the user, menu, and date
    cursor.execute(
        "SELECT * FROM click_logs WHERE user_id=%s AND menu_name=%s AND click_date=%s",
        (user_id, menu_name, click_date)
    )
    record = cursor.fetchone()

    if record:
        # Update existing record
        updated_timestamps = json.loads(record["timestamps"])
        updated_timestamps.append(timestamp)
        new_click_count = record["click_count"] + 1

        cursor.execute(
            "UPDATE click_logs SET click_count=%s, timestamps=%s WHERE id=%s",
            (new_click_count, json.dumps(updated_timestamps), record["id"])
        )
    else:
        # Insert a new record
        cursor.execute(
            "INSERT INTO click_logs (user_id, menu_name, click_date, click_count, timestamps) VALUES (%s, %s, %s, %s, %s)",
            (user_id, menu_name, click_date, 1, json.dumps([timestamp]))
        )

    db.commit()

# Function to calculate menu ranks
def calculate_menu_ranks(user_id):
    # Fetch all records for the user
    cursor.execute("SELECT menu_name, SUM(click_count) AS total_clicks FROM click_logs WHERE user_id=%s GROUP BY menu_name ORDER BY total_clicks DESC", (user_id,))
    records = cursor.fetchall()

    # Format the result
    ranked_menus = [{"menu": record["menu_name"], "total_clicks": record["total_clicks"]} for record in records]
    return ranked_menus

# API Endpoint: Log a menu click
@app.route("/log-menu-click", methods=["POST"])
def log_menu_click_endpoint():
    data = request.json
    user_id = data["user_id"]
    menu_name = data["menu_name"]
    timestamp = data["timestamp"]
    log_menu_click(user_id, menu_name, timestamp)
    return jsonify({"message": "Click logged successfully"}), 200

# API Endpoint: Fetch ranked menus
@app.route("/get-ranked-menus", methods=["GET"])
def get_ranked_menus():
    user_id = request.args.get("user_id", "user_123")
    
    # Step 1: Fetch data from the database
    input_data = fetch_click_data_for_llama(user_id)
    print("getting db data..........................")
    print(input_data)
    # Step 2: Call the LLaMA model to get ranked results
    try:
        ranked_menus = get_ranked_menus_with_llama(input_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    # Step 3: Return the ranked menu data
    return jsonify({"user_id": user_id, "ranked_menus": ranked_menus})

# API Endpoint: Fetch ranked menus
# @app.route("/get-ranked-menus", methods=["GET"])
# def get_ranked_menus():
#     user_id = request.args.get("user_id", "user_123")
#     ranked_menus = calculate_menu_ranks(user_id)
#     return jsonify({"user_id": user_id, "ranked_menus": ranked_menus})

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
