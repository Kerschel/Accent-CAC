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
country = ["Trinidad", "Tobago", "Barbados", "St. Lucia"]
for c in country:
    for filename in os.listdir("./Countries/"+c+"/normalized/"): 
        path = os.path.join("./Countries/"+c+"/normalized/", filename)
        if not os.path.isdir(path):
            sound = AudioSegment.from_file("./Countries/"+c+"/"+filename)
            # reduce rate by a factor of 0.4
            slow_sound = speed_change(sound, 0.4)
            slow_sound.export("./Countries/"+c+"/slow/"+filename, format="wav")
