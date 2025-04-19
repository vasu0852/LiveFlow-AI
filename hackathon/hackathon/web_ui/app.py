from flask import Flask, render_template
from flask import Flask, render_template, jsonify
import cx_Oracle
import os,sys
from flask import Flask, render_template, url_for
from heatmap_generator import generate_heatmap
from flask import Flask, render_template, request, jsonify
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import shared_data
app = Flask(__name__)

current_threshold = 4 

# Oracle DB connection settings
USERNAME = 'system'
PASSWORD = 'thanuj'
HOST = 'localhost'
PORT = 1521
SERVICE_NAME = 'XE'

dsn = cx_Oracle.makedsn(HOST, PORT, service_name=SERVICE_NAME)

def get_logs():
    try:
        conn = cx_Oracle.connect(USERNAME, PASSWORD, dsn)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id,
                   TO_CHAR(log_time, 'YYYY-MM-DD HH24:MI:SS') AS log_time,
                   people_count,
                   alert_triggered
            FROM venueflow_logs
            ORDER BY log_time DESC FETCH FIRST 20 ROWS ONLY
        """)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
    except Exception as e:
        print(f"Error fetching logs: {e}")
        return []

@app.route("/")
def dashboard():
    logs = get_logs()
    return render_template("dashboard.html", logs=logs,current_threshold=current_threshold)

@app.route('/update-threshold', methods=['POST'])
def update_threshold():
    global current_threshold  # Ensure we are using the global variable
    data = request.get_json()  # Retrieve the JSON data from the request body
    new_threshold = int(data['threshold'])  # Convert the threshold to an integer
    current_threshold = new_threshold  # Update the global threshold variable
    return jsonify(success=True)  # Respond with success

@app.route('/get-threshold', methods=['GET'])
def get_threshold():
    global current_threshold
    return jsonify({'threshold': current_threshold})

@app.route('/heatmap')
def show_heatmap():
    from heatmap_generator import generate_heatmap
    generate_heatmap()  # Create latest heatmap
    return render_template('heatmap.html')


if __name__ == "__main__":
    app.run(debug=True)
