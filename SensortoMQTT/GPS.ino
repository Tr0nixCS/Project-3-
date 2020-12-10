void display_values()
{
  // This sketch displays information every time a new sentence is correctly encoded.
  while (gpsSerial.available() > 0)
    if (gps.encode(gpsSerial.read()))
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
    latitude = String(gps.location.lat(), 6);
    longitude = String(gps.location.lng(), 6);
    coordinates = latitude + " " + longitude;
    client.publish(topic3, String(coordinates).c_str());
    Serial.print("Latitude: ");
    Serial.println(gps.location.lat(), 6);
    Serial.print("Longitude: ");
    Serial.println(gps.location.lng(), 6);
  }
  else
  {
    client.publish(topic3, "Not Available");
  }
  
  //Serial.print("Time: ");
  if (gps.time.isValid())
  {
    if (gps.time.hour() < 10) Serial.print(F("0"));
    hourtime = String(gps.time.hour() + 1);
    minutetime = String(gps.time.minute());
    secondtime = String(gps.time.second());
    totaltime = hourtime + ":" + minutetime + ":" + secondtime;
    
    client.publish(topic4, String(totaltime).c_str());
  }
  else
  {
    client.publish(topic4, 0);
  }
  //Serial.println();
  //Serial.println();
  delay(1000);
}
