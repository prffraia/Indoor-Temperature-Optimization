import mysql.connector
import requests
import time

#API parameters
api_key = "bc2ea985a9c79a2948df30c5d310d622"
db_config = {
    "host": "",
    "user": "",
    "password": "",
    "database": "Sensor"
}

#URL of weather API endpoint
api_base_url = "https://api.openweathermap.org/data/2.5/weather?lat=40.4258727&lon=-3.7860027&appid=bc2ea985a9c79a2948df30c5d310d622&units=metric"

#Connect to MySQL database
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

while True:
    try:
        #Make API call
        response = requests.get(api_base_url)
        data = response.json()
        data_main = data.get("main")
        print(data)
        print(data_main)

        #Extract relevant data
        humidity = data_main["humidity"]
        temperature = data_main["temp"]
        pressure = data_main["pressure"]
        time_id = data["dt"]

        #Insert data into MySQL database
        insert_query = "INSERT INTO openweather (humidity, temperature, pressure, time) VALUES (%s, %s, %s, %s)"
        cursor.execute(insert_query, (humidity, temperature, pressure, time_id))
        conn.commit()

        time.sleep(300) #Wait for 5 minutes before next iteration

    except Exception as error:
        print(f"An error occurred: {str(error)}")
        time.sleep(60) #Wait for 1 minute before retrying






