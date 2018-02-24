import cv2
import numpy as np
from tensorflow.contrib import predictor

WIDTH = 28
HEIGHT= 28

image = cv2.imread("/Users/bartowski/tmp/data/wxjump/test/1519373760_652.png")
grey_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
resized_image = cv2.resize(grey_image, (28, 28))

for m in range(0, len(resized_image)):
    for n in range(0, len(resized_image[m])):
        resized_image[m][n] = resized_image[m][n] / 255.0

resized_image = np.array(resized_image).flatten()
print(resized_image.shape)

predict_fn = predictor.from_saved_model("./model/1519411350")
predictions = predict_fn(
    {"x": resized_image})
print(predictions)
