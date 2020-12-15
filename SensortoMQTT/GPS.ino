void display_values()
{
  int time_start = millis();
  // This sketch displays information every time a new sentence is correctly encoded.
  while (gpsSerial.available() > 0)
    if (gps.encode(gpsSerial.read()))

      // 
      if (millis() - time_start >= 5000);
        displayInfo();

  // If 5000 milliseconds pass and there are no characters coming in
  // over the software serial port, show a "No GPS detected" error
  if (millis() > 5000 && gps.charsProcessed() < 10)
  {
    Serial.println("No GPS detected");
    while(true);
  }
}

void displayInfo()
{
  if (gps.location.isValid())
  {
    // Converting the GPS data to string variables
    latitude = String(gps.location.lat(), 6);
    longitude = String(gps.location.lng(), 6);
    
    coordinates = latitude + " " + longitude;
    
    // Publishes the GPS location to the GPS location topic
    client.publish(topic3, String(coordinates).c_str());
    Serial.println(gps.location.lat(), 6);
  }
  else
  {
    // Publishes nothing to the topic if the GPS cant get any signal
    client.publish(topic3, "Not Available");
  }
  
  if (gps.time.isValid())
  {
    if (gps.time.hour() < 10) Serial.print(F("0"));

      // Converting the GPS data to string variables
      hourtime = String(gps.time.hour() + 1);
      minutetime = String(gps.time.minute());
      secondtime = String(gps.time.second());
      totaltime = hourtime + ":" + minutetime + ":" + secondtime;

      // Publishes GPS time to the gps time topic
      client.publish(topic4, String(totaltime).c_str());
  }
  else
  {
    // Prints nothing if the GPS cant get any signal
    client.publish(topic4, 0);
  }
  delay(1000);
}
