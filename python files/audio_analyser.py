import os

import numpy as np
from scipy.io.wavfile import write

from better_profanity import profanity

import wave
import contextlib

import moviepy.editor
from pydub import AudioSegment

def video_to_audio(filepath):
    fileName = filepath + '.mp4'
    video = moviepy.editor.VideoFileClip(fileName)
    audio = video.audio
    audio.write_audiofile(filepath + ".mp3")

def mp3_to_wav(filepath):
    # print(1)
    fileName = filepath + '.mp3'
    AudioSegment.from_mp3(fileName).export(filepath + '.wav', format="wav")


def wav_to_mp3(filepath):
    fileName_wav = filepath + '.wav'
    output_path = 'C:\\Harshith\\python projects\\sentinalhack\\result_files\\result_audio.mp3'
    AudioSegment.from_wav(fileName_wav).export(output_path , format="mp3")
    # os.remove(filepath+'.wav')


def audio_analysis(filepath):
    fileName_mp3 = filepath + '.mp3'
    fileName_srt = filepath + '.srt'
    fileName_wav = filepath + '.wav'

    '''mp3 to wav conversion for further use'''
    mp3_to_wav(filepath)

    N_C_W_index = []
    # not common word index

    first_time_hr = []
    first_time_min = []
    first_time_sec = []
    first_time_millisec = []

    second_time_hr = []
    second_time_min = []
    second_time_sec = []
    second_time_millisec = []

    time_difference = []

    '''reading srt file and analysing with profanity filter'''

    with open(fileName_srt, "r") as myFile:
        text_string = myFile.read()
    filtered_string = profanity.censor(text_string)

    # print(text_string)
    # print(filtered_string)

    f = open(filepath + "filtered.srt", "w+")
    f.write(filtered_string)
    f.close()

    '''converting text file to array of new and old srt file'''

    fileObj = open(fileName_srt, "r")
    old_srt_array = fileObj.read().splitlines()
    fileObj.close()
    print(old_srt_array)

    fileObj1 = open(filepath + 'filtered.srt', "r")
    new_srt_array = fileObj1.read().splitlines()
    fileObj1.close()
    print(new_srt_array)
    # print(new_srt_array[10][-1:])

    '''comparing both the arrays'''

    for a in range(0, len(old_srt_array)):
        if new_srt_array[a] == old_srt_array[a]:
            pass
        else:
            try:
                int(old_srt_array[a - 1][-1:])
                N_C_W_index.append(old_srt_array[a - 1])
                # print(N_C_W_index)
            except:
                N_C_W_index.append(old_srt_array[a - 2])

    '''time difference'''

    for b in range(0, len(N_C_W_index)):
        # print(N_C_W_index[b][0:2])
        first_time_hr.append(int(N_C_W_index[b][0:2]))
        first_time_min.append(int(N_C_W_index[b][3:5]))
        first_time_sec.append(int(N_C_W_index[b][6:8]))
        first_time_millisec.append(int(N_C_W_index[b][9:12]))

        second_time_hr.append(int(N_C_W_index[b][17:19]))
        second_time_min.append(int(N_C_W_index[b][20:22]))
        second_time_sec.append(int(N_C_W_index[b][23:25]))
        second_time_millisec.append(int(N_C_W_index[b][26:]))

        difference = ((second_time_hr[b] * 3600000) + (second_time_min[b] * 60000) + (second_time_sec[b] * 1000) +
                      second_time_millisec[b]) - \
                     ((first_time_hr[b] * 3600000) + (first_time_min[b] * 60000) + (first_time_sec[b] * 1000) +
                      first_time_millisec[b])
        time_difference.append(difference)

    print(time_difference)


    '''length of audio grabbing '''

    with contextlib.closing(wave.open(fileName_wav, 'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
    duration = frames / float(rate)
        # print(duration)

    '''beep sound generator'''

    for c in range(0, len(N_C_W_index)):
        sps = 44100
        freq_hz = 987.77
        beep_duration = time_difference[c] / 1000
        vol = 1

        esm = np.arange(beep_duration * sps)
        wf = np.sin(2 * np.pi * esm * freq_hz / sps)
        wf_quiet = wf * vol
        wf_int = np.int16(wf_quiet * 32767)
        write(filepath + "2.wav", sps, wf_int)

        '''audio file trimming'''

        t1 = 0  # Works in milliseconds
        t2 = (first_time_hr[0] * 3600000) + (first_time_min[0] * 60000) + (first_time_sec[0] * 1000) + \
             first_time_millisec[0]
        newAudio = AudioSegment.from_wav(fileName_wav)
        newAudio = newAudio[t1:t2]
        newAudio.export(filepath + '1.wav', format="wav")

        t1 = ((second_time_hr[0] * 3600000) + (second_time_min[0] * 60000) + (second_time_sec[0] * 1000) +
              second_time_millisec[0])  # Works in milliseconds
        t2 = duration * 1000
        newAudio = AudioSegment.from_wav(fileName_wav)
        newAudio = newAudio[t1:t2]
        newAudio.export(filepath + '3.wav', format="wav")

        '''audio files joining'''

        infiles = [filepath + "1.wav", filepath + "2.wav", filepath + "3.wav"]
        outfile = fileName_wav

        data = []

        for infile in infiles:
            w = wave.open(infile, 'rb')
            data.append([w.getparams(), w.readframes(w.getnframes())])
            w.close()

        output = wave.open(outfile, 'wb')
        output.setparams(data[0][0])
        for i in range(len(data)):
            output.writeframes(data[i][1])
        output.close()


    '''wav to mp3 conversion'''
    wav_to_mp3(filepath)

    '''removing unwanted files'''
    os.remove(fileName_wav)
    os.remove(filepath + 'filtered.srt')
    os.remove(filepath + '1.wav')
    os.remove(filepath + '2.wav')
    os.remove(filepath + '3.wav')



    # os.remove("C:\\Users\\harsh\\Downloads" + '\\format.txt')
    #
    # f1 = open(file_path0 + '\\front-end\\load.txt' + "", "w+")
    # f1.write('success')
    # f1.close()