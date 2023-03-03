import os
import cv2
import numpy as np

# Define the path to the directory where the dataset will be stored
dataset_path = 'path/to/dataset'

# Define the list of labels for the sign language alphabet
labels = ['A', 'B', 'C']

# Define the size of the images to be captured and stored
img_size = (64, 64)

# Initialize the webcam and set the resolution
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Collect the dataset
for label in labels:
    label_path = os.path.join(dataset_path, label)
    if not os.path.exists(label_path):
        os.makedirs(label_path)
    print(f'Collecting images for label {label} ...')
    for i in range(100):
        ret, frame = cap.read()
        if ret:
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            img = cv2.resize(img, img_size)
            img_path = os.path.join(label_path, f'{i}.jpg')
            cv2.imwrite(img_path, img)
        cv2.imshow('Collecting dataset', img)
        if cv2.waitKey(1) == ord('q'):
            break

# Release the webcam and close the window
cap.release()
cv2.destroyAllWindows()

# Preprocess the dataset
X = []
y = []
for label in labels:
    label_path = os.path.join(dataset_path, label)
    for img_name in os.listdir(label_path):
        img_path = os.path.join(label_path, img_name)
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img, img_size)
        X.append(img)
        y.append(label)
X = np.array(X).reshape(-1, img_size[0], img_size[1], 1)
y = np.array(y)

# Save the preprocessed dataset as a NumPy binary file
np.savez('custom_sign_language_dataset.npz', X=X, y=y)
