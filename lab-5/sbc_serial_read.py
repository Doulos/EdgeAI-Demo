import serial

ser = serial.Serial('COM4',9600)
ser.flushInput()

while True:
	try:
		line = ser.readline()
		line_read=line.decode()
		data_read= line_read.replace('\n','')
		print(data_read)
		with open("test_data.txt","a") as f:
			f.write(data_read)
	except:
		print("Keyboard Interrupt")
		break
