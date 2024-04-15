import os

from ultralytics import YOLO
import cv2

import mysql.connector
import requests
import time
import datetime

#DB Connection----------------------------------------------------------------------------------------------------------------------------------------------------------
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "Prforsman10!",
    "database": "Sensor"
}

#Connect to MySQL database
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

#Detect Gauge Temperature-----------------------------------------------------------------------------------------------------------------------------------------------

PRED_DIR = 'predictions'
input_path = os.path.join(PRED_DIR, "input_images")
output_path = os.path.join(PRED_DIR, "output_images")
model_path = os.path.join('.', 'runs', 'detect', 'train5', 'weights', 'best.pt')

#Load custom model
model = YOLO(model_path)
threshold = 0.5

for file in os.listdir(input_path):
    image_path = os.path.join(input_path, file)
    pred_path = os.path.join(output_path, "{}_out.jpg".format(file))
    timestamp = datetime.datetime.strptime((file.split("."))[-2], '%Y%m%d_%H%M%S')
    image = cv2.imread(image_path)
    results = model(image)[0]

    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result

        if score > threshold:
        #    cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)
        #    cv2.putText(image, results.names[int(class_id)].upper(), (int(x1), int(y1-10)),
        #                cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)   
        #cv2.imwrite(pred_path, image)       

#Insert Data--------------------------------------------------------------------------------------------------------------------------------------------------------------               
            insert_query = "INSERT INTO gauge_data (water_temperature, timestamp) VALUES (%s, %s)"
            cursor.execute(insert_query, (results.names[int(class_id)], timestamp))
            conn.commit()