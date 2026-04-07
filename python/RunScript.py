import os
from ComputeOffsets import ComputeOffsets
import math
import pandas as pd
import numpy as np

if __name__ == "__main__":

    InputFolder = r"./" # folder that continas the video and the seperator sound
    sensitivity = 2 ; # higher sensitivy means more points in the results. usually 2-3 is a good choice.
    sepratorSound = "transition.mp3" # seperator sound name
    minimal_distance_between_sounds = 2
    #cd(InputFolder);

    files = dir(InputFolder)

    # the loop does the process for all videos in the input folder. you can
    # also do that to other filetypes besides mp4.
    # Loop through all files in the directory
    Offsets = pd.DataFrame() #The matrix that will be the CSV file
    for file in os.listdir(InputFolder):    
        if file.endswith("mp4"): #the file is not a folder and is an mp4 file
            currentOffsets = np.array(ComputeOffsets(os.path.join(InputFolder, sepratorSound), os.path.join(InputFolder,file), minimal_distance_between_sounds, sensitivity))
            currentOffsets = [currentOffsets, np.floor(currentOffsets), (currentOffsets - np.floor(currentOffsets)) * 60]

            # Assuming file.name contains the file name without extension
            output_file_name = os.path.join(InputFolder, file + '.csv')

            # Convert currentOffsets to a DataFrame and save to a CSV file
            df = pd.DataFrame(np.array(currentOffsets).T, columns=['float_offset', 'minutes', 'seconds'])
            df.to_csv(output_file_name, index=False)