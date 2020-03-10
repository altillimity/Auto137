import subprocess
import os
import time
import core
from datetime import datetime, timedelta
from core import Recording

# APT Pass record function
def recordAPT(satellite, end_time):
    print("AOS " + satellite.name + "...")

    filename = satellite.name + " at " + str(datetime.utcnow())
    print("Saving as '" + filename + "'")

    command = "rtl_fm -f " + str(satellite.frequency) + "M -M mbfm -s 60000 -r 48000 - | ffmpeg -f s16le -channels 1 -sample_rate 48k -i pipe:0 -f wav '" + filename + ".wav'"
    subprocess.Popen([command], shell=1)

    while end_time >= datetime.utcnow():
        time.sleep(1)
    
    subprocess.Popen("killall rtl_fm".split(" "))

    print("LOS " + satellite.name + "...")
    time.sleep(10)
    core.decoding_queue.append(Recording(satellite, filename))

# LRPT Pass record function
def recordLRPT(satellite, end_time):
    print("AOS " + satellite.name + "...")

    filename = satellite.name + " at " + str(datetime.utcnow())
    print("Saving as '" + filename + "'")

    command = "rtl_fm -M raw -s 140000 -f " + str(satellite.frequency) + "M -E dc '" + filename + ".raw'"
    subprocess.Popen([command], shell=1)

    while end_time >= datetime.utcnow():
        time.sleep(1)
    
    subprocess.Popen("killall rtl_fm".split(" "))

    print("LOS " + satellite.name + "...")
    time.sleep(10)
    core.decoding_queue.append(Recording(satellite, filename))

# Downlink mode redirection
def recordPass(satellite, end_time):
    core.radio_lock.acquire()
    if satellite.downlink == "APT":
        recordAPT(satellite, end_time)
    elif satellite.downlink == "LRPT":
        recordLRPT(satellite, end_time)
    core.radio_lock.release()

# Decode APT file
def decodeAPT(filename):
    print("Decoding '" + filename + "'...")
    command = "noaa-apt '" + filename + ".wav' -o '" + filename + ".png'"
    if subprocess.Popen([command], shell=1).wait() == 0:
        os.remove(filename + ".wav")
    print("Done decoding'" + filename + "'!")

# Decode LRPT file
def decodeLRPT(filename):
    print("Demodulating '" + filename + "'...")
    command = "meteor_demod -B -s 140000 '" + filename + ".raw' -o '" + filename + ".lrpt'"
    if subprocess.Popen([command], shell=1).wait() == 0:
        os.remove(filename + ".raw")
    print("Decoding '" + filename + "'...")
    command1 = "medet '" + filename + ".lrpt' '" + filename + " - Visible' -r 65 -g 65 -b 64"
    command2 = "medet '" + filename + ".lrpt' '" + filename + " - Infrared' -r 68 -g 68 -b 68"
    if subprocess.Popen([command1], shell=1).wait() == 0 and subprocess.Popen([command2], shell=1).wait() == 0:
        os.remove(filename + ".raw")
    print("Done decoding'" + filename + "'!")

# Redirect to the right decoder function
def decodePass(filename, satellite):
    if satellite.downlink == "APT":
        decodeAPT(filename)
    if satellite.downlink == "LRPT":
        decodeLRPT(filename)

# Process pending decodings
def processDecodeQueue():
    while True:
        time.sleep(1)
        if len(core.decoding_queue) > 0:
            decode = core.decoding_queue[0]
            decodePass(decode.filename, decode.satellite)
            core.decoding_queue.remove(decode)