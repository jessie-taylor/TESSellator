import numpy as np
#from keras.utils import to_categorical # COMMENTED WHILE TESTING
from sklearn.model_selection import train_test_split
#import keras
#from keras.models import Sequential, Input, Model
#from keras.layers import Dense, Dropout, Flatten
#from keras.layers import Conv2D, MaxPooling2D
#from keras.layers.normalization import BatchNormalization  # ALL THESE [LINES 4-9 COMMENTED WHILE TESTING
#from keras.layers.advanced_activations import LeakyReLU
import matplotlib.pyplot as plt

# Loading the training as the first 1000 images and test as final 259.
arraydir = './DATA/arrays/'

train_Xgd1 = np.load(arraydir + 'gdor_387.npy')
#train_Ygd = np.load('GdClass.npy')

train_Xds1 = np.load(arraydir + 'dsct_154.npy')
#train_Yds = np.load('dsc.npy')

# train_Xhyb1 = np.load(arraydir + 'New_HybridArray.npy')
#train_Yhyb = np.load('hybridclass.npy')

# As there is more than 1 array for nvs:
non1 = np.load(arraydir + "nv_1000.npy")
non2 = np.load(arraydir + "nv_2000.npy")
non3 = np.load(arraydir + "nv_2800.npy")
print("about to concatenate")
train_Xnon1 = np.concatenate((non1, non2, non3), axis = 2)
print("concatenated")
# Clearing up some memory
non1 = 0
non2 = 0
non3 = 0
#train_Xnon1 = np.load(arraydir + 'nv_1000.npy')

train_Xbin1 = np.load(arraydir + 'ebs_501.npy')

train_Xrrlyr1 = np.load(arraydir + "rrlyr_46.npy")

train_Xgd =train_Xgd1.transpose(2, 0, 1)
train_Xds =train_Xds1.transpose(2, 0, 1)
# train_Xhyb =train_Xhyb1.transpose(2, 0, 1)
train_Xnon =train_Xnon1.transpose(2, 0, 1)
train_Xbin = train_Xbin1.transpose(2,0,1)
train_Xrrlyr = train_Xrrlyr1.transpose(2,0,1)

train_Ygd=np.full(train_Xgd.shape[0], 1)
train_Yds=np.full(train_Xds.shape[0], 2)
#train_Yhyb=np.full(train_Xhyb.shape[0], 5)
train_Ynon=np.full(train_Xnon.shape[0], 0)
train_Ybin=np.full(train_Xbin.shape[0], 3) 
train_Yrrlyr = np.full(train_Xrrlyr.shape[0], 4)

# Setting the numbers to use as training sets 
# if these say 1000 in the index ranges then it uses the first 1000 
# to train and then the remainder for testing
# Using 10% for the testing at this point, hence the round(TOTAL/10) function
# to save 90% for training
def ninety_perc(arrayname):
  amount = arrayname.shape[0] - round(arrayname.shape[0]/10)
  return amount

#get 90% of total GDs first
gd_90 = ninety_perc(train_Xgd)
test_Xgd = train_Xgd[gd_90::]
test_Ygd = train_Ygd[gd_90::]
train_Xgd = train_Xgd[:gd_90:]
train_Ygd = train_Ygd[:gd_90:]

ds_90 = ninety_perc(train_Xds)
test_Xds = train_Xds[ds_90::]
test_Yds = train_Yds[ds_90::]
train_Xds = train_Xds[:ds_90:]
train_Yds = train_Yds[:ds_90:]

#hyb_90 = ninety_perc(train_Xhyb)
#test_Xhyb = train_Xhyb[1000::]
#test_Yhyb = train_Yhyb[1000::]
#train_Xhyb = train_Xhyb[:1000:]
#train_Yhyb = train_Yhyb[:1000:]

non_90 = ninety_perc(train_Xnon)
test_Xnon = train_Xnon[non_90::]
test_Ynon = train_Ynon[non_90::]
train_Xnon = train_Xnon[:non_90:]
train_Ynon = train_Ynon[:non_90:]
#print(train_Xnon.shape, train_Ynon.shape)

bin_90 = ninety_perc(train_Xbin)
test_Xbin = train_Xbin[bin_90::]
test_Ybin = train_Ybin[bin_90::]
train_Xbin = train_Xbin[:bin_90:]
train_Ybin = train_Ybin[:bin_90:]

