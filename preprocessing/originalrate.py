from pydub import AudioSegment
import os
def speed_change(sound, speed=1.0):
    # Manually override the frame_rate. This tells the computer how many
    # samples to play per second
    sound_with_altered_frame_rate = sound._spawn(sound.raw_data, overrides={
         "frame_rate": int(sound.frame_rate * speed)
      })
     # convert the sound with altered frame rate to a standard frame rate
     # so that regular playback programs will work right. 
    return sound_with_altered_frame_rate.set_frame_rate(sound.frame_rate)
# slow down the list of countries audio file
country = ["St. Lucia"]
for c in country:
    for filename in os.listdir("./Countries/"+c+"/segment/"): 
        sound = AudioSegment.from_file("./Countries/"+c+"/segment/"+filename)
        fast_sound = speed_change(sound, 2.5)
        fast_sound.export("./Countries/Caribbean/"+filename, format="wav")
