import helpers as k
import pandas as pd
from collections import Counter
from keras.callbacks import CSVLogger
import sys
import getsplit
import csv
from keras import utils
import accuracy
import multiprocessing
import librosa
import numpy as np
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Flatten
from keras.layers.convolutional import MaxPooling2D, Conv2D
from keras.layers.normalization import BatchNormalization
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import EarlyStopping, TensorBoard
from keras.models import load_model
import tensorflow as tf

DEBUG = True
SILENCE_THRESHOLD = .01
RATE = 24000
N_MFCC = 13
COL_SIZE = 30
EPOCHS = 10 #35#250

def train_model(X_train,y_train,X_validation,y_validation, batch_size=128): #64
    '''
    Trains 2D convolutional neural network
    :param X_train: Numpy array of mfccs
    :param y_train: Binary matrix based on labels
    :return: Trained model
    '''

    # Get row, column, and class sizes
    rows = X_train[0].shape[0]
    cols = X_train[0].shape[1]
    val_rows = X_validation[0].shape[0]
    val_cols = X_validation[0].shape[1]
    num_classes = len(y_train[0])

    # input image dimensions to feed into 2D ConvNet Input layer
    input_shape = (rows, cols, 1)
    X_train = X_train.reshape(X_train.shape[0], rows, cols, 1 )
    X_validation = X_validation.reshape(X_validation.shape[0],val_rows,val_cols,1)
    device_name = "/device:GPU:1"
    # device_name = "/cpu:0"
    
    with tf.device(device_name):
        print("Using: {0}".format(device_name))
        print('X_train shape:', X_train.shape)
        print(X_train.shape[0], 'training samples')

        # model = Sequential()

        # model.add(Conv2D(32, 
        #                 kernel_size=(3,3), 
        #                 activation='relu',
        #                 data_format="channels_last",
        #                 input_shape=input_shape))
        # model.add(BatchNormalization())
        # model.add(MaxPooling2D(pool_size=(2, 2)))
        
        # model.add(Conv2D(64,
        #                 kernel_size=(3,3), 
        #                 activation='relu'))
        # model.add(BatchNormalization())
        # model.add(MaxPooling2D(pool_size=(2, 2)))
        # model.add(Dropout(0.30))

        # model.add(Flatten())
        # model.add(Dense(256, activation='relu'))
        # model.add(Dropout(0.30))

        # model.add(Dense(num_classes, activation='softmax'))
        # model.compile(loss='categorical_crossentropy',
        #               optimizer='adam',
        #               metrics=['accuracy'])


        model = Sequential()
        model.add(Conv2D(32, kernel_size=(3,3), activation='relu',
                        data_format="channels_last",
                        input_shape=input_shape))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Conv2D(64,kernel_size=(3,3), activation='relu'))
        model.add(BatchNormalization())
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.30))

        model.add(Flatten())
        model.add(Dense(256,kernel_regularizer= keras.regularizers.l2(0.001) , activation='relu'))
        model.add(Dropout(0.50))

        model.add(Dense(num_classes, activation='softmax'))
        model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])


        # Stops training if loss gets worst
        es = EarlyStopping(monitor='val_loss', patience=10, verbose=1, mode='auto')

        # Creates log file for graphical interpretation using TensorBoard
        tb = TensorBoard(log_dir='../logs', histogram_freq=0, batch_size=32, write_graph=True, write_grads=True,
                         write_images=True, embeddings_freq=0, embeddings_layer_names=None,
                         embeddings_metadata=None)

        # Image shifting
        datagen = ImageDataGenerator(width_shift_range=0.05)

        # Fit model using ImageDataGenerator
        csv_logger = CSVLogger('train-validation.csv', append=True, separator=',')
        model.fit_generator(datagen.flow(X_train, y_train, batch_size=batch_size),
                            steps_per_epoch=len(X_train) / 32
                            , epochs=EPOCHS,
                            callbacks=[es,tb,csv_logger], validation_data=(X_validation,y_validation))
        # model.fit(X_train,y_train,batch_size=batch_size,epochs=EPOCHS)

        return (model)

