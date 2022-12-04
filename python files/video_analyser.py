import time

from keras_preprocessing.image import load_img
from moviepy.editor import *
import os
from os.path import isfile, join
import cv2
import numpy as np
from tensorflow.keras.models import load_model

import categorize

def video_to_img_fun(filepath):
    filepath1 = 'C:\\Harshith\\python projects\\sentinalhack\\video_and_audio_files\\'
    print('deframming video')

    cam = cv2.VideoCapture(filepath+'.mp4')
    try:
        # creating a folder named data
        if not os.path.exists(filepath1+'data'):
            os.makedirs(filepath1+'data')

    # if not created then raise error
    except OSError:
        pass

    # frame
    currentframe = 0

    while True:
        # reading from frame
        ret, frame = cam.read()

        if ret:
            # if video is still left continue creating images
            name = filepath1+'data\\' + str(currentframe) + '.jpg'

            # writing the extracted images
            cv2.imwrite(name, frame)

            # increasing counter so that it will
            # show how many frames are created
            currentframe += 1
        else:
            break

    # Release all space and windows once done
    cam.release()
    cv2.destroyAllWindows()

def sl():
    time.sleep(15)

def fps_fun(filepath):
    print('calculating_fps')

    cap= cv2.VideoCapture(filepath+'.mp4')

    framespersecond= int(cap.get(cv2.CAP_PROP_FPS))

    return framespersecond

# print("The total number of frames in this video is ", framespersecond)

def convert_frames_to_video(filepath):
    print('stitching video frames')
    data_file_path = "C:\\Harshith\\python projects\\sentinalhack\\video_and_audio_files\\data\\"
    pathout = 'C:\\Harshith\\python projects\\sentinalhack\\video_and_audio_files\\stitched.mp4'

    fps = fps_fun(filepath)
    frame_array = []
    files = [f for f in os.listdir(data_file_path) if isfile(join(data_file_path, f))]

    # #for sorting the file names properly
    # files.sort(key = lambda x: int(x[5:-4]))

    for i in range(len(files)):
        filename=data_file_path + files[i]
        #reading each files
        img = cv2.imread(filename)
        height, width, layers = np.shape(img)
        size = (width,height)
        # print(filename)
        #inserting the frames into an image array
        frame_array.append(img)

    out = cv2.VideoWriter(pathout,cv2.VideoWriter_fourcc(*'mp4v'), fps, size)

    for i in range(len(frame_array)):
        # writing to a image array
        out.write(frame_array[i])
    out.release()

    for i in os.listdir(data_file_path):
        os.remove(data_file_path+i)


def merger(filepath):
    print('merging audio with video')
    stitched_file_path = 'C:\\Harshith\\python projects\\sentinalhack\\video_and_audio_files\\'
    output_path = 'C:\\Harshith\\python projects\\sentinalhack\\result_files\\'
    clip = VideoFileClip(stitched_file_path+'stitched.mp4')

    audioclip = AudioFileClip(output_path + "result_audio.mp3")

    videoclip = clip.set_audio(audioclip)

    videoclip.write_videofile(output_path + 'results.mp4')
    return 0


# def blank_img_fun(img_name):
#
#     from PIL import Image as im
#     img = cv2.imread(img_name)
#     # img = np.zeros([100,100,3],dtype=np.uint8)
#     # img.fill(0) # or img[:] = 255
#     img1 = np.ones([240, 320, 3], dtype=np.uint8)
#
#     # out =  np.concatenate((img, img1), axis = 0)
#     out = np.multiply(img, img1)
#
#     data = im.fromarray(out)
#     data.save(img_name)

def video_analyse_fun(filepath):
    print('starting video analysis')
    category = categorize.validate(filepath)
    fileName = filepath +'.mp4'

    # '''output file writing'''
    #
    # f = open(file_path0+'\\front-end\\load.txt', "w+")
    # f.write('true')
    # f.close()

    '''video to image'''
    video_to_img_fun(filepath)


    if category == 'notblok':
        '''cnn model'''
        '''model integration and prediction'''
        try:
            classify_number = 0

            model = load_model('imgclassifier.h5')

            data_file_path = "C:\\Harshith\\python projects\\sentinalhack\\video_and_audio_files\\data"

            files = os.listdir(data_file_path)

            for img in files:
                img = load_img(img, target_size=(200, 200,3))
                img = np.array(img)
                predict = model.predict(img)

                if predict[0] == 'notnormal':
                    classify_number+=1
                elif predict[0] == 'violence':
                    classify_number+=1
                elif classify_number == 10:
                    category = 'block'

        except:
            pass

    elif category == 'notblock':
        sl()
        '''image to video'''
        convert_frames_to_video(filepath)

        '''video and audio merge'''
        merger(filepath)
        os.remove('C:\\Harshith\\python projects\\sentinalhack\\video_and_audio_files\\stitched.mp4')

        return category

    else :
        '''image to video'''
        sl()
        convert_frames_to_video(filepath)

        '''video and audio merge'''
        merger(filepath)
        os.remove('C:\\Harshith\\python projects\\sentinalhack\\video_and_audio_files\\stitched.mp4')
        os.remove('C:\\Harshith\\python projects\\sentinalhack\\result_files\\results.mp4')

        return category


    # f1 = open(file_path0 + '\\front-end\\load.txt' + "", "w+")
    # f1.write('success')
    # f1.close()
    # os.remove(file_path + "\\audio.wav")
    # os.remove(file_path + "\\stitched.mp4")
    # return classify_number
    # # exit()

    # '''output file writing'''

    # f = open(file_path0+'\\front-end\\load.txt' + "", "w+")
    # f.write('success')
    # f.close()



