# # import cv2
# # from pytesseract import image_to_string
# # import numpy as np

# # def getText(filename):
# #     img = cv2.imread(filename)
# #     HSV_img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
# #     h,s,v = cv2.split(HSV_img)
# #     v = cv2.GaussianBlur(v, (1,1), 0)
# #     thresh = cv2.threshold(v, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
# #     cv2.imwrite('{}.png'.format(filename),thresh)
# #     kernel = cv2.getStructuringElement(cv2.MORPH_RECT, ksize=(1, 2))
# #     thresh = cv2.dilate(thresh, kernel)
# #     txt = image_to_string(thresh, config="--psm 6 digits")
# #     return txt
    

# # text = getText('frame100.jpg')
# # print(text)
# # # text = getText('np2.png')
# # # print(text)

# import cv2
# import pytesseract
# import numpy as np

# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# cascade= cv2.CascadeClassifier("haarcascade_russian_plate_number.xml")
# states={"AN":"Andaman and Nicobar","AP":"Andhra Pradesh","AR":"Arunachal Pradesh","AS":"Assam","BR":"Bihar","CH":"Chandigarh","DN":"Dadra and Nagar Haveli","DD":"Daman and Diu","DL":"Delhi","GA":"Goa","GJ":"Gujarat",
# "HR":"Haryana","HP":"Himachal Pradesh","JK":"Jammu and Kashmir","KA":"Karnataka","KL":"Kerala","LD":"Lakshadweep","MP":"Madhya Pradesh","MH":"Maharashtra","MN":"Manipur","ML":"Meghalaya","MZ":"Mizoram","NL":"Nagaland","OD":"Odissa","PY":"Pondicherry","PN":"Punjab","RJ":"Rajasthan","SK":"Sikkim","TN":"TamilNadu","TR":"Tripura","UP":"Uttar Pradesh", "WB":"West Bengal","CG":"Chhattisgarh","TS":"Telangana","JH":"Jharkhand","UK":"Uttarakhand"}

# def extract_num(img_name):
#     img = cv2.imread(img_name) ## Reading Image
#     # Converting into Gray
#     gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) 
#     # Detecting plate
#     nplate = cascade.detectMultiScale(gray,1.1,4)
#     for (x,y,w,h) in nplate:
#         # Crop a portion of plate
#         a,b = (int(0.02*img.shape[0]), int(0.025*img.shape[1]))
#         plate = img[y+a:y+h-a, x+b:x+w-b, :]
#         # make image more darker to identify the LPR
#         ## iMAGE PROCESSING
#         kernel = np.ones((1, 1), np.uint8)
#         plate = cv2.dilate(plate, kernel, iterations=1)
#         plate = cv2.erode(plate, kernel, iterations=1)
#         plate_gray = cv2.cvtColor(plate,cv2.COLOR_BGR2GRAY)
#         (thresh, plate) = cv2.threshold(plate_gray, 127, 255, cv2.THRESH_BINARY)
#         # Feed Image to OCR engine
#         read = pytesseract.image_to_string(plate)
#         read = ''.join(e for e in read if e.isalnum())
#         print(read)
#         stat = read[0:2]
#         try:
#         # Fetch the State information
#             print('Car Belongs to',states[stat])
#         except:
#             print('State not recognised!!')
#         print(read)
#         cv2.rectangle(img, (x,y), (x+w, y+h), (51,51,255), 2)
#         cv2.rectangle(img, (x, y - 40), (x + w, y),(51,51,255) , -1)
#         cv2.putText(img,read, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
#         cv2.imshow('PLate',plate)
#         # Save & display result image
#         cv2.imwrite('plate.jpg', plate)

#     cv2.imshow("Result", img)
#     cv2.imwrite('result.jpg',img)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()

# # Let's make a function call
# extract_num('/home/scarlett/Samarth/data/frame230.jpg')

from pytesseract import image_to_string 
from PIL import Image # pip install Pillow
print (image_to_string(Image.open('/home/scarlett/Samarth/data/frame230.jpg')))