from pydub import AudioSegment
from pydub.silence import split_on_silence
import os
country = ["Trinidad","Tobago","Barbados","St.Lucia"]
code = ["T","TB","B","S"]
index =0
for c in country:
    i=0
    for filename in os.listdir("./Countries/"+c+"/slow/"): 
        sound_file = AudioSegment.from_wav(filename)
        audio_chunks = split_on_silence(sound_file, 
            # must be silent 
            # for at least 1/10 of a second
            min_silence_len=100,
            # consider it silent if quieter than -40 dBFS
            silence_thresh=-40        )
        for k,chunk in enumerate(audio_chunks):
            out_file = "./Countries/"+c+"/segment/"+code[index]+"{0}.wav".format(i)
            chunk.export(out_file, format="wav")
            i=i+1
    index = index +1
