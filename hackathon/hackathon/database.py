import cx_Oracle
from datetime import datetime

# Replace with your credentials
USERNAME = 'system'
PASSWORD = 'thanuj'
HOST = 'localhost'
PORT = 1521
SERVICE_NAME = 'XE'

dsn = cx_Oracle.makedsn(HOST, PORT, service_name=SERVICE_NAME)

def log_crowd_count(count, alert_triggered):
    try:
        conn = cx_Oracle.connect(USERNAME, PASSWORD, dsn)
        cursor = conn.cursor()

        cursor.execute("""
            BEGIN
                EXECUTE IMMEDIATE '
                    CREATE TABLE venueflow_logs (
                        id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                        log_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        people_count NUMBER,
                        alert_triggered VARCHAR2(5)
                    )';
            EXCEPTION
                WHEN OTHERS THEN
                    IF SQLCODE != -955 THEN
                        RAISE;
                    END IF;
            END;
        """)

        cursor.execute("""
            INSERT INTO venueflow_logs (people_count, alert_triggered)
            VALUES (:count, :alert_triggered)
        """, {'count': count, 'alert_triggered': 'YES' if alert_triggered else 'NO'})

        conn.commit()
        cursor.close()
        conn.close()
        print(f"[DB LOGGED] Count: {count}, Alert: {'YES' if alert_triggered else 'NO'}")
    except Exception as e:
        print(f"[DB ERROR] {e}")

# -- Set line size and column widths
# SET LINESIZE 100
# SET PAGESIZE 50

# COLUMN ID FORMAT 999
# COLUMN LOG_TIME FORMAT A25
# COLUMN PEOPLE_COUNT FORMAT 999
# COLUMN ALERT_TRIGGERED FORMAT A10

# -- View the table in tabular form
# SELECT * FROM venueflow_logs;
