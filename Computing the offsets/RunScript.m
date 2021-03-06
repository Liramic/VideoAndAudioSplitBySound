InputFolder = "."; % folder that continas the video and the seperator sound
sensitivity = 3; % higher sensitivy means more points in the results. usually 2-3 is a good choice.
sepratorSound = "IntroSound.mp3"; % seperator sound name
%cd(InputFolder);


files = dir(InputFolder);

% the loop does the process for all videos in the input folder. you can
% also do that to other filetypes besides mp4.
for i = 1:numel(files)
    file = files(i);
    if file.isdir == 0 && endsWith(file.name, "mp4")
        currentOffsets = ComputeOffsets(fullfile(InputFolder, sepratorSound), fullfile(InputFolder,file.name), 6, sensitivity);
        currentOffsets = [ currentOffsets, floor(currentOffsets), (currentOffsets-floor(currentOffsets))*60 ];
        writematrix(currentOffsets ,fullfile(InputFolder,file.name) +  '.csv') 
    end
end