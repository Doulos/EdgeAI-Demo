import sys
import time
import datetime
import cv2
import json
import sqlite3
import paho.mqtt.client as mqtt
from ai_edge_litert.interpreter import Interpreter
import numpy as np

# --- Configuration ---
DB_NAME = "detections.db"
BROKER = "test.mosquitto.org"
#BROKER = "broker.hive.com"
TOPIC = "object/detections/json"

# --- Database Initialization ---
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Create table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS detection_log
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  timestamp DATETIME,
                  label TEXT,
                  confidence REAL,
                  x1 INTEGER, y1 INTEGER, x2 INTEGER, y2 INTEGER)''')
    conn.commit()
    conn.close()
    
# --- MQTT Callbacks ---

def on_message(client, userdata, message):
    try:
        payload = message.payload.decode()
        data = json.loads(payload)
        timestamp_str = datetime.datetime.fromtimestamp(data['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
        
        # 1. Get the single object dictionary
        obj = data.get('objects')
        
        if obj:
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            
            # 2. Access the dictionary keys directly (no loop needed if it's one object)
            c.execute('''INSERT INTO detection_log 
                         (timestamp, label, confidence, x1, y1, x2, y2) 
                         VALUES (?, ?, ?, ?, ?, ?, ?)''',
                      (timestamp_str, 
                       obj['label'], 
                       obj['confidence'], 
                       obj['bbox'][0], 
                       obj['bbox'][1], 
                       obj['bbox'][2], 
                       obj['bbox'][3]))
            
            conn.commit()
            conn.close()
            print(f"✅ Logged to DB: {obj['label']}")
            
    except Exception as e:
        print(f"❌ Database Insertion Error: {e}")

def init_mqtt():
    #client = mqtt.Client()
    client.on_message = on_message
    #client.connect(BROKER, 1883, 60)
    client.subscribe(TOPIC)
    client.loop_start()
    return client



# Broker_address for prototyping MQTT communications
#broker_address = "test.mosquitto.org"
# In case "test.mosquitto.org" is not working, use the broker from HiveMQ mentioned below
#broker_address = "broker.hivemq.com"

#Create new MQTT client instance
client = mqtt.Client()

#Connect to broker. Broker can be located on edge or cloud
client.connect(BROKER, 1883)


# Function to load labels from a file
def load_labels(file_path):
    with open(file_path, 'r') as f:
        return {i: line.strip() for i, line in enumerate(f.readlines())}

# Load labels from the provided text file
label2string = load_labels('src/coco_labels.txt')

def detect_from_image():
    cap = cv2.VideoCapture('/dev/video0', cv2.CAP_V4L)
    
    success, img_org = cap.read()
    #     if not success:
    #        sys.exit('ERROR: Unable to read from webcam. Please verify your webcam settings.')

    # prepare input image
    img = cv2.cvtColor(img_org, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (640, 640))
    input_tensor = np.asarray(img, dtype=np.float32)

    # Normalize pixel values to be between 0 and 1.0
    input_tensor /= 255.0

    # Add batch dimension (1, 640, 640, 3) as expected by the TFLite model
    input_tensor = np.expand_dims(input_tensor, axis=0)

    # Overview of Object Detection - YOLOv10 model: https://docs.ultralytics.com/models/yolov10/
   
    interpreter = Interpreter(
        model_path="src/yolov10n_float16.tflite")

    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # set input tensor
    interpreter.set_tensor(input_details[0]['index'], input_tensor)

    # execute model graph using LiteRT
    interpreter.invoke()

    output_data = interpreter.get_tensor(output_details[0]['index'])    
      
    first_detection = output_data[0,0]
    
    # get output tensor details for first detection [0]
    x, y, w, h, confidence, class_id = first_detection
    
    det_info = {
                "class_id": int(class_id.item()), 
                "label": label2string[int(class_id.item())],
                "confidence": round(float(confidence.item()), 3),
                # Ensure every element in the list is a native float
                "bbox": [
                    float(x.item()), 
                    float(y.item()), 
                    float(w.item()), 
                    float(h.item())
                                    ]
            }

    return det_info


def publish_inference():
    detection = detect_from_image()
    
    message = {
        "timestamp": time.time(),
        "objects": detection
        
    }

    # Convert dictionary to a JSON formatted string
    json_payload = json.dumps(message)
    
    print(f"Sending JSON: {json_payload}")
    client.publish(TOPIC, payload=json_payload)
    print ('Inference published to MQTT topic')
 
def print_final_report():
    """
    Reads the SQLite database and prints it using 
    only the Python Standard Library.
    """
    print("\n" + "="*80)
    print(f"{'ID':<4} | {'Timestamp':<20} | {'Label':<10} | {'Conf':<6} | {'Coordinates (x1, y1, x2, y2)'}")
    print("-" * 80)
    
    try:
        # Connect to the database
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        # Execute the query
        cursor.execute("SELECT id, timestamp, label, confidence, x1, y1, x2, y2 FROM detection_log")
        rows = cursor.fetchall()
        
        if not rows:
            print("No detections found in the database.")
        else:
            for row in rows:
                # Unpack the row for easier formatting
                id_val, ts, label, conf, x1, y1, x2, y2 = row
                coords = f"({x1}, {y1}, {x2}, {y2})"
                
                # Use f-string alignment: < for left, > for right
                print(f"{id_val:<4} | {ts:<20} | {label:<10} | {conf:<6.2f} | {coords}")
        
        conn.close()
    except Exception as e:
        print(f"Error reading database: {e}")
    
    print("="*80 + "\n")

if __name__ == '__main__':
    init_db()
    init_mqtt()
    publish_inference()
    time.sleep(5)
    publish_inference
    time.sleep(5)
    client.disconnect()
    client.loop_stop()
    print("MQTT client disconnected and loop stopped.")
    print_final_report()
    sys.exit(0) # Exit the Python program    

