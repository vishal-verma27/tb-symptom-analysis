import os
import cv2
cv2.startWindowThread()
from keras.models import load_model
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Dense, Flatten
from keras.optimizers import Adam
import warnings
warnings.filterwarnings('ignore')

class TuberculosisClassifier:
    def __init__(self, img_size=250):
        self.img_size = img_size
        self.TOTAL_DATA = []
        self.FEATURE_MATRIX = []
        self.TARGET = []
        self.NORMALIZED_X = []
        self.x_train, self.x_test, self.y_train, self.y_test = None, None, None, None
        self.X_train, self.X_test = None, None
        self.model = None
        self.history = None

    def otsus_binarization(self, folder, target):
        images = []
        for filename in os.listdir(folder):
            img = cv2.imread(os.path.join(folder, filename), 0)
            if img is not None:
                images.append([img, target])
        return images

    def load_data(self):
        tuberculosis = self.otsus_binarization("dataset\\TB_Chest_Radiography_Database\\Tuberculosis", 0)
        normal = self.otsus_binarization("dataset\\TB_Chest_Radiography_Database\\Normal", 1)
        self.TOTAL_DATA = tuberculosis + normal

    def preprocess_data(self):
        for x, y in self.TOTAL_DATA:
            self.FEATURE_MATRIX.append(cv2.resize(x, (self.img_size, self.img_size)))
            self.TARGET.append(y)

        for x in self.FEATURE_MATRIX:
            self.NORMALIZED_X.append(x / 255)

    def split_data(self):
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(
            self.NORMALIZED_X, self.TARGET
        )

    def reshape_data(self):
        img_rows, img_cols = self.x_train[0].shape[0], self.x_train[0].shape[1]
        self.X_train = np.array(self.x_train).reshape(
            len(self.x_train), img_rows, img_cols, 1
        )
        self.X_test = np.array(self.x_test).reshape(
            len(self.x_test), img_rows, img_cols, 1
        )

    def define_model(self):
        model = Sequential()
        model.add(
            Conv2D(
                32,
                (3, 3),
                activation="relu",
                kernel_initializer="he_uniform",
                padding="same",
                input_shape=(self.img_size, self.img_size, 1),
            )
        )
        model.add(Conv2D(32, (3, 3), activation="relu", kernel_initializer="he_uniform", padding="same"))
        model.add(Conv2D(32, (3, 3), activation="relu", kernel_initializer="he_uniform", padding="same"))
        model.add(MaxPooling2D((2, 2)))
        model.add(Conv2D(32, (3, 3), activation="relu", kernel_initializer="he_uniform", padding="same"))
        model.add(Conv2D(32, (3, 3), activation="relu", kernel_initializer="he_uniform", padding="same"))
        model.add(Conv2D(32, (3, 3), activation="relu", kernel_initializer="he_uniform", padding="same"))
        model.add(MaxPooling2D((2, 2)))
        model.add(Conv2D(64, (3, 3), activation="relu", kernel_initializer="he_uniform", padding="same"))
        model.add(Conv2D(64, (3, 3), activation="relu", kernel_initializer="he_uniform", padding="same"))
        model.add(MaxPooling2D((2, 2)))
        model.add(Conv2D(128, (3, 3), activation="relu", kernel_initializer="he_uniform", padding="same"))
        model.add(Conv2D(128, (3, 3), activation="relu", kernel_initializer="he_uniform", padding="same"))
        model.add(MaxPooling2D((2, 2)))
        model.add(Flatten())
        model.add(Dense(128, activation="relu", kernel_initializer="he_uniform"))
        model.add(Dense(128, activation="relu", kernel_initializer="he_uniform"))
        model.add(Dense(128, activation="relu", kernel_initializer="he_uniform"))
        model.add(Dense(128, activation="relu", kernel_initializer="he_uniform"))
        model.add(Dense(128, activation="relu", kernel_initializer="he_uniform"))
        model.add(Dense(128, activation="relu", kernel_initializer="he_uniform"))
        model.add(Dense(2, activation="softmax"))
        # compile model
        opt = Adam(learning_rate=0.001)
        model.compile(optimizer=opt, loss="sparse_categorical_crossentropy", metrics=["accuracy"])
        self.model = model


    def train_model(self, epochs=2):
        self.history = self.model.fit(
            np.array(self.X_train),
            np.array(self.y_train),
            epochs=epochs,
            validation_data=(self.X_test, np.array(self.y_test)),
        )

    def plot_model_history(self):
        print(self.history.history.keys())
        plt.plot(self.history.history["accuracy"])
        plt.plot(self.history.history["val_accuracy"])
        plt.title("Model Accuracy")
        plt.ylabel("Accuracy")
        plt.xlabel("Epoch")
        plt.legend(["Train", "Test"], loc="upper left")
        plt.show()

        plt.plot(self.history.history["loss"])
        plt.plot(self.history.history["val_loss"])
        plt.title("Model Loss")
        plt.ylabel("Loss")
        plt.xlabel("Epoch")
        plt.legend(["Train", "Test"], loc="upper left")
        plt.show()

    def evaluate_model(self):
        predicted = self.model.predict(np.array(self.X_test))
        result = [np.argmax(item) for item in predicted]

        # Confusion Matrix
        cm = confusion_matrix(self.y_test, result)
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
        plt.title('Confusion Matrix')
        plt.xlabel('Predicted')
        plt.ylabel('Actual')
        plt.show()

        # Classification Report
        print("Classification Report:")
        print(classification_report(self.y_test, result))

    def save_model(self, model_path="tuberculosis_model.h5"):
        """
        Save the trained model to a file.

        Parameters:
            model_path (str): Path to save the model file.
        """
        if self.model is not None:
            model_path = os.path.abspath(model_path)
            self.model.save(model_path)
            print(f"Model saved successfully at: {model_path}")
        else:
            print("No model to save. Train the model first.")
