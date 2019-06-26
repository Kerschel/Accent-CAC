from pydub import AudioSegment
import pandas as pd
import os
import wave
import contextlib
def getlength(fname):
  with contextlib.closing(wave.open("./Countries/Caribbean/"+fname,'r')) as f:
      frames = f.getnframes()
      rate = f.getframerate()
      duration = frames / float(rate)
      return duration
for filename in os.listdir("./Countries/Caribbean"):
    path = os.path.join("./Countries/Caribbean/", filename)
    if not os.path.isdir(path):
      audio = AudioSegment.from_wav("./Countries/Caribbean/"+filename)
      length = getlength(filename)
      # pad all files within range to be 1 second long
      if length > .1 and length <= .8:
        pad_ms = 1000  # milliseconds of silence needed
        new = pad_ms - (length*1000)
        pad_ms = abs(new)
        silence = AudioSegment.silent(duration=pad_ms)
        padded = audio + silence  # Adding silence after the audio
        padded.export('./Countries/Caribbean/padded/'+filename, format='wav')
      else:
        # if  length of file >.8 keep else discard the others because they contain nothing
        if length > .8:
          audio.export('./Countries/Caribbean/padded/'+filename, format='wav')
