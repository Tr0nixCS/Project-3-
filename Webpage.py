from flask import Flask, render_template                                        # Import these libraries
import mariadb
import sys

app = Flask(__name__)                                                           # This is used to create the webpage with Flask. __name__ is, to make it able to be used in other programs just by importing the name of the file
try:
    conn = mariadb.connect(                                                     # Connecting to our DB = Database
        user="root",                                                            # This is what the "Username" of the DB would be
        password="!Vdn66aha",                                                   # Our password for the DB
        host="localhost",                                                       # What website we wan't it on. In this instance its just our localhost.
        port=3306,                                                              # What port that's used
        database="SensorData",                                                  # The name of our DB
        autocommit=True)                                                        # If our DB get's any input from the sensors, it then automaticly stores it.
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")                         # If an error occurs and it's an mariadb.Error message, then it prints the next line instead
    sys.exit(1)                                                                 # The program, if incounter an error, it prints exit(1) meaning that there's an error in the system

cur = conn.cursor()                                                             # Opens a cursor, to perform DB operations

@app.route("/")                                                                 # This is the "homepage" of the website, with all of your data "printed" on it.
def table():
    tempreading = []
    ldrreading = []
    humidityreading = []
    timereading = []
    global coordinates
    cur.execute("SELECT * FROM SensorData.temperatur order by id desc limit 1;")
    for (id, temperature, sensor) in cur:
        tempreading.append(f"<tr><td>{id}</td><td>{temperature}</td><td>{sensor}</td></tr>")
    cur.execute("SELECT * FROM SensorData.ldrsensor order by id desc limit 1;")
    for (id, brightness, sensor) in cur:
        ldrreading.append(f"<tr><td>{id}</td><td>{brightness}</td><td>{sensor}</td></tr>")
    cur.execute("SELECT * FROM SensorData.fugtighed order by id desc limit 1;")
    for (id, humidity, sensor) in cur:
        humidityreading.append(f"<tr><td>{id}</td><td>{humidity}</td><td>{sensor}</td></tr>")
    cur.execute("SELECT coordinates FROM SensorData.gps_placering order by id desc limit 1;")
    gpsreading = cur.fetchone()  # Stores the coordinates in a variable as a tuple
    gpstring = "".join(gpsreading)  # Converts the tuple to a string and stores it in a variable
    coordinates = gpstring[-10:] + ", " + gpstring[:-10]
    cur.execute("SELECT * FROM SensorData.gps_tid order by id desc limit 1;")
    for (id, time, sensor) in cur:
        timereading.append(f"<tr><td>{id}</td><td>{time}</td><td>{sensor}</td></tr>")
    return render_template("index.html", temp="".join(tempreading), ldr="".join(ldrreading), humid="".join(humidityreading), gps="".join(timereading))


@app.route("/Map")                                                              # Opens the map.html file and sets the zoom level to 17, when you press the Map tab in the webpage
def maptab():
    zooom = "17"
    return render_template("map.html", zoom=f"{zooom}", coordinates=coordinates)


@app.route("/sams.geojson")                                                     # Puts a small circle at the corrdinates from the GPS in the DB. And shows that on the map page. 
def samsdata():
    return render_template("sams.geojson.txt", coordinates=coordinates)


if __name__ == "__main__":                                                      #We use __name__ == "__main__": For being able to run it in deffernt instances. So we can call the app.run, and it will run everything at once.                                             
    app.run()
