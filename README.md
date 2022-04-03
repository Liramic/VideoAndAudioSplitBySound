# VideoAndAudioSplitBySound
Splitting audio or video by finding a specific sound instances

There are currently two stages to the process - 
First   -   Get the instances of the shorter sound with matlab.
            outputs a CSV file.
Second  -   the python code assumes that each part in the video,
            starts and ends with the shorter sound, and it cuts the video
            into parts when each odd line K in the CSV is the start of the part,
            and line K+1 is the end of that part.

