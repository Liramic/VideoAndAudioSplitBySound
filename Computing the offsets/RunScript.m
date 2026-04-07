InputFolder = "C:\Liron\DataEmg\ForYael"; % folder that continas the video and the seperator sound
sensitivity = 2; % higher sensitivy means more points in the results. usually 2-3 is a good choice.
minimalDistanceBetweenSounds = 0.1; %should be a good estimate  for good results
sepratorSound = "IntroSound.mp3"; % seperator sound name
%cd(InputFolder);

currentFolder = pwd;

files = dir(InputFolder);

% the loop does the process for all videos in the input folder. you can
% also do that to other filetypes besides mp4.
for i = 1:numel(files)
    file = files(i);
    if file.isdir == 0 && endsWith(file.name, "mp4")
        currentOffsets = ComputeOffsets(fullfile(currentFolder, sepratorSound), fullfile(InputFolder,file.name), minimalDistanceBetweenSounds, sensitivity);
        currentOffsets = [ currentOffsets, floor(currentOffsets), (currentOffsets-floor(currentOffsets))*60 ];
        writematrix(currentOffsets ,fullfile(InputFolder,file.name) +  '.csv') 
    end
end