rrlyr_90 = ninety_perc(train_Xrrlyr)
test_Xrrlyr = train_Xrrlyr[rrlyr_90::]
test_Yrrlyr = train_Yrrlyr[rrlyr_90::]
train_Xrrlyr = train_Xrrlyr[:rrlyr_90:]
train_Yrrlyr = train_Yrrlyr[:rrlyr_90:]


test_X = np.concatenate([test_Xnon, test_Xgd, test_Xds, 
                         test_Xbin, test_Xrrlyr])

test_Y = np.concatenate([test_Ynon, test_Ygd, test_Yds,
                         test_Ybin, test_Yrrlyr])


train_X = np.concatenate([train_Xnon, train_Xgd, train_Xds, 
                          train_Xbin, train_Xrrlyr])

train_Y = np.concatenate([train_Ynon, train_Ygd, train_Yds,
                          train_Ybin, train_Yrrlyr])

np.save('./model/test_image_data.npy', test_X)

print(test_X.shape, test_Y.shape, train_X.shape, train_Y.shape)


permutation = np.random.permutation(len(train_X))
train_X = train_X[permutation]
train_Y = train_Y[permutation]
print("Train Permutation: ",permutation)

# Keeping the final permutation saved for safety.

text_file = open("FinalTrainPermutation.txt", "w")


# Writes the permutation to a text file so we can find star images in later predicted classes
# this helps us find the stars with high/low confidence/accuracy. It's good stuff as we can run a script to
# compare class here with the predicted version in the output of Preediction.py

position = 0

for image in permutation:
    text_file.write(str(position) + ":" + str(image)+", class: " + str(train_Y[position])+"\n")
    position += 1
text_file.close()

z = 0

for x in train_Y:
    if x == 0:
        z += 1
print("GD=", z, "\n")

#print("-1?", train_X.shape[0])
# Reshapes the array into one suitable for CNN
train_X = train_X.reshape(-1, 480, 640, 1)
test_X = test_X.reshape(-1, 480, 640, 1)
train_X = train_X.astype('float32')
test_X = test_X.astype('float32')
# Takes it down to 0 or 1 pixel values. Simpler.
train_X = train_X / 255.
test_X = test_X / 255.

print(test_X.shape, test_Y.shape, train_X.shape, train_Y.shape)

# Change the labels from categorical to one-hot encoding meaning the model cannot say that class 3 is more important
# than class 2.
train_Y_one_hot = to_categorical(train_Y)
test_Y_one_hot = to_categorical(test_Y)

# Display the change for category label using one-hot encoding
print('Original label:', train_Y[0], train_Y[1], train_Y[2],train_Y[3], train_Y[4], train_Y[5])
print('After conversion to one-hot:', train_Y_one_hot[0], train_Y_one_hot[1], train_Y_one_hot[2] )
print('test Original label:', test_Y[0])
print('test After conversion to one-hot:', test_Y_one_hot[0])

# Splits data into 80% training 20% validation
train_X, valid_X, train_label, valid_label = train_test_split(train_X, train_Y_one_hot, test_size=0.3, random_state=13)

# Number of images per batch, updated weights afterwards. Small is faster and easier, but less accurate at
# guessing the gradient, as high number batches have a lot more info per update.
batch_size = 2
# Number of runs through all data.
epochs = 20
# Used for plotting results later. Number of classes duh.
num_classes = 5




# Every layer of the algorithm added one at a time. Sequential model with the input shape we used earlier. Linear
# activation with LeakyRelu added in the layer after.
classifier = Sequential()
classifier.add(Conv2D(32, kernel_size=(3, 3), activation='linear', input_shape=(480, 640, 1), padding='same'))
classifier.add(LeakyReLU(alpha=0.1))


# Literally the mot important line of code. Without these, EVERY prediction is the same confidence and value giving a completely wrong total result.
classifier.add(BatchNormalization())

# Read the thesis on this stuff. Max pooling is basically simplifying it from what I recall.
classifier.add(MaxPooling2D((2, 2), padding='same'))
classifier.add(Conv2D(64, (2, 2), activation='linear', padding='same'))

