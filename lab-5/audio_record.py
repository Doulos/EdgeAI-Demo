# Description :  Code to acquire 5s audio clips and convert to Spectrogram

# Input :  Audio from SBC input (.wav) files. 
#          Use arecord -l to get a list of the devices on your system. 
#          The hw:X,Y comes from this mapping of your hardware.
#          In this case, X is the card number, while Y is the device number.
#
#Output: Spectrogram (.png) files of size 224 x 224 pixels created using Sound Exchange (SoX) software


import os
import subprocess



for i in range(6):
	arecord_cli = (f'arecord --format cd -D hw:2,0 --duration 5 --channels 1 waves{i}.wav')
	subprocess.run(args = arecord_cli, shell=True)
	print (f' Record Iteration number {i}')


for i in range (6):
	sox_cli =(f'sox waves{i}.wav -n rate 44k spectrogram -x 224 -y 224 -q 5 -o waves{i}.png')
	subprocess.run(args = sox_cli, shell= True)
	print (f' Spectrogram created for {i}')

print (f'All Done')

