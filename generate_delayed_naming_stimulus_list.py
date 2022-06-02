from audioop import reverse
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

def generate_beeps(dir, prefix, min_delay, max_delay, beep_len, beep_f, nro_stimuli, repeats = 1):
    """
    Generate delayed beeps for naming experiments in AAA.
    Filenames will be [prefix]_[seed]_[running number].wav.

    Arguments are (where relevant in seconds): 
    prefix = filename prefix from user. 
    min = minimum length of wait i.e. silence in the beginning
    max = maximum length of wait i.e. silence in the beginning
    beep_len = lenght of the stimulus beep
    beep_f = frequency of the stimulus beep
    nro_stimuli = number of stimuli that need a beep
    repeats = number of times the stimuli are repeated
    """
    nro_beeps = nro_stimuli * repeats

    fs = 44100
    beep_len = int(round(beep_len*fs))
    min_len = int(round(min_delay*fs))
    max_len = int(round(max_delay*fs))
    audio_len = beep_len + max_len

    # wav is a 32 bit format, numpy uses by default 64.
    audio = np.zeros(audio_len, dtype=np.float32)
    audio[-beep_len:] = np.sin(np.multiply(2*np.pi*beep_f/fs, list(range(1,beep_len+1))))
    audio = audio.astype(np.float32)

    beep_names = []
    for i in range(nro_beeps):
        filename = "{prefix:s}-{i:03d}.wav".format(prefix = prefix, i = i+1)
        beep_names.append(filename)
        delay = int(np.random.uniform(min_len, max_len))
        sio_wavfile.write(dir/filename, fs, audio[-(delay+beep_len):])

    return beep_names


def generate_stimulus_list(output_dir, prefix, stimuli, calibration, beep_names, repeats = 1, half_way_break = False):

    n = len(stimuli)
	
    indeces = np.zeros((n, repeats))
    indeces[:,0] = np.random.permutation(n)
    i = 1
    while (i < repeats):
        indeces[:,i] = np.random.permutation(n)
        
        # If last token of previous block and the first token of this block 
        # would be the same, regenerate this block.
        if indeces[n,i-1] == indeces[1,i]:
            next
        i = i+1

    indeces = indeces.reshape(n*repeats)
    indeces = indeces.astype(int)
    tokens = [stimuli[i] for i in indeces]

    # Generate dot counters to indicate number of repeats and add them to the prompts.
    if repeats > 1:
        counters = []
        counter = ""
        for i in range(repeats):
            counter += "."
            counters.extend([counter]*n)
        # Flatten the counter list
        counters = [counter for repeat in counters for counter in repeat]

        tokens = [token + " " + counter for (token, counter) in zip(tokens, counters)]


    m = len(tokens)
    l = len(calibration)

    # Combine beep wav file names to a table with the tokens.
    tokens = [{'prompt': token, 'bmp': " ", 'wav': beep} for (token, beep) in zip(tokens, beep_names)]

    if half_way_break:
        # Generate calibration, counters and leave beeps out of the table.
        calibration = calibration * 4
        calibration_counters = []
        counter = ""
        for i in range(4):
            counter += "."
            calibration_counters.extend([counter]*l)
        calibration = [cal + " " + counter for (cal, counter) in zip(calibration, calibration_counters)]
        calibration = [{'prompt': cal, 'bmp': " ", 'wav': " "} for cal in calibration]

        # Note that the final calibrations happen in reverse order in case there are 
        # tasks like a tap test for synchrony that should be done without the participant.
        tokens = calibration[:l] + tokens[:int(m/2)] + list(reversed(calibration[l:2*l]))
        tokens += calibration[2*l:3*l] + tokens[int(m/2):] + list(reversed(calibration[3*l:]))
    else:
        # Generate calibration, counters and leave beeps out of the table.
        calibration = calibration * 2
        calibration_counters = []
        counter = ""
        for i in range(2):
            counter += "."
            calibration_counters.extend([counter]*l)
        calibration = [cal + " " + counter for (cal, counter) in zip(calibration, calibration_counters)]
        calibration = [{'prompt': cal, 'bmp': " ", 'wav': " "} for cal in calibration]

        # Note that the final calibration happens in reverse order in case there are 
        # tasks like a tap test for synchrony that should be done without the participant.
        tokens = calibration[:l] + tokens + list(reversed(calibration[l:]))

    filename = output_dir / (prefix + ".csv")
    with closing(open(filename, 'w', newline='\r\n')) as csvfile:
        line = "\"{prompt:s}\",\" \",\"{beep:s}\"\n"
        for token in tokens:
            csvfile.write(line.format(prompt = token['prompt'], beep = token['wav']))

    print("Wrote file " + str(filename) + ".")


def read_prompts(filename):
    with closing(open(filename, 'r', newline='')) as csv_file:
        reader = csv.reader(csv_file, quotechar = '"')
        prompts = [prompt[0] for prompt in reader]
        for prompt in prompts:
            if len(prompt.split("\t")) > 1:
                print("Input files should contain only one word per line.")
                print("Found instead this: {prompt}.", prompt = prompt) 
                sys.exit()
        return prompts


def main(args):
    repeats = 1
    if len(args) == 6:
        repeats = int(args.pop())
    prefix = args.pop()
    output_dir = Path(prefix)
    if not output_dir.exists():
        output_dir.mkdir()
    
    nro_participants = int(args.pop())
    calibration = read_prompts(args.pop())
    stimuli = read_prompts(args.pop())

    for id in range(1,nro_participants+1):
        participant_prefix = (prefix + '-' + str(id))
        participant_dir = output_dir / participant_prefix        
        if not participant_dir.exists():
            participant_dir.mkdir()

        # Setting the seed here makes the generated wait times and permutations reproducible.
        np.random.seed(id)

        beep_names = generate_beeps(participant_dir, participant_prefix, 1.2, 1.8, 0.05, 1000, len(stimuli), repeats)
        generate_stimulus_list(participant_dir, participant_prefix, stimuli, calibration, beep_names, repeats)


if (len(sys.argv) not in [5, 6]):
    print("\ngenerate_delayed_naming_stimulus_list.py")
    print("\tusage: python generate_delayed_naming_stimulus_list.py stimuli calibration numberOfParticipants prefix [repeats]")
    sys.exit(0)


if (__name__ == '__main__'):
    t = time.time()
    main(sys.argv[1:])
    print('Elapsed time: ' + str(time.time() - t))