classifier.add(LeakyReLU(alpha=0.1))
classifier.add(BatchNormalization())

classifier.add(MaxPooling2D(pool_size=(2, 2), padding='same'))

classifier.add(Flatten())
# Prevents overfitting.
classifier.add(Dropout(0.5))

classifier.add(Dense(64, activation='linear'))
classifier.add(LeakyReLU(alpha=0.1))
# 4: class 0 or class 1 2 3
classifier.add(Dense(5, activation='softmax'))

# Finally compiling all layers with the most accurate lr and metric. Categorical gives us prediction weightings too, I
# think. Still, can't use binary so.
classifier.compile(loss=keras.losses.categorical_crossentropy,
                   optimizer=keras.optimizers.SGD(lr=0.00001, momentum=0, decay=0.0, nesterov=False),
                   metrics=['accuracy'])

# Shows some parameters in each layer and the total parameters
print(classifier.summary())

# Trains the model on the train_X data with their labels. We see variables we set earlier, validation is checking itself
# with each epoch. Verbose says how much info it gives you as it runs. It will take a while, don't think it's frozen.
history = classifier.fit(train_X, train_label, batch_size=batch_size, epochs=epochs, verbose=1,
                               validation_data=(valid_X, valid_label))




# Sets The predicted classes as what we predicted
predicted_classes = classifier.predict(test_X)

# Checks the predeicted classes. Without BN layer at the beginning they would all be the same class, so we have this
# to look it over.
try:
    print("a ", predicted_classes)
    print("b ", predicted_classes[0])
except:
    pass





# Saving the predictions and weightings for use in star analysis. before softmax. We do the same when predicting on
# all KASOC data with the same format. So simple, but so vital. This is how we find results and eliminate low confidence.
predic = 0
text_file = open("Predictions.txt", "w")

for predictionite in predicted_classes:

    text_file.write(str(predic) + ":" + str(predictionite)+"\n")
    predic += 1
text_file.close()







# Takes the max value and its position(?) in the array to find the true class. [0,1...0] -> class 1. Basically
# reverses one hot encoding.
predicted_classes = np.argmax(np.round(predicted_classes), axis=1)
print("c ", predicted_classes)
text_file = open("Predictions_max.txt", "w")

for i in range(len(predicted_classes)):
    text_file.write(str(i) + ":" + str(predicted_classes[i]) +"\t" +str(test_Y[i])+"\n")

text_file.close()








# Decide what is correct here by comparing to our initial labels.
correct = np.where(predicted_classes == test_Y)[0]
print("Final result 20 epochs Found %d correct labels" % len(correct))

# More details on accuracy. Prints out our total correct predictions in case of crashing I guess.
from sklearn.metrics import classification_report


target_names = ["Class {}".format(i) for i in range(num_classes)]
print((classification_report(test_Y, predicted_classes, target_names=target_names)))

text_file = open("Output.txt", "w")
text_file.write("\n Final result 20 epochs Found %d correct labels" % len(correct))
text_file.close()


# JT ~~ ADDED AFTER ~~
# saves the model for later use
classifier.save('./saved_classifier_model')


# This plots the accuracy over time. Was good for getting a cool graph for the thesis.





# Same for incorrect
incorrect = np.where(predicted_classes != test_Y)[0]
print("Found %d incorrect labels" % len(incorrect))


# Saves our full report.
text_file = open("results.txt", "w")


text_file.write((classification_report(test_Y, predicted_classes, target_names=target_names)))

text_file.close()


incor =0
text_file2 = open("Incorrect_results.txt", "w")

for l in incorrect:
    text_file2.write(str(incor) + ":" + str(l)+"\n")
    incor += 1
text_file2.close()
cor =0

text_file3 = open("correct_results.txt", "w")

for c in correct:
    text_file3.write(str(cor) + ":" + str(c)+"\n")
    cor += 1
text_file3.close()


print(history.history)
plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('Model accuracy over time')
plt.ylabel('Accuracy')
plt.xlabel('epoch')
plt.legend(['training', 'test'], loc='upper left')

plt.savefig('accuracytestfinal.png')

try:
    plt.clear()
except:
    pass

try:
    plt.clf()
except:
    pass

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model loss over time')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['training', 'test'], loc='upper left')

plt.savefig('Losstestfinal.png')

