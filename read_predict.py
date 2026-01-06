import serial
import time
import pickle
import numpy as np
from sklearn.ensemble import RandomForestClassifier

# -----------------------------
# CONFIGURATION
# -----------------------------
SERIAL_PORT = '/dev/ttyACM0'   # change if needed
BAUD_RATE = 115200
MODEL_PATH = 'water_quality_random_forest_model.pickle'

# -----------------------------
# LOAD MODEL
# -----------------------------
with open(MODEL_PATH, 'rb') as f:
    model = pickle.load(f)

print("Model loaded successfully")

# -----------------------------
# OPEN SERIAL PORT
# -----------------------------
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
time.sleep(2)  # allow serial to settle

print(" Serial connection established")

# -----------------------------
# MAIN LOOP
# -----------------------------
while True:
    try:
        line = ser.readline().decode('utf-8').strip()

        if not line:
            continue

        print(f" Raw data: {line}")

        # Parse values
        ph, turb, cond = map(float, line.split(','))

        # Prepare input for model
        X = np.array([[ph, turb, cond]])

        # Prediction
        y_pred = model.predict(X)[0]
        y_prob = model.predict_proba(X)[0][1]

        status = "GOOD ✅" if y_pred == 1 else "BAD ❌"

        print(f"pH={ph:.2f}, Turb={turb:.2f}, Cond={cond:.0f}")
        print(f"Prediction: {status} (confidence={y_prob:.2f})")
        print("-" * 50)

        # send command back to microcontroller
        # if y_pred == 0:
        #     ser.write(b"CLOSE_VALVE\n")
        # else:
        #     ser.write(b"OPEN_VALVE\n")

        time.sleep(2)

    except ValueError:
        print("⚠ Data format error")
    except KeyboardInterrupt:
        print("🛑 Stopped by user")
        break

ser.close()
