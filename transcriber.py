#!/usr/bin/env python
import whisper
import os
import glob
import rospy
from geometry_msgs.msg import Twist
import re

# find most recent files in a directory
rospy.init_node('transcriber')
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=5)
recordings_dir = os.path.join('recordings', '*')

model = whisper.load_model("small")

rate = rospy.Rate(10)
velocity_msg = Twist()
# list to store which wav files have been transcribed
transcribed = []
try:
    while not rospy.is_shutdown():
        # get most recent wav recording in the recordings directory
        files = sorted(glob.iglob(recordings_dir),
                       key=os.path.getctime, reverse=True)
        if len(files) < 1:
            continue

        latest_recording = files[0]
        latest_recording_filename = latest_recording.split('/')[1]

        if os.path.exists(latest_recording) and not latest_recording in transcribed:
            audio = whisper.load_audio(latest_recording)
            audio = whisper.pad_or_trim(audio)
            mel = whisper.log_mel_spectrogram(audio).to(model.device)
            options = whisper.DecodingOptions(language='en', fp16=False)

            result = whisper.decode(model, mel, options)

            if result.no_speech_prob < 0.5:
                # print(result.text)
                p = re.findall(r'\b\w+\b', result.text)
                for i in p:
                    if i == 'forward':
                        velocity_msg.linear.x = 2
                pub.publish(velocity_msg)
                # append text to transcript file
                with open("transcriptions/transcript.txt", 'a') as f:
                    f.write(result.text)

                # save list of transcribed recordings so that we don't transcribe the same one again
                transcribed.append(latest_recording)

except KeyboardInterrupt:
    print("Closing transcription")
    for filename in glob.glob("recordings/*.wav*"):
        os.remove(filename)
