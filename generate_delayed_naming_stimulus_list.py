from contextlib import closing
import csv
from fileinput import filename
import glob
import os
from pathlib import Path
import random
import sys
import time

import numpy as np

# wav file handling
import scipy.io.wavfile as sio_wavfile

def generate_beeps(prefix, min, max, beep_len, beep_f, nro_beeps, seed, repeats = 1):
    """
    Generate delayed beeps for naming experiments in AAA.
    Filenames will be [prefix]_[seed]_[running number].wav.

    Arguments are (where relevant in seconds): 
    prefix = filename prefix from user. 
    min = minimum length of wait i.e. silence in the beginning
    max = maximum length of wait i.e. silence in the beginning
    beep_len = lenght of the stimulus beep
    beep_f = frequency of the stimulus beep
    nro_beeps = number of randomised beep files to generate
    seed = random number seed for the generator, must be a non-negative
      integer. If a negative number is given as the seed, it will not be
      used. This feature can be used to generate consecutive batches of
      pseudorandom beeps without resetting the seed between batches.
    """
    if repeats != 1:
        raise ValueError("Having more than one repeat not yet implemented. repeats = " + str(repeats))

    fs = 44100
    beep_len = np.floor(round(beep_len*fs))
    min_len = np.floor(round(min*fs))
    max_len = np.floor(round(max*fs))
    audio_len = beep_len + max_len

    audio = np.zeros(audio_len)
    audio[-beep_len+1:] = np.sin(np.multiply(2*np.pi*beep_f/fs, list(range(1,beep_len+1))))
    
    if seed >= 0:
        random.seed(seed)

    beep_names = []
    for i in range(nro_beeps):
        filename = "{prefix:s}_{id:d}_{i:03d}.wav".format(prefix = prefix, id = seed, i = i)
        beep_names.append(filename)
        delay = random.uniform(min_len, max_len)
        sio_wavfile.write(filename, fs, audio[delay:])

    return beep_names


def write_results(table, filename):
    # Finally dump all the metadata into a csv-formated file to
    # be read by Python or R.
    with closing(open(filename, 'w')) as csvfile:
        fieldnames = ['id', 'speaker', 'sliceBegin', 'beep', 'begin', 'end', 'word']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames,
                                quoting=csv.QUOTE_NONNUMERIC)

        writer.writeheader()
        map(writer.writerow, table)

    print("Wrote file " + filename + " for R/Python.")


def generate_stimulus_list(output_dir, stimuli, calibration, id, beep_names, repeats = 1, half_way_break = False):

    if repeats != 1:
        raise ValueError("Having more than one repeat not yet tested. repeats = " + str(repeats))

    n = len(stimuli)
	
    indeces = matrix(, nrow=n, ncol=repeats)
    indeces[,1] = sample.int(n)
    i = 2
    while (i <= repeats){
        indeces[,i] = sample.int(n)
        
        # If last token of previous block and the first token of this block 
        # would be the same, regenerate this block.
        if (indeces[n,i-1] == indeces[1,i]){
            next
        }
        i = i+1
    }
    indeces = as.vector(indeces)
    tokens = stimuli[indeces]

    counters = []
    counter = ""
    for i in range(repeats):
        counter += "."
        counters.append(counter)

    # Generate dot counters to indicate number of repeats and add the to the stimulus stimuli.
    counters = as.vector(matrix(c(".","..","..."), nrow=n, ncol=repeats, byrow=T))
    tokens = apply(data.frame(tokens, counters), 1, paste, collapse=" ") 

    m = len(tokens)
    l = len(calibration)

    # Generate beep wav-file names and combine them to a table with the tokens.
    # Beep files are [prefix]_[seed]_[running number].wav.
    beeps = apply(data.frame(file_prefix, sprintf("_%03d", 1:(m)), ".wav"), 1, paste, collapse="")
    tokens = cbind(prompt = tokens, bmp = " ", wav = beeps)

    if half_way_break:
        # Generate calibration, counters and leave beeps out of the table.
        calibration_counters = c(".","..","...", "....")
        calibration = apply(expand.grid(calibration, calibration_counters), 1, paste, collapse = " ")
        calibration = cbind(prompt = calibration, bmp = " ", wav = "")

        tokens = c(
            calibration[1:l], tokens[1:(m/2)], calibration[(l+1):(2*l)],
            calibration[(2*l+1):(3*l)], tokens[(m/2+1):(m)], calibration[(3*l+1):(4*l)]
        )
    else:
        # Generate calibration, counters and leave beeps out of the table.
        calibration_counters = c(".","..")
        calibration = apply(expand.grid(calibration, calibration_counters), 1, paste, collapse = " ")
        calibration = cbind(prompt = calibration, bmp = " ", wav = "")

        tokens = c(calibration[1:l], tokens, calibration[(l+1):(2*l)])

    with closing(open(filename, 'w')) as csvfile:
        fieldnames = ['token', 'bmp', 'beep']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames,
                                quoting=csv.QUOTE_NONNUMERIC)

        writer.writeheader()
        map(writer.writerow, tokens)

    print("Wrote file " + filename + ".")


def read_recording_names(filename):
    with closing(open(filename, 'r')) as file:
        return [line.rstrip() for line in file]


def main(args):
    prefix = args.pop()
    output_dir = Path(prefix)
    if not output_dir.exists():
        output_dir.mkdir()
    
    nro_participants = args.pop()
    calibration = read_recording_names(args.pop())
    stimuli = read_recording_names(args.pop())

    for id in range(1,nro_participants+1):
        participant_prefix = (prefix + '_' + str(id))
        participant_dir = output_dir / participant_prefix        
        if not participant_dir:
            participant_dir.mkdir()
        beep_names = generate_beeps(participant_dir, participant_prefix, 1.2, 1.8, 0.05, 1000, len(stimuli), id)
        generate_stimulus_list(participant_dir, participant_prefix, stimuli, calibration, id, beep_names)


if (len(sys.argv) not in [3,4]):
    print("\ngenerate_delayed_naming_stimulus_list.py")
    print("\tusage: python generate_delayed_naming_stimulus_list.py stimuli calibration numberOfParticipants prefix")
    sys.exit(0)


if (__name__ == '__main__'):
    t = time.time()
    main(sys.argv[1:])
    print('Elapsed time: ' + str(time.time() - t))


