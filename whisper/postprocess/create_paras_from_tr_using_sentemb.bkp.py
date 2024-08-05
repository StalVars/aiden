#!/bin/python

import sys
import re
import os

# First let import the most necessary libs
import pandas as pd
import numpy as np
# Library to import pre-trained model for sentence embeddings
from sentence_transformers import SentenceTransformer
# Calculate similarities between sentences
from sklearn.metrics.pairwise import cosine_similarity
# Visualization library
import seaborn as sns
import matplotlib.pyplot as plt
# package for finding local minimas
from scipy.signal import argrelextrema
import math

def rev_sigmoid(x:float)->float:
    return (1 / (1 + math.exp(0.5*x)))

def activate_similarities(similarities:np.array, p_size=10)->np.array:
        """ Function returns list of weighted sums of activated sentence similarities
        Args:
            similarities (numpy array): it should square matrix where each sentence corresponds to another with cosine similarity
            p_size (int): number of sentences are used to calculate weighted sum
        Returns:
            list: list of weighted sums
        """
        # To create weights for sigmoid function we first have to create space. P_size will determine number of sentences used and the size of weights vector.
        x = np.linspace(-10,10,p_size)
        # Then we need to apply activation function to the created space
        y = np.vectorize(rev_sigmoid)
        # Because we only apply activation to p_size number of sentences we have to add zeros to neglect the effect of every additional sentence and to match the length ofvector we will multiply
        activation_weights = np.pad(y(x),(0,similarities.shape[0]-p_size))
        ### 1. Take each diagonal to the right of the main diagonal
        diagonals = [similarities.diagonal(each) for each in range(0,similarities.shape[0])]
        ### 2. Pad each diagonal by zeros at the end. Because each diagonal is different length we should pad it with zeros at the end
        diagonals = [np.pad(each, (0,similarities.shape[0]-len(each))) for each in diagonals]
        ### 3. Stack those diagonals into new matrix
        diagonals = np.stack(diagonals)
        ### 4. Apply activation weights to each row. Multiply similarities with our activation.
        diagonals = diagonals * activation_weights.reshape(-1,1)
        ### 5. Calculate the weighted sum of activated similarities
        activated_similarities = np.sum(diagonals, axis=0)
        return activated_similarities

sentences=[]
stamps=[]
ti=0
with open(sys.argv[1],"r") as f:
    for line in f:
        line=line.strip()
        fields=line.split("\t")
        sentences.append(fields[0])
        stamps.append((float(fields[1]),float(fields[2])))
        ti+=1
        #if ti % 5 == 0:
        #    sentences.append("\n")
        #    stamps.append(())


# Embeddings
model = SentenceTransformer('all-mpnet-base-v2')
embeddings = model.encode(sentences)

#Similarities
similarities = cosine_similarity(embeddings)


# Split algorithm based on cosine similarities

# Lets apply our function. For long sentences i reccomend to use 10 or more sentences
activated_similarities = activate_similarities(similarities, p_size=5)

### 6. Find relative minima of our vector. For all local minimas and save them to variable with argrelextrema function
minmimas = argrelextrema(activated_similarities, np.less, order=2) #order par




base=os.path.basename(sys.argv[1])
tfile="data/_inparas/"+base
tf=open(tfile,"w")

#Get the order number of the sentences which are in splitting points
split_points = [each for each in minmimas[0]]
# Create empty string
text = ''
start=0
end=1
for num,each in enumerate(sentences):

    # Check if sentence is a minima (splitting point)

    if num in split_points:
        # If it is then add a dot to the end of the sentence and a paragraph before it.
        text+=f'\n {each}. '
        start = stamps[num][0]
    else:
        # If it is a normal sentence just add a dot to the end and keep adding sentences.
        text+=f'{each}. '
        end = stamps[num][1]



tf.write(text+"\n")
tf.close()

    
