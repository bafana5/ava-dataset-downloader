import os
from os.path import basename

# data manipulation
import numpy as np
import pandas as pd

ava_dataset_path       = "ava_dataset"
train_annotations_path = "annotations"


# Read annotaions and images
annotationsfile      = "ava_train_v2.1.csv"
annotationsfilepath  = os.path.join(ava_dataset_path, annotationsfile)
df = pd.read_csv(annotationsfilepath, delimiter=',')
data = df[df.columns[:]].values

# Collect the video paths
path = "train"
video_file_paths = []
videos_in_dir = os.listdir(path)
for index, file in enumerate(videos_in_dir):
    file_path = os.path.join(path, file)
    video_file_paths.append(file_path)

# video_names = df['video_id'].unique()
video_names = videos_in_dir

file = os.path.join(train_annotations_path,'train.txt' )


f = open(file, "a")

for video_name, video_path in zip(video_names, video_file_paths):
    df2 = df.loc[df.video_id == video_name[:-4], :] # remove .mp4
    video_timestamp = df2['middle_frame_timestamp'].unique()
    for timestep in video_timestamp:
        df3 = df2.loc[df2.middle_frame_timestamp == timestep, :]
        videodata = df3[df3.columns[:-1]].values
        
        
        cap = cv2.VideoCapture(video_path)
        # Check if camera opened successfully
        if (cap.isOpened()): 

    #         fps = cap.get(cv2.CAP_PROP_FPS)
    #         print("Frames per second using video.get(cv2.CAP_PROP_FPS): {:2.2f}".format(fps))
            # Read until video is completed
#             while(cap.isOpened()):
                # Capture frame-by-frame

            for indx, i in enumerate(videodata):
                if indx is 0:
                    sec = i[1]
                    w, h = (416, 416)
                    cap.set(cv2.CAP_PROP_FRAME_WIDTH, w)
                    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h)
                    cap.set(cv2.CAP_PROP_POS_MSEC, sec*1000)
                    success, image = cap.read()

                    if success:
                        # Read frame
                        imagename = 'trainimages' + "\\"  + video_name[:-4] + "_%06d.jpg"% sec
                        image = cv2.resize(image,(w, h),interpolation=cv2.INTER_AREA)
                        cv2.imwrite(imagename, image)     # save frame as JPEG file
                        # Press Q on keyboard to  exit
                        if cv2.waitKey(25) & 0xFF == ord('q'):
                            break
                    # Break the loop
                    else: 
                        break
                    f.write("%s %i,%i,%i,%i,%i"%(imagename,int(w*i[2]),int(w*i[3]),int(w*i[4]),int(w*i[5]),int(i[6])))
                else:
                    f.write(" %i,%i,%i,%i,%i"%(int(w*i[2]),int(w*i[3]),int(w*i[4]),int(w*i[5]),int(i[6])))  
            f.write("\n") 
            
            # When everything done, release the video capture object
            cap.release()
            # Closes all the frames
            cv2.destroyAllWindows()
        #     framename = val_arou_txt[:-20]+"_%06d.jpg"% labels[indx,0]
        #     f.write("%s,%.15f,%.15f\n"%(framename, labels[indx, 1], labels[indx, 2])) 
f.close()