void TempHumi() {
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  if (isnan(h) || isnan(t)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }
  // Publishes the humidity to the humidity topic
  client.publish(topic5, String(h).c_str());
  // Publishes the temperature to the temperature topic
  client.publish(topic2, String(t).c_str());
}
