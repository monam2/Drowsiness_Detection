import cv2
import uuid
import os
import time

list_path = ['G:\\','code','monitor', 'data', 'image_iot']
IMAGES_PATH = os.path.join(*list_path)
labels = ['data']
number_imgs = 100

cap = cv2.VideoCapture(0)

for label in labels:
    print('Collecting images for {}'.format(label))
    time.sleep(0.5)
    
    for img_num in range(number_imgs):
        print('Collecting images for {}, image number {}'.format(label, img_num))
        
        ret, frame = cap.read()
        
        imgname = os.path.join(IMAGES_PATH, label+'.'+str(uuid.uuid1())+'.jpg')

        cv2.imwrite(imgname, frame)
        cv2.imshow('Image Collection', frame)
        time.sleep(0.5)
        
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()

print(os.path.join(IMAGES_PATH, labels[0]+'.'+str(uuid.uuid1())+'.jpg'))

for label in labels:
    print('Collecting images for {}'.format(label))
    for img_num in range(number_imgs):
        print('Collecting images for {}, image number {}'.format(label, img_num))
        imgname = os.path.join(IMAGES_PATH, label+'.'+str(uuid.uuid1())+'.jpg')
        print(imgname)
