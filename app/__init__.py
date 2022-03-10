import datetime
import json

from flask import Flask, render_template, Response
from app.dynamodb_access import get_all_readings, get_item_by_attribute


app = Flask(__name__)

def convert_to_datetime(items):
    for item in items:
        item['datetime'] = datetime.datetime.strptime(item['datetime'], "%Y-%m-%d %H:%M:%S")


@app.get('/')
def index():
    return render_template('index.html')

@app.get('/tables')
def tables():
    readings = get_all_readings()
    return render_template('tables.html', readings=readings)

@app.get('/data')
def get_data():
    sensor_living_room_readings = get_item_by_attribute('sensor', 'LivingRoom Sensor')
    sensor_kitchen_readings = get_item_by_attribute('sensor', 'Kitchen Sensor')
    sensor_bedroom_readings = get_item_by_attribute('sensor', 'Bedroom Sensor')
    sensor_gaming_room_readings = get_item_by_attribute('sensor', 'GamingRoom Sensor')

    convert_to_datetime(sensor_living_room_readings)
    convert_to_datetime(sensor_kitchen_readings)
    convert_to_datetime(sensor_bedroom_readings)
    convert_to_datetime(sensor_gaming_room_readings)

    #SENSOR FOR LIVING ROOM
    sensor_liv = sorted(sensor_living_room_readings, key=lambda item: item['datetime'])[-1]
    sensor_liv['temp'] = int(sensor_liv['temp'])
    sensor_liv['datetime'] = sensor_liv['datetime'].strftime("%Y-%m-%d %H:%M:%S")

    #SENSOR FOR KITCHEN
    sensor_kitchen = sorted(sensor_kitchen_readings, key=lambda item: item['datetime'])[-1]
    sensor_kitchen['temp'] = int(sensor_kitchen['temp'])
    sensor_kitchen['datetime'] = sensor_kitchen['datetime'].strftime("%Y-%m-%d %H:%M:%S")

    #SENSOR FOR BEDROOM
    sensor_bedroom = sorted(sensor_bedroom_readings, key=lambda item: item['datetime'])[-1]
    sensor_bedroom['temp'] = int(sensor_bedroom['temp'])
    sensor_bedroom['datetime'] = sensor_bedroom['datetime'].strftime("%Y-%m-%d %H:%M:%S")

    #SENSOR FOR GAMING ROOM
    sensor_gaming = sorted(sensor_gaming_room_readings, key=lambda item: item['datetime'])[-1]
    sensor_gaming['temp'] = int(sensor_gaming['temp'])
    sensor_gaming['datetime'] = sensor_gaming['datetime'].strftime("%Y-%m-%d %H:%M:%S")

    sensors = [sensor_liv, sensor_kitchen, sensor_bedroom, sensor_gaming]


    return Response(json.dumps(sensors), 200, content_type='application/json')