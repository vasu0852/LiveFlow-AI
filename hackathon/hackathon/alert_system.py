from twilio.rest import Client
import time

# Replace with your Twilio credentials
TWILIO_ACCOUNT_SID = 'ACa09c67ad762f5039ce229ea492c40af8'
TWILIO_AUTH_TOKEN = '79e10e19aad680c63e8603c4a521ce49'
TWILIO_FROM_NUMBER = '+14787788030'
ALERT_TO_NUMBER = '+916281629149'

# Cooldown in seconds to prevent spamming
last_alert_time = 0
cooldown_seconds = 60

def send_alert(current_count, threshold):
    global last_alert_time
    now = time.time()

    if now - last_alert_time < cooldown_seconds:
        return  # Don't send another alert yet

    message_body = f'⚠️ Crowd Alert! Current count is {current_count}, which exceeds the threshold {threshold}.'

    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=message_body,
            from_=TWILIO_FROM_NUMBER,
            to=ALERT_TO_NUMBER
        )
        print(f"[ALERT SENT] SID: {message.sid}")
        last_alert_time = now
    except Exception as e:
        print(f"[ALERT FAILED] {e}")
