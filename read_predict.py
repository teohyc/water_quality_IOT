#import serial
import time
import pickle
import numpy as np
from sklearn.ensemble import RandomForestClassifier

import requests

# -----------------------------
# TELEGRAM CONFIG
# -----------------------------
TELEGRAM_TOKEN = "8481983410:AAFIbCgYyMNMm4NuGShLaonot7tmIu_Ckm0"
CHAT_ID = 1598056895  # replace with your chat id


# -----------------------------
# CONFIGURATION
# -----------------------------
'''SERIAL_PORT = '/dev/ttyACM0'   # change if needed
BAUD_RATE = 115200
MODEL_PATH = 'water_quality_random_forest_model.pickle'



# -----------------------------
# OPEN SERIAL PORT
# -----------------------------
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
time.sleep(2)  # allow serial to settle

print(" Serial connection established")'''

def send_telegram_alert(status, confidence, ph, turb, cond):
    message = (
        "🚰 *Water Quality Alert*\n\n"
        f"*Status:* {status}\n"
        f"*pH:* {ph:.2f}\n"
        f"*Turbidity:* {turb:.2f} NTU\n"
        f"*Conductivity:* {cond:.0f} µS/cm\n"
        f"*Confidence:* {confidence:.2f}"
    )

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    })


# -----------------------------
# MAIN LOOP
# -----------------------------
MODEL_PATH = 'water_quality_random_forest_model.pickle'
with open(MODEL_PATH, 'rb') as f:
    model = pickle.load(f)

last_status = None
while True:
    try:
        '''line = ser.readline().decode('utf-8').strip()

        if not line:
            continue

        print(f" Raw data: {line}")

        # Parse values
        ph, turb, cond = map(float, line.split(','))'''

        # Prepare input for model
        cond=float(input("cond:"))
        ph=float(input("ph:"))
        turb=float(input("turb:"))
        

        X = np.array([[cond, ph, turb]])

        # Prediction
        #test bad - 430, 7.9, 29.8
        #test good - 380, 8.6, 8.6

        y_pred = model.predict(X)[0]
        y_prob = model.predict_proba(X)[0][1]

        status = "GOOD" if y_pred == 1 else "BAD"

        print(f"pH={ph:.2f}, Turb={turb:.2f}, Cond={cond:.0f}")
        print(f"Prediction: {status} (confidence={y_prob:.2f})")
        print("-" * 50)

         # Send Telegram alert ONLY on status change
        if status != last_status:
            send_telegram_alert(status, y_prob, ph, turb, cond)
            last_status = status

        # send command back to microcontroller
        # if y_pred == 0:
        #     ser.write(b"CLOSE_VALVE\n")
        # else:
        #     ser.write(b"OPEN_VALVE\n")

        time.sleep(2)

    except ValueError:
        print("Data format error")
    except KeyboardInterrupt:
        print("🛑 Stopped by user")
        break

#ser.close()