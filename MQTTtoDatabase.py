import paho.mqtt.client as mqtt # Import these libraries
import mariadb                  #|
import sys                      #|

try:
    conn = mariadb.connect(     # Connecting to our DB = Database
        user="root",            # This is what the "Username" of the DB would be, for better sequrity this should be switched in the future.
        password="!Vdn66aha",   # Our password for the DB
        host="localhost",       # What website we wan't it on. In this instance its just our localhost.
        port=3306,              # What port that's used
        database="SensorData",  # The name of our DB
        autocommit=True)        # If our DB get's any input from the sensors, it then automaticly stores it. 

except mariadb.Error as e:      # If an error occurs and it's an mariadb.Error message, then it prints the next line instead
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)                 # The program, if incounter an error, it prints exit(1) meaning that there's an error in the system

cur = conn.cursor()             # Opens a cursor, to perform DB operations

                                # These DEF "add_" functions, allows us to insert data into the database, in the different tables

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

                                # Here we subscribe the MQTT server with the topic /# = wildcard. So it takes everything in the topic
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("Project3/#")

                                # Takes the message and, stores it in the respective tables in the DB
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

                                
client = mqtt.Client()          # Connecting to our MQTT-Server with the the on_connect and on_message defines
client.on_connect = on_connect
client.on_message = on_message
client.connect("broker.hivemq.com", 1883, 60)   # This is our selected broker to use, with the port and a max of 60 seconds of use
client.loop_forever()           # Keeps the connection open

