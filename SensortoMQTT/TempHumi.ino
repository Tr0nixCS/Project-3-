void TempHumi() {
  // Wait a few seconds between measurements:
  //delay(2000);
  // Reading temperature or humidity takes about 250 milliseconds!
  // Sensor readings may also be up to 2 seconds 'old' (its a very slow sensor)
  // Read the humidity in %:
  float h = dht.readHumidity();
  // Read the temperature as Celsius:
  float t = dht.readTemperature();
  // Read the temperature as Fahrenheit:
  float f = dht.readTemperature(true);
  // Check if any reads failed and exit early (to try again):
  if (isnan(h) || isnan(t) || isnan(f)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }
  // Compute heat index in Fahrenheit (default):
  float hif = dht.computeHeatIndex(f, h);
  // Compute heat index in Celsius:
  float hic = dht.computeHeatIndex(t, h, false);
  //Serial.print("Humidity: ");
  client.publish(topic5, String(h).c_str());
  //Serial.print(" % ");
  //Serial.print("Temperature: ");
  client.publish(topic2, String(t).c_str());
  Serial.print(" \xC2\xB0");
  //Serial.println("C");
}
