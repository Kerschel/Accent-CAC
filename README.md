# Accent Prediction API
To run the flask server use 
```bash
python server.py
```
[server.py](server.py) is the Flask API server we are referring to
The server will start on localhost. The folder contains the prediction model for classifying the accents based on the incomming audio.
It accepts 3 audio files then finds the classification of each. It then finds the mode classification and returns it to the user.
The files are sent to the /save and endpoint and saved in the directory for prediction.
[prediction.py](prediction.py) is used to classify the accents and is classed when a user hits the /predict endpoint.
