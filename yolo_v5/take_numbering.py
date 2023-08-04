import os
import uuid

file_path = 'D:/22.08.17code/monitor/data/images'
file_names = os.listdir(file_path)

count=0
for name in file_names:
    count+=1
    imgname = os.path.join(file_path, str(count) + '.'+ str((uuid.uuid1()))+'.jpg')
    src = os.path.join(file_path, name)
    dst = imgname
    dst = os.path.join(file_path, dst)
    os.rename(src, dst)



    
