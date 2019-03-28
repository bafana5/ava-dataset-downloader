# author     : Meshack B. Shabalala (bafana5@gmail.com)
# date       : 21 February 2019
# description: Download the Google AVA Dataset directly from YouTube
import os
import sys
import json
import argparse
import youtube_dl
import pandas as pd

def read_data(filename):
    try:
        df = pd.read_csv(filename)
    except (OSError, IOError) as err:
        self.report_error('unable to read file ' + filename + error_to_compat_str(err))
        exit(1)

    data = df[df.columns[0]].values
    data = list(dict.fromkeys(data)) # remove duplicates 
    return data     

def dir_exists(path):
    try:
        dn = os.path.isdir(path)
        if not dn:
            os.mkdir(path)
            return True
        else:
            return True
    except (OSError, IOError) as err:
        self.report_error('unable to create directory ' + error_to_compat_str(err))
        return False

def download(datasetfile, savedir):
    data = read_data(datasetfile)
    missing_videos = []
    ydownloader_opts = {'outtmpl': savedir + '\%(id)s.%(ext)s'}
    ydownloader = youtube_dl.YoutubeDL(ydownloader_opts)
    for video in data:
        try:
            with ydownloader:
                ydownloader.download(['http://www.youtube.com/watch?v=' + video])
                # [ydownloader.download('https://s3.amazonaws.com/ava-dataset/trainval/' + video) for video in data]
        # except (OSError, IOError) as err:
        except:
            # self.report_error('This video is unavailable ' + video + error_to_compat_str(err))
            # print('This video is unavailable ' + video + str(IOError))
            missing_videos.append(video)
            continue
    file = os.path.join(savedir,'missing_videos.txt' )
    f = open(file, "a")
    f.write("================%s==============\n"%(savedir))
    for  i in missing_videos:
        f.write("%s\n"%(i))
    f.close()

#%%

def main():
    # Download 'train' or 'test' or 'val' dataset separately
    # e.g. ava-dataset-downloader.py --test
    parser = argparse.ArgumentParser(description='Download the Google AVA Video Dataset')
    if sys.argv[1] == '--test':
        if dir_exists('test'):
            filename = 'ava_dataset\\ava_test_v2.1.txt'
            download(filename, 'test')
        pass
    elif sys.argv[1] == '--train':
        if dir_exists('train'):
            filename = 'ava_train_v2.1.csv'
            download(filename, 'train')
    elif sys.argv[1] == '--val':
        if dir_exists('val'):
            filename = 'ava_val_v2.1.csv'
            download(filename, 'val')
#%%

if __name__ == '__main__':
    main()