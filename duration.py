import pandas as pd
import os
import wave
import contextlib
def getlength(fname):
  try:
    with contextlib.closing(wave.open("./ES1/"+fname,'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
        return duration
  except:
    return 0
# gets the length of the audio file and saves it in the csv file
df = pd.read_csv("./ES1.csv",encoding='ISO-8859-1')
dur = []
for name in df.Filename.values:
  dur.append(getlength (name+".wav"))
df['duration'] = dur

df.to_csv("data.csv", sep=',', encoding='ISO-8859-1')
