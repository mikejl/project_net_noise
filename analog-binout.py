#!/usr/bin/env python
# binstack-stats.py
# Mike Libassi
# 6/7/17
#
# in: time to record ADC binary values
# out: outfile
#
# #################################################
import time
import os
import sys
import RPi.GPIO as GPIO
import subprocess

# Mode setup
GPIO.setmode(GPIO.BCM)
DEBUG = 1
GPIO.setwarnings(False)

# Inputs
rectime = sys.argv[1]
#binfile = sys.argv[2]
binfile = "test.out"

# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
        if ((adcnum > 7) or (adcnum < 0)):
                return -1
        GPIO.output(cspin, True)
        GPIO.output(clockpin, False)  # start clock low
        GPIO.output(cspin, False)     # bring CS low

        commandout = adcnum
        commandout |= 0x18  # start bit + single-ended bit
        commandout <<= 3    # we only need to send 5 bits here
        for i in range(5):
                if (commandout & 0x80):
                        GPIO.output(mosipin, True)
                else:
                        GPIO.output(mosipin, False)
                commandout <<= 1
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)

        adcout = 0
        # read in one empty bit, one null bit and 10 ADC bits
        for i in range(12):
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)
                adcout <<= 1
                if (GPIO.input(misopin)):
                        adcout |= 0x1

        GPIO.output(cspin, True)

        adcout >>= 1       # first bit is 'null' so drop it
        return adcout

# SPI pinout
SPICLK = 11
SPIMISO = 9
SPIMOSI = 10
SPICS = 8

# set up the SPI interface pins
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

# 10k and LDR Voltage divider connected to adc #0
ldr_adc = 0


# Open file for writing
outf = open(binfile, "w")

# Setup counter
counter = int(rectime)

while (counter > 0):
        analog_read = readadc(ldr_adc, SPICLK, SPIMOSI, SPIMISO, SPICS)
        binout = '{:08b}'.format(analog_read)
        hexout = '{:02x}'.format(analog_read)
        print "Analog: ", analog_read
        print "Binary: ", binout
        print "Hex: ", hexout
        outf.write(binout)
        #outf.write(hexout)
        counter -= 1
        #time.sleep(1) # 1 sec sleep for throttling / testing



# close file
outf.write('\n') # insert line feed
outf.close()


# Generte bitmap and spectrogram files
#/usr/bin/sox -V -t ima -r 44100 -e ima-adpcm $OUTDIR/$OUTFILE -e signed-integer -b16 $OUTDIR/$OUTFILEW
#/usr/bin/sox $OUTDIR/$OUTFILEW -n spectrogram
#cat test.out | ./make_bitmap2  250 250

print "Generate spectrogram and bitmap?"
YN=raw_input("Y/N: ")
if YN == "Y":
        subprocess.call(['/usr/bin/sox -V -t ima -r 44100 -e ima-adpcm test.out -e signed-integer -b16 test.wav'], shell=True)
        subprocess.call(['/usr/bin/sox test.wav -n spectrogram'], shell=True)
        subprocess.call(['/bin/cat test.out | ./make_bitmap2  250 250'], shell=True)
        print "test.out  spectrogram and bitmap generated in local dir"

# Wrap-up
GPIO.cleanup

# END