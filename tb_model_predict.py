import cv2
import numpy as np
from keras.models import load_model

class TuberculosisClassifierPredict:
    def __init__(self, model_path="model\\tuberculosis_model.h5"):
        self.model = load_model(model_path)

    def classify_image(self, image_path):
        img = cv2.imread(image_path, 0)
        if img is not None:
            resized_img = cv2.resize(img, (250, 250)) / 255.0
            input_data = resized_img.reshape(1, 250, 250, 1)
            prediction = self.model.predict(input_data)
            label = np.argmax(prediction)
            label_result = ''
            if int(label) == 0:
                label_result = 'TB_Detected'
            if int(label) == 1:
                label_result = 'TB_Not_Detected'
            probability_score = float(prediction[0][label])

            result = {"Label": label_result, "Probability": probability_score,"Actual": prediction}
            return result
        else:
            return {"error": "Invalid image path"}