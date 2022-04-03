function offsets = ComputeOffsets(introSignalFileName, longerSignalFileName, minimalDistanceInSeconds)
    % this function takes 2 audios, one short and one longer, and finds the
    % instances of the shorter inside the longer. minimalDistanceInSeconds
    % - is the distance betweeen the nearest instances of the shorter
    % audio. a good rule of thumb is 

    [introSignal, fs] = audioread(introSignalFileName);
    [longerSignal, longerSignalFs] = audioread(longerSignalFileName);
    
    %convert to mono.
    if ( size(introSignal,2) > 1 )
        introSignal = sum(introSignal,2)/size(introSignal,2);
    end
    
    if ( size(longerSignal,2) > 1)
        longerSignal = sum(longerSignal,2)/size(longerSignal,2);
    end

    % format both signal to the same sampling rate
    commonFs = fs;
    if( fs ~= longerSignalFs)
        biggerFs = max(fs,longerSignalFs);
        commonFs = min(fs,longerSignalFs);
        [P,Q] = rat(commonFs/biggerFs);
        if ( biggerFs == longerSignalFs)
            longerSignal = resample(longerSignal, P, Q);
        else
            introSignal = resample(introSignal, P, Q);
        end
    end
    
    %normalize volume:
    longerSignal = NormalizeLoudness(longerSignal, commonFs);
    introSignal = NormalizeLoudness(introSignal, commonFs);

    %envelope both signal + reduce the a moving mean in the size of the
    %shorter signal - so only the shorter signal would yield a maximal
    %cross corrolation
    y1 = introSignal;   %envelope(introSignal);
    y2 = longerSignal;  %envelope(longerSignal);
    y2 = y2 - movmean(y2, numel(y1));
    y1 = y1 - mean(y1);
    r = xcorr(y2,y1);
    
    %returning the peaks location in the array which are numel(y2) offseted with the
    %places where the shorter signal was found in the longer signal.
    minimalPeakHeight = max(r)/3;
    minimialPeakProminaence = 0;%max(r);
    minSpaceBetweenIntros = minimalDistanceInSeconds*commonFs;

    %TODO - FIX FIND PEAKS parameters.

    [~,locs] = findpeaks(r,'MinPeakDistance',minSpaceBetweenIntros, 'MinPeakProminence',minimialPeakProminaence, ...
        'MinPeakHeight',minimalPeakHeight,'Threshold',1e-4);
    % if you want the seconds value you can remove dividing by 60.
    % use "format longG" command to get percise answers.
    offsets = (locs-numel(y2))/(commonFs*60);
    % this will print the number of instances found in the long signal.
    %numel(offsets)
    
    % sanity plot - you can comment that.
    %plot(r);

end