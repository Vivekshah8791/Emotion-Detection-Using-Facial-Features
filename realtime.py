import cv2
import numpy as np
from keras.models import model_from_json


with open("emotiondetector.json", "r") as json_file:
    model_json = json_file.read()
model = model_from_json(model_json)

model.load_weights("emotiondetector.h5")

haar_file = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(haar_file)

labels = {
    0: 'angry',
    1: 'disgust',
    2: 'fear',
    3: 'happy',
    4: 'neutral',
    5: 'sad',
    6: 'surprise'
}

def extract_features(image):
    """
    Takes a grayscale image of a face and returns
    a normalized numpy array ready for prediction.
    """
    feature = np.array(image)
    feature = feature.reshape(1, 48, 48, 1) 
    return feature / 255.0  

webcam = cv2.VideoCapture(0)

while True:
    ret, frame = webcam.read()
    if not ret:
        print("Failed to grab frame")
        break

    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    for (x, y, w, h) in faces:
        
        face_img = gray[y:y+h, x:x+w]
        face_img = cv2.resize(face_img, (48,48))

        img = extract_features(face_img)
        pred = model.predict(img)
        prediction_label = labels[pred.argmax()]

        cv2.rectangle(frame, (x, y), (x+w, y+h), (255,0,0), 2)
        cv2.putText(frame, prediction_label, (x-10, y-10),
                    cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (0,0,255), 1, cv2.LINE_AA)

    cv2.imshow("Emotion Detector", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

webcam.release()
cv2.destroyAllWindows()
