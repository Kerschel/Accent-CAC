import helpers as speech
import sys
import accuracy
import multiprocessing
from keras.models import load_model
from collections import Counter
DEBUG = True


def predict(X_test):
    # X_test =["",""]
    print("here")
    # Get resampled wav files using multiprocessing
    print (X_test)
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    X_test = pool.map(speech.get_wav, X_test)

    X_test = pool.map(speech.to_mfcc, X_test)

    model = load_model("predictionmodel.h5")
    items = []
    y_predicted = accuracy.predict_class_all(speech.create_segmented_mfccs(X_test), model)
    for i in y_predicted:
      items.append(i)
    data = Counter(items)
    classes = {0:"Trinidad",1:"Tobago",2:"Barbados",3:"St. Lucia"}
    return classes[data.most_common(1)[0][0]]

if __name__ == "__main__":
  print(predict(['L1','L2','L3']))