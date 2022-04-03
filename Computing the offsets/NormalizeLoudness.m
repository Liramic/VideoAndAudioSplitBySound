function normalizedSignal = NormalizeLoudness(signal,fs)
    % normalizes sound volume for signal
    [loudness, ~] = integratedLoudness(signal,fs);
    target = -23;
    gaindB = target - loudness;
    gain = 10^(gaindB/20);
    normalizedSignal = signal.*gain;
    %normalizedSignal = (normalizedSignal-min(normalizedSignal))/range(normalizedSignal)*2-1;
end

