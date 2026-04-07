from moviepy.editor import * # pip install moviepy
import pydub # pip install pydub
import os


working_directory = r".";
# this folder should includ the SeperatorSound.mp3 file as well.

os.chdir(working_directory);

introSound = pydub.AudioSegment.from_file("IntroSound.mp3");
lenOfIntroSoundInSeconds = introSound.frame_count() / introSound.frame_rate; 

def convertToSeconds(timeInMins, shouldAddIntroLength=False):
    timeInSecs = timeInMins*60;
    if(shouldAddIntroLength):
        timeInSecs = timeInSecs + lenOfIntroSoundInSeconds;
    return timeInSecs

def readCsv(movieFileName):
    col = ([],[]);
    currentList = 0;
    csvFileName = movieFileName + ".csv";
    with open(csvFileName) as f:
        for row in f:
            col[currentList].append(row.split(',')[0])
            currentList = (currentList+1) % 2
    return col

movies = []

for file in os.listdir("."):
    if( file.endswith(".mp4")):
        movies.append(file)

for movie_name in movies:
    cuttingInstructions = readCsv(movie_name);
    clip = VideoFileClip(movie_name);
    numberOfSubclips = len(cuttingInstructions[0]);

    for i in range(0,numberOfSubclips):
        start = convertToSeconds(float(cuttingInstructions[0][i]), True);
        end = convertToSeconds(float(cuttingInstructions[1][i]));
        clipToSave = clip.subclip(start, end);
        clipToSave.write_videofile(movie_name[0:len(movie_name)-4] + "_" + str(i) + ".mp4");
