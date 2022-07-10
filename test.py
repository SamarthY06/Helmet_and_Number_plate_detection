import cv2
from cv2 import imread
import numpy as np
import os
import imutils
from tensorflow import keras
from keras.models import load_model
from os import path
from PIL import Image
import PIL




directory = r'/home/scarlett/Samarth/Images'
os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'

net = cv2.dnn.readNet("yolov3-custom_7000.weights", "yolov3-custom.cfg")
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)


model = load_model('helmet-nonhelmet_cnn.h5')
print('model loaded!!!')

cap = cv2.VideoCapture('/home/scarlett/Samarth/video.mp4')
COLORS = [(0,255,0),(0,0,255)]

layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
 

fourcc = cv2.VideoWriter_fourcc(*"XVID")
writer = cv2.VideoWriter('video_output.avi', fourcc, 5,(888,500))



def helmet_or_nohelmet(helmet_roi):
	try:
		helmet_roi = cv2.resize(helmet_roi, (224, 224))
		helmet_roi = np.array(helmet_roi,dtype='float32')
		helmet_roi = helmet_roi.reshape(1, 224, 224, 3)
		helmet_roi = helmet_roi/255.0
		return int(model.predict(helmet_roi)[0][0])
	except:
			pass

ret = True

while ret:

    ret, img = cap.read()
    img = imutils.resize(img,height=500)
    # img = cv2.imread('test.png')
    height, width = img.shape[:2]

    blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

    net.setInput(blob)
    outs = net.forward(output_layers)

    confidences = []
    boxes = []
    classIds = []

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.3:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)

                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                classIds.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    
    # directory = r'D:\PATH'
    c=1
    for i in range(len(boxes)):
        if i in indexes:
            x,y,w,h = boxes[i]
            color = [int(c) for c in COLORS[classIds[i]]]
            # green --> bike
            # red --> number plate
            if classIds[i]==0: #bike
                helmet_roi = img[max(0,y):max(0,y)+max(0,h)//4,max(0,x):max(0,x)+max(0,w)]
            else: #number plate
                x_h = x-60
                y_h = y-350
                w_h = w+100
                h_h = h+100
                cv2.rectangle(img, (x, y), (x + w, y + h), color, 7)
                # h_r = img[max(0,(y-330)):max(0,(y-330 + h+100)) , max(0,(x-80)):max(0,(x-80 + w+130))]
                if y_h>0 and x_h>0:
                    h_r = img[y_h:y_h+h_h , x_h:x_h +w_h]
                    c = helmet_or_nohelmet(h_r)
                    cv2.putText(img,['helmet','no-helmet'][c],(x,y-100),cv2.FONT_HERSHEY_SIMPLEX,2,(0,255,0),2)                
                    cv2.rectangle(img, (x_h, y_h), (x_h + w_h, y_h + h_h),(255,0,0), 10)
                    c+=i
                    #cropped_image = img[y_h:y_h+h_h, x_h:x_h+w_h]
                    cropped_image = img[y:y+h, x:x+w]
                    # print(cropped_image)
                    # image = cv2.imread('test3.png')
                    # print(image)
                    # img_plate = cv2.imread(cropped_image)
                    os.chdir(directory) 
                    print("Before saving")   
                    print(os.listdir(directory))   
                    filename = 'plate' + f'{c}' + '.jpg'
                    cv2.imwrite(filename, cropped_image) 
                    print("After saving")  
                    print(os.listdir(directory))
                    # print(cropped_image)
                    # picture = Image.open(cropped_image)  
                    # picture = picture.save("dolls" +"c"+ ".jpg") 
# cropped_image = img[Y:Y+H, X:X+W]
# print([X,Y,W,H])
# plt.imshow(cropped_image)
# cv2.imwrite('contour1.png', cropped_image)
    
# for filename in os.listdir(directory):
#     if filename.endswith(".jpg"):
#         im = Image.open(filename)
#         name='img'+str(c)+'.png'
#         rgb_im = im.convert('RGB')
#         rgb_im.save(name)
#         c+=1
#         print(os.path.join(directory, filename))
#         continue
#     else:
#         continue
    writer.write(img)
    cv2.imshow("Image", img)
    
    if cv2.waitKey(1) == 27:
        break

writer.release()
cap.release()
cv2.waitKey(0)
cv2.destroyAllWindows()