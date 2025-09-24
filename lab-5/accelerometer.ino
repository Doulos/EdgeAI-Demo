/*
  Arduino LSM9DS1 - Simple Accelerometer

  This example reads the acceleration values from the LSM9DS1
  sensor and continuously prints them to the Serial Monitor
  or Serial Plotter.

  The circuit:
  - Arduino Nano 33 BLE Sense

  created 10 Jul 2019
  by Riccardo Rizzo

  This example code is in the public domain.
*/

#include <Arduino_HTS221.h>
#include <Arduino_LSM9DS1.h>

void setup() {
  Serial.begin(9600);
  while (!Serial);
  Serial.println("Started");

  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }
     

  if (!HTS.begin()) {
      Serial.println("Failed to initialize humidity temperature sensor!");
      while (1); // Halt if sensor initialization fails
  }
        

  Serial.print("Accelerometer sample rate = ");
  Serial.print(IMU.accelerationSampleRate());
  Serial.println(" Hz");
  Serial.println();
  Serial.println("Acceleration in g's");
  Serial.println("X,Y,Z");
}

void loop() {

  float temperature = HTS.readTemperature(); // Read temperature
  float humidity = HTS.readHumidity();     // Read humidity
  float x, y, z;

  Serial.print("Temperature = ");
  Serial.print(temperature);
  Serial.println(" °C");

  Serial.print("Humidity = ");
  Serial.print(humidity);
  Serial.println(" %");

  IMU.readAcceleration(x, y, z);

  Serial.print("Accel_x = ");
  Serial.println(x);
  Serial.print("Accel_y = ");
  Serial.println(y);
  Serial.print("Accel_z = ");
  Serial.println(z);

  delay(100); // Wait 0.1 second before reading again
  
}
