from moviepy.editor import * # pip install moviepy
import pydub # pip install pydub
import os
import pandas as pd


def convertToSeconds(timeInMins, shouldAddIntroLength=False):
    timeInSecs = timeInMins*60
    if(shouldAddIntroLength):
        timeInSecs = timeInSecs + lenOfIntroSoundInSeconds
    return timeInSecs

def readCsv(movieFileName):
    col = [[],[]]
    currentList = 0
    csvFileName = movieFileName + ".csv"
    with open(csvFileName) as f:
        for row in f:
            col[currentList].append(row.split(',')[0])
            currentList = (currentList+1) % 2
    col[0] = col[0][1:]
    #col[1] = col[1][1:]
    return col

if __name__ == "__main__":
    max_num_of_clips = 8
    working_directory = "Video3"
    # this folder should includ the SeperatorSound.mp3 file as well.
    os.chdir(working_directory)

    movies = []
    introSound = pydub.AudioSegment.from_file("IntroSound.mp3")
    lenOfIntroSoundInSeconds = introSound.frame_count() / introSound.frame_rate
    for file in os.listdir("."):
        if(file.endswith(".mp4")):
            movies.append(file)

    for movie_name in movies:
        cuttingInstructions = readCsv(movie_name)
        clip = VideoFileClip(movie_name)
        numberOfSubclips = len(cuttingInstructions[0])

        for i in range(0,max_num_of_clips):
            output_file_name = movie_name[0:len(movie_name)-4] + "_" + str(i) + ".mp3"
            #output_path = os.path.join("/final", "test.mp3")
            start = convertToSeconds(float(cuttingInstructions[1][i]), True)
            end = convertToSeconds(float(cuttingInstructions[0][i]))
            clipToSave = clip.subclip(start, end)
            audio_clip = clipToSave.audio

            audio_clip.write_audiofile(output_file_name)
