

from __future__ import print_function
import utils
import numpy as np
import random
import sys
from keras.models import load_model
import argparse

"""
    Define global variables.
"""
SEQUENCE_LENGTH = 40
SEQUENCE_STEP = 3
PATH_TO_CORPUS = "corpus.txt"
EPOCHS = 25
DIVERSITY = 1.0

"""
    Read the corpus and get unique characters from the corpus.
"""
text = utils.read_corpus(PATH_TO_CORPUS)
chars = utils.extract_characters(text)

"""
    Create sequences that will be used as the input to the network.
    Create next_chars array that will serve as the labels during the training.
"""
sequences, next_chars = utils.create_sequences(text, SEQUENCE_LENGTH, SEQUENCE_STEP)
char_to_index, indices_char = utils.get_chars_index_dicts(chars)

"""
    The network is not able to work with characters and strings, we need to vectorise.
"""
X, y = utils.vectorize(sequences, SEQUENCE_LENGTH, chars, char_to_index, next_chars)

"""
    Define the structure of the model.
"""
model = utils.build_model(SEQUENCE_LENGTH, chars)


# model.fit(X, y, batch_size=128, nb_epoch=EPOCHS)

model = load_model("kmodel.h5") 

"""
    Pick a random sequence and make the network continue
"""

for diversity in [0.2, 0.5, 1.0, 1.2]:
    print()
    print('Diversity:', diversity)

    generated = ''
    
    sentence = "I will wash away your pain with my tears"

    sentence = sentence.lower()
    generated += sentence

    print('Generating with seed: "' + sentence + '"')
    sys.stdout.write(generated)

    for i in range(500):
        x = np.zeros((1, SEQUENCE_LENGTH, len(chars)))
        for t, char in enumerate(sentence):
            x[0, t, char_to_index[char]] = 1.

        predictions = model.predict(x, verbose=0)[0]
        next_index = utils.sample(predictions, diversity)
        next_char = indices_char[next_index]

        generated += next_char
        sentence = sentence[1:] + next_char

        sys.stdout.write(next_char)
        sys.stdout.flush()
    print()



