import serial
import time
import csv

ser = serial.Serial('/dev/ttyACM0')
ser.flushInput()

while True:
	try:
		ser_bytes = ser.readline()
		data_read= str(ser_bytes,'UTF-8')
		print(data_read)
		with open("test_data.csv","a") as f:
			writer = csv.writer(f,delimiter=",")
			writer.writerow([time.time(),data_read])
	except:
		print("Keyboard Interrupt")
		break
		
		
'''#include <Arduino_LSM9DS1.h>

void setup() {
  Serial.begin(9600);
  while (!Serial);
  Serial.println("Started");

  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }

  Serial.print("Accelerometer sample rate = ");
  Serial.print(IMU.accelerationSampleRate());
  Serial.println(" Hz");
  Serial.println();
  Serial.println("Acceleration in G's");
  Serial.println("X\tY\tZ");
}

void loop() {
  float x, y, z;

  if (IMU.accelerationAvailable()) {
    IMU.readAcceleration(x, y, z);

    Serial.print(x);
    Serial.print('\t');
    Serial.print(y);
    Serial.print('\t');
    Serial.println(z);
  }
}'''