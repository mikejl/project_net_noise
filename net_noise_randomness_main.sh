#!/bin/bash

# #########################################################
#  net_noise_randomness_main.sh
#  24-May-2017
#  Mike Libassi
# 
# Input - number of seconds to capture and input device
# Output - raw file to raw directory
# Needs: sox, hex2bin.pl, dieharder, make_bitmap, 
# ###########################################################

# Params
SR=$1
IDEV=$2
OUTDIR="/media/pi/SD64/raw"
ANALYSISDIR="/media/pi/SD64/analysis"
DTS=$(date +%m%d%y)
OUTFILE="raw-sample_$1_$2_$DTS.raw"
OUTFILEB="raw-sample_$1_$2_$DTS.binary"
OUTFILEW="raw-sample_$1_$2_$DTS.wav"
OUTFILESPC="raw-sample_$1_$2_$DTS.png"
OUTFILEHEXSTACK="raw-sample_$1_$2_$DTS.hexstack"
OUTFILEBINSTACK="raw-sample_$1_$2_$DTS.binstack"
OUTMONOBIT="monobit_sample_$1_$2_$DTS.txt"
OUTBITMAP="bitmap_$1_$2_$DTS.pgm"
OUTBINSTATS="bitstats_sample_$1_$2_$DTS.txt"

# Usage
if [ "${#}" != 2 ] ; then
   /bin/echo "Usage ./rawgen.sh <number of seconds to capture> <input device..i.e eth0>"
   exit 1;
fi

# Check for outdir
if [ ! -d "$OUTDIR" ] ; then
   /bin/echo "Output directory: $OUTDIR does not exist.. exit"
   exit 1;
fi

if [ ! -d "$ANALYSISDIR" ] ; then
   /bin/echo "Output directory: $ANALYSISDIR does not exist.. exit"
   exit 1;
fi

/bin/echo "Output raw directory: $OUTDIR"
/bin/echo "Output analysis directory: $ANALYSISDIR"

if [ ! -f "make_bitmap" ]; then
   /bin/echo "no make_bitmap in wokring directory"
   exit 1;
fi

if [ ! -f "binstack-stats.py" ]; then
   /bin/echo "no binstack-stats.py in wokring directory"
   exit 1;
fi

if [ ! -f "hex2bin.pl" ]; then
   /bin/echo "no hex2bin.pl in wokring directory"
   exit 1;
fi

/bin/echo "Systems are ready"
read -p "Continue? (Y/N)" -n 1 -r
if [[ $REPLY =~ ^[Nn]$ ]]
then
  /bin/echo "  Exiting..."
  exit 1;
fi

# Capture
/usr/bin/tshark -i $IDEV -a duration:$SR -w - > $OUTDIR/$OUTFILE

# Generate binary with xxd
/usr/bin/xxd -b $OUTDIR/$OUTFILE | awk {'print $2" "$3" "$4" "$5" "$6" "$7'} > $OUTDIR/$OUTFILEB
/usr/bin/xxd -ps $OUTDIR/$OUTFILE $OUTDIR/$OUTFILEHEXSTACK

# Generate raw bits
/bin/echo "Generating raw binary stack.."
/usr/bin/perl hex2bin.pl $OUTDIR/$OUTFILEHEXSTACK > $OUTDIR/$OUTFILEBINSTACK
sleep 2

# Generte wav and spectrogram.png files
/usr/bin/sox -V -t ima -r 44100 -e ima-adpcm $OUTDIR/$OUTFILE -e signed-integer -b16 $OUTDIR/$OUTFILEW
/usr/bin/sox $OUTDIR/$OUTFILEW -n spectrogram
/bin/mv spectrogram.png $OUTDIR/$OUTFILESPC

# Play audio and open spectrogram
/usr/bin/play $OUTDIR/$OUTFILEW stats
/usr/bin/gpicview $OUTDIR/$OUTFILESPC &

# Run Analysis
/bin/echo "Running monobit testing and generating bitmap on binstack data"
/usr/bin/dieharder -f $OUTDIR/$OUTFILEBINSTACK -d 209 > $ANALYSISDIR/$OUTMONOBIT &
/bin/cat $OUTDIR/$OUTFILEBINSTACK | ./make_bitmap 800 800 && /bin/mv bitmap.pgm $ANALYSISDIR/$OUTBITMAP &
/usr/bin/python binstack-stats.py $OUTDIR/$OUTFILEBINSTACK >> $ANALYSISDIR/$OUTBINSTATS &
/bin/echo "Check analysis directory for results"

# END Of SCRIPT
/bin/echo " "
