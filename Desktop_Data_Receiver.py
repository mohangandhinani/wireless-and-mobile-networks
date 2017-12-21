#########################################################
# Desktop_Data_Receiver.py
#########################################################

import pyaudio
import sys
import numpy as np
import aubio
import time

#########################################################
# Decode the character received based on the frequency
#########################################################
def get_character(xpitch):

    if   (xpitch >= 441 and xpitch <= 445):
        return 'a'
    elif (xpitch >= 466 and xpitch <= 470):
        return 'b'
    elif (xpitch >= 487 and xpitch <= 491):
        return 'c'
    elif (xpitch >= 505 and xpitch <= 510):
        return 'd'
    elif (xpitch >= 522 and xpitch <= 526):
        return 'e'
    elif (xpitch >= 536 and xpitch <= 540):
        return 'f'
    elif (xpitch >= 550 and xpitch <= 554):
        return 'g'
    elif (xpitch >= 562 and xpitch <= 566):
        return 'h'
    elif (xpitch >= 573 and xpitch <= 577):
        return 'i'
    elif (xpitch >= 583 and xpitch <= 587):
        return 'j'
    elif (xpitch >= 592 and xpitch <= 598):
        return 'k'
    elif (xpitch >= 601 and xpitch <= 605):
        return 'l'
    elif (xpitch >= 610 and xpitch <= 614):
        return 'm'
    elif (xpitch >= 618 and xpitch <= 622):
        return 'n'
    elif (xpitch >= 625 and xpitch <= 629):
        return 'o'
    elif (xpitch >= 632 and xpitch <= 636):
        return 'p'
    elif (xpitch >= 639 and xpitch <= 643) or (xpitch >= 543 and xpitch <= 547):
        return 'q'
    elif (xpitch >= 646 and xpitch <= 650):
        return 'r'
    elif (xpitch >= 652 and xpitch <= 656):
        return 's'
    elif (xpitch >= 658 and xpitch <= 662):
        return 't'
    elif (xpitch >= 663 and xpitch <= 667):
        return 'u'
    elif (xpitch >= 669 and xpitch <= 673):
        return 'v'
    elif (xpitch >= 674 and xpitch <= 678):
        return 'w'
    elif (xpitch >= 679 and xpitch <= 683):
        return 'x'
    elif (xpitch >= 684 and xpitch <= 688):
        return 'y'
    elif (xpitch >= 688 and xpitch <= 693):
        return 'z'
    elif (xpitch >= 878 and xpitch <= 882) or (xpitch > 650 and xpitch < 652):
        return ' '
    else:
        return ''

# Initialize pyaudio
p = pyaudio.PyAudio()

# Open the Audio stream
buff_sz   = 1024
samp_rate = 44100
stream    = p.open(format = pyaudio.paFloat32,
                   channels = 1,
                   rate = samp_rate,
                   input = True,
                   frames_per_buffer = buff_sz)

outputsink      = None
record_duration = None

# Setup pitch
tolerance  = 0.8

# FFT size
win_s      = 4096

# hop size
hop_s      = buff_sz

samp       = 0
char_found = 0
prev_char  = '-'

pitch_o = aubio.pitch("default", win_s, hop_s, samp_rate)
pitch_o.set_unit("midi")
pitch_o.set_tolerance(tolerance)


print("\nStarting Recording\n")
print "Received Message : ",

while True:
    try:
        audiobuffer = stream.read(buff_sz)
        signal = np.fromstring(audiobuffer, dtype=np.float32)

        pitch = pitch_o(signal)[0]
        confidence = pitch_o.get_confidence()
        
        samp += 1
        if samp == 10:
            xpitch = pitch * 8
            if confidence > 0.8 and xpitch > 440 and xpitch < 900:
                c = get_character(xpitch)
                if prev_char == c:
                    char_found += 1
                    if char_found == 3:
                        sys.stdout.write(c)
                        char_found = 0
                else:
                    char_found = 0
                prev_char = c
            samp = 0

        if outputsink:
            outputsink(signal, len(signal))

        if record_duration:
            total_frames += len(signal)
            if record_duration * samp_rate < total_frames:
                break
                
    except KeyboardInterrupt:
        print("Ctrl+C pressed, exiting")
        break

print("Stopping Recording")
stream.stop_stream()
stream.close()
p.terminate()

#########################################################
# References
#########################################################
#
# 1) Aubio Demo : https://github.com/aubio/aubio/blob/master/python/demos/demo_pyaudio.py
