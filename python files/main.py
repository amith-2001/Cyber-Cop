import os
import audio_analyser
import video_analyser

def analyse(file):


    filepath = file['path']
    print(filepath)
    original_filepath = filepath[:-4]
    if filepath[-4:] == ".mp3":
        audio_analyser.audio_analysis(original_filepath)
        return 0

    else:
        try:
            audio_analyser.video_to_audio(original_filepath)
            audio_analyser.audio_analysis(original_filepath)
        except:
            pass
        category = video_analyser.video_analyse_fun(original_filepath)

        print(category)
        return category
