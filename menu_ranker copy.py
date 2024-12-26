from flask import Flask, jsonify, request
import json
from collections import defaultdict

app = Flask(__name__)

# Dummy Data
click_data = {
    "user_123": {
        "Menu 1": [
            {"date": "2024-12-26", "count": 4, "timestamps": ["2024-12-26T06:08:03", "2024-12-26T05:24:03"]},
            {"date": "2024-12-25", "count": 3, "timestamps": ["2024-12-25T10:30:03"]},
        ],
        "Menu 2": [
            {"date": "2024-12-26", "count": 5, "timestamps": ["2024-12-26T01:30:03", "2024-12-26T12:24:03"]},
            {"date": "2024-12-25", "count": 2, "timestamps": ["2024-12-25T11:00:03"]},
        ],
        "Menu 3": [
            {"date": "2024-12-26", "count": 3, "timestamps": ["2024-12-26T09:08:03", "2024-12-26T06:24:03"]},
        ],
        "Menu 4": [
            {"date": "2024-12-26", "count": 2, "timestamps": ["2024-12-26T10:08:03"]},
        ],
    }
}


# Function to calculate menu ranks
def calculate_menu_ranks(user_id):
    user_data = click_data.get(user_id, {})
    menu_counts = defaultdict(int)

    # Aggregate total counts per menu
    for menu, logs in user_data.items():
        for log in logs:
            menu_counts[menu] += log["count"]

    # Sort menus by total counts (descending order)
    ranked_menus = sorted(menu_counts.items(), key=lambda x: x[1], reverse=True)

    # Convert to the desired format
    ranked_menus_list = [{"menu": menu, "total_clicks": total_clicks} for menu, total_clicks in ranked_menus]
    return ranked_menus_list


# API Endpoint: Fetch ranked menus
@app.route("/get-ranked-menus", methods=["GET"])
def get_ranked_menus():
    user_id = request.args.get("user_id", "user_123")
    ranked_menus = calculate_menu_ranks(user_id)
    return jsonify({"user_id": user_id, "ranked_menus": ranked_menus})


# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
