import paho.mqtt.client as mqtt
import mariadb
import sys

try:
    conn = mariadb.connect(
        user="root",
        password="!Vdn66aha",
        host="localhost",
        port=3306,
        database="SensorData",
        autocommit=True)

except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

cur = conn.cursor()


def add_time_measurement(cur, t, p):
    cur.execute("INSERT INTO SensorData.GPS_tid(time, sensor)"
                "VALUES (?, ?)", (t, p))


def add_location_measurement(cur, t, p):
    cur.execute("INSERT INTO SensorData.GPS_placering(coordinates, location)"
                "VALUES (?, ?)", (t, p))


def add_humidity_measurement(cur, t, p):
    cur.execute("INSERT INTO SensorData.fugtighed(fugtighed, sensor)"
                "VALUES (?, ?)", (t, p))


def add_ldr_measurement(cur, t, p):
    cur.execute("INSERT INTO SensorData.ldrsensor(brightness, sensor)"
                "VALUES (?, ?)", (t, p))


def add_temperature_measurement(cur, t, p):
    cur.execute("INSERT INTO SensorData.temperatur(temperature, sensor)"
                "VALUES (?, ?)", (t, p))


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("Project3/#")


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload.decode("utf-8")))
    if msg.topic == "Project3/Temperature_classroom/Martin":
        add_temperature_measurement(cur, msg.payload, msg.topic)
    if msg.topic == "Project3/Humidity_classroom/Martin":
        add_humidity_measurement(cur, msg.payload, msg.topic)
    if msg.topic == "Project3/LDR_classroom/Martin":
        add_ldr_measurement(cur, msg.payload, msg.topic)
    if msg.topic == "Project3/GPS_location/Martin":
        add_location_measurement(cur, msg.payload, msg.topic)
    if msg.topic == "Project3/GPS_time/Martin":
        add_time_measurement(cur, msg.payload, msg.topic)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("broker.hivemq.com", 1883, 60)
client.loop_forever()

