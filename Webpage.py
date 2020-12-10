from flask import Flask, render_template
import mariadb
import sys

app = Flask(__name__)
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


def checklocation():
    variable = cur.execute("SELECT * FROM SensorData.gps_location order by id desc limit 1;")
    print(variable)


@app.route("/")
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


@app.route("/Map")
#
def maptab():
    zooom = "17"
    return render_template("map.html", zoom=f"{zooom}", coordinates=coordinates)


@app.route("/sams.geojson")
def samsdata():
    return render_template("sams.geojson.txt", coordinates=coordinates)


if __name__ == "__main__":
    app.run()