def save_model(model, model_filename):
    '''
    Save model to file
    :param model: Trained model to be saved
    :param model_filename: Filename
    :return: None
    '''
    model.save('{}.h5'.format(model_filename))  # creates a HDF5 file 'my_model.h5'



############################################################

#######################################

if __name__ == '__main__':
    '''
        Console command example:
        python trainmodel.py bio_metadata.csv model50
        '''
    results=[]
    acc = []
    
    # Load arguments
    file_name = sys.argv[1]
    model_filename = sys.argv[2]
    csvfile = sys.argv[3]
    # Load metadata
    df = k.pd.read_csv(file_name,encoding='ISO-8859-1')
    df = df[df.Filename != 'undefined']
    df = df[df.Words != 'undefined']
    if (csvfile =="ES1.csv"):
        df = df[df.duration >=10]
    if (csvfile =="ES2.csv"):
        df = df[df.duration >=1]
    if (csvfile =="ES3.csv"):
        df = df[df.duration >=2]
    # # Filter metadata to retrieve only files desired
    filtered_df = getsplit.filter_df(df)
    # Train test split
    X_train, X_test, y_train, y_test = k.getsplit.split_people(filtered_df)
    # Get statistics

    # print (y_train)
    train_count = k.Counter(y_train)
    test_count = k.Counter(y_test)

    print("Entering main")

    # import ipdb
    # ipdb.set_trace()


    acc_to_beat = test_count.most_common(1)[0][1] / float(np.sum(list(test_count.values())))
    # print (y_train)
    # To categorical
    y_train = k.to_categorical(y_train)
    # print (y_train)
    
    y_test = k.to_categorical(y_test)

    # Get resampled wav files using multiprocessing
    if DEBUG:
        print('Loading wav files....')
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    X_train = pool.map(k.get_wav, X_train)
    X_test = pool.map(k.get_wav, X_test)

        # Convert to MFCC
    if DEBUG:
        print('Converting to MFCC....')
    X_train = pool.map(k.to_mfcc, X_train)
    X_test = pool.map(k.to_mfcc, X_test)

    # Create segments from MFCCs
    X_train, y_train = k.make_segments(X_train, y_train)
    X_validation, y_validation = k.make_segments(X_test, y_test)
    # print (X_train)

    X_train, _, y_train, _ = train_test_split(X_train, y_train, test_size=0)
    # trainer = (np.array(X_train) / np.amax(X_train)).astype(np.float32)
    # Randomize training segments
#     # print (np.array(X_train))
#     # print ("MAX IS HERE ", np.amax(np.array(X_train)))
#     # print (trainer)
    for i in range (0,1):

        print (y_train)
    #     # Train model
        model = train_model(np.array(X_train), np.array(y_train), np.array(X_validation),np.array(y_validation))
        # print (model.summary())
        # score = model.evaluate(X_validation, y_validation,  verbose=1)
        # print (score)
    #     # model = load_model("model.h5")
    #     # predicted = model.predict (k.create_segmented_mfccs(X_test))
    #     # for i in predicted:
    #     #     print (i)
    #     # Make predictions on full X_test MFCCs
        y_predicted = accuracy.predict_class_all(k.create_segmented_mfccs(X_test), model)
        print('Training samples:', train_count)
        print('Testing samples:', test_count)
        print('Accuracy to beat:', acc_to_beat)
        print('Confusion matrix of total samples:\n', np.sum(accuracy.confusion_matrix(y_predicted, y_test),axis=1))
        print('Confusion matrix:\n',accuracy.confusion_matrix(y_predicted, y_test))
        print('Accuracy:', accuracy.get_accuracy(y_predicted,y_test))

        results.append(accuracy.confusion_matrix(y_predicted, y_test))
        acc.append(accuracy.get_accuracy(y_predicted,y_test))
        with open(csvfile, 'a') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow([i,accuracy.get_accuracy(y_predicted,y_test)])
#     # Save model
# print (results)
# print (acc)
    save_model(model, model_filename)