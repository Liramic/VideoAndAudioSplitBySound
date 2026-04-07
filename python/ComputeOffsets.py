from pydub import AudioSegment
import os
import numpy as np
import librosa
import scipy.signal
import pyloudnorm

    # this function takes 2 audios, one short and one longer, and finds the
    # instances of the shorter inside the longer. minimalDistanceInSeconds
    # is the distance betweeen the nearest instances of the shorter audio.

def normalize_loudness(signal, fs, target_lufs=-16.0):
    # float in [-1, 1]
    if signal.dtype.kind in ("i", "u"):
        peak = np.iinfo(signal.dtype).max
        signal = signal.astype(np.float32) / peak
    else:
        signal = signal.astype(np.float32)

    meter = pyloudnorm.Meter(fs)
    in_loudness = meter.integrated_loudness(signal)
    # returns the normalized SIGNAL (not gain)
    signal_norm = pyloudnorm.normalize.loudness(signal, in_loudness, target_lufs)
    return signal_norm


def ComputeOffsets(intro_signal_file_name, longer_signal_file_name, minimal_distance_in_seconds, sensitivity):

    # Load the intro audio file
    intro_audio = AudioSegment.from_file(intro_signal_file_name)

    # Load the longer audio file
    longer_audio = AudioSegment.from_file(longer_signal_file_name)

    # Convert to mono
    if intro_audio.channels > 1:
        intro_audio = intro_audio.set_channels(1)
    if longer_audio.channels > 1:
        longer_audio = longer_audio.set_channels(1)

    # Resample to a common sampling rate if necessary
    common_fs = intro_audio.frame_rate
    if intro_audio.frame_rate != longer_audio.frame_rate:
        common_fs = min(intro_audio.frame_rate, longer_audio.frame_rate)
        intro_audio = intro_audio.set_frame_rate(common_fs)
        longer_audio = longer_audio.set_frame_rate(common_fs)

    # Convert to NumPy arrays
    intro_signal = np.array(intro_audio.get_array_of_samples())
    longer_signal = np.array(longer_audio.get_array_of_samples())

    
    # Normalize 
    longer_signal = normalize_loudness(longer_signal, common_fs)
    intro_signal = normalize_loudness(intro_signal, common_fs)

    #envelope both signal + reduce the a moving mean in the size of the
    #shorter signal - so only the shorter signal would yield a maximal cross corrolation
    # Envelope and moving mean reduction
    y1 = intro_signal
    y2 = longer_signal
    y2 = y2 - scipy.signal.convolve(y2, np.ones(len(y1))/len(y1), mode='same')
    #y1 = y1 - np.mean(y1)
    
    # Cross-correlation
    r = scipy.signal.correlate(y2, y1, mode='valid')

    #returning the peaks location in the array which are numel(y2) offseted with the
    #places where the shorter signal was found in the longer signal.
    # Find peaks
    min_peak_height = max(r) / sensitivity
    min_space_between_intros = minimal_distance_in_seconds * common_fs
    peaks, _ = scipy.signal.find_peaks(r, distance=min_space_between_intros, height=min_peak_height, prominence=0)

    # Convert peak locations to time offsets
    #offsets = (peaks - len(y2)) / (common_fs * 60)
    offsets = peaks / (common_fs * 60)

    return offsets