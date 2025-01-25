import cv2
import numpy as np

#import image
img = cv2.imread('images/image2.png')
#get height and width for future use
height, width, channels = img.shape 

#increase contrast for terrible UW contrast schedule
lab= cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
#Split into channels
l_channel, a, b = cv2.split(lab)

clahe = cv2.createCLAHE(clipLimit=10.0, tileGridSize=(8,8))
#increase contrast of l channel
cl = clahe.apply(l_channel*10)
limg = cv2.merge((cl,a,b))
enhanced_img = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

#convert to grayscale
gray = cv2.cvtColor(enhanced_img, cv2.COLOR_BGR2GRAY)

#initial thresholding and morph 
gray2 = cv2.bitwise_not(gray)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU )[1] 
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (17,17))
morph = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

# cv2.imwrite("test_morph1.jpg", morph)
# cv2.imwrite("test_thresh1.jpg", thresh)

#adaptive thresholding for removal of horizontal lines as to find better bounding boxes
thresh = cv2.adaptiveThreshold(morph,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY_INV,81,17)
horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25,1))

remove_horizontal = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=3)
cnts = cv2.findContours(remove_horizontal, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
mask = np.zeros(morph.shape, np.uint8)
for c in cnts:
    cv2.drawContours(mask, [c], -1, (255,255,255),2)

morph = cv2.inpaint(morph, mask, 3, cv2.INPAINT_TELEA)
morph = cv2.erode(morph, kernel, iterations=1)

# creation of bounding boxes 
boundbox = []
boundbox_img = img.copy()
contours = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours = contours[0] if len(contours) == 2 else contours[1]


for cont in contours:
    x, y, w, h = cv2.boundingRect(cont)
    if (w < width / 3) and (w > width / 6.5):
        
        if x > 1:
            x = x - 5
            w = w + 10
        cv2.rectangle(boundbox_img, (x, 0), (x+w, height), (0, 0, 255), 1)
        boundbox.append([x, 0, w, height])


boundbox.sort(key=lambda x: x[0])

# cleaning up of duplicate days
remove = []
for i in range(1, len(boundbox)):
    if boundbox[i][0] == boundbox[i-1][0] or boundbox[i][0] - boundbox[i-1][0] < 10:
        remove.append(i)

for i in range(len(remove)-1, -1, -1):
    boundbox.pop(remove[i])

#saving of cropped images
i = 1
for bbox in boundbox:
    string = "scheduleImages/day" + str(i) + ".jpg"
    (x,y,w,h) = bbox
    if(w > 40):
        crop = img[y:y+h, x:x+w]
        cv2.imwrite(string, crop)
        i+=1

# cv2.imwrite("test_thresh.jpg", thresh)
# cv2.imwrite("test_gray.jpg", gray)
# cv2.imwrite("test_morph.jpg", morph)
# cv2.imwrite("test_boundbox.png", boundbox_img)
# cv2.waitKey(0)
