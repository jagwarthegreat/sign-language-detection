import cv2
import numpy as np
from keras.models import load_model
from skimage.transform import resize, pyramid_reduce
import PIL
from PIL import Image

model = load_model('CNNmodel.h5')
cam_capture = cv2.VideoCapture(0)

colors = []
for i in range(0,20):
    colors.append((245,117,16))


window_name = "Sign Language Detection using CNN Algorithmn"
def prediction(pred):
    return(chr(pred+ 65))


def keras_predict(model, image):
    data = np.asarray( image, dtype="int32" )
    
    pred_probab = model.predict(data)[0]
    pred_class = list(pred_probab).index(max(pred_probab))
    return max(pred_probab), pred_class

def keras_process_image(img):
    
    image_x = 28
    image_y = 28
    img = cv2.resize(img, (1,28,28), interpolation = cv2.INTER_AREA)
  
    return img
 

def crop_image(image, x, y, width, height):
    # return image[y:y + height, x:x + width]
    return image[40:400,0:300]

def main():
    l = []
    
    while True:
        _, image_frame = cam_capture.read()  
    # Select ROI
        im2 = crop_image(image_frame, 300,300,300,300)

        image_frame=cv2.rectangle(image_frame,(0,40),(300,400),255,2)

        image_grayscale = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)
    
        image_grayscale_blurred = cv2.GaussianBlur(image_grayscale, (15,15), 0)
        im3 = cv2.resize(image_grayscale_blurred, (28,28), interpolation = cv2.INTER_AREA)
    
        im4 = np.resize(im3, (28, 28, 1))
        im5 = np.expand_dims(im4, axis=0)
    

        pred_probab, pred_class = keras_predict(model, im5)
    
        curr = prediction(pred_class)

        print(pred_probab,curr)

        #cv2.putText(image_frame, curr, (100, 300), cv2.FONT_HERSHEY_COMPLEX, 4.0, (255, 255, 255), lineType=cv2.LINE_AA)
 
    # Display cropped image

        cv2.rectangle(image_frame, (0,0), (300, 40), (245, 117, 16), -1)
        cv2.putText(image_frame,"Output: - "+' '.join(curr), (3,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        #cv2.rectangle(image_frame, (300, 300), (600, 600), (255, 255, 00), 3)
        cv2.imshow(window_name, frame)
        cv2.setWindowProperty(window_name,cv2.WND_PROP_TOPMOST,1)
        
        
    #cv2.imshow("Image4",resized_img)
        # cv2.imshow("Image3",image_grayscale_blurred)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

main()

cam_capture.release()
cv2.destroyAllWindows()