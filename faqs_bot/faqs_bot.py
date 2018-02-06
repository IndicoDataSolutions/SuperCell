import math
import os
import tqdm
from random import sample
import cPickle as pickle

from scipy.spatial.distance import cdist
import json
import numpy as np
import indicoio
from texttable import Texttable
indicoio.config.api_key = "YOUR_API_KEY_HERE"

'''
Use indico's Text Features API to find text similarity and create a customer support bot that automatically responds to FAQs from users.
Tutorial: https://indico.io/blog/faqs-bot-text-features-api/
'''

faqs = {
    'Where can I find my API Key?':'Hi there! You receive an API key upon sign up. After you confirm your email you will be able to log in to your dashboard at indico.io/dashboard and see your API key on the top of the screen.',
    'Can indico be downloaded as a package and used offline?':'Unfortunately, no. However we do have a paid option for on premise deployment for enterprise clients.',
    'What is indico API credit?':'Hello! indico API credit is what we use to keep track of usage. If you send in 100 bits of text into our API you are charged 100 credits, essentially one credit is consumed per datapoint analyzed. Every user gets 10,000 free API credits per month.',
    'Would I be able to set up a Pay as You Go account and have it stop if I reach 10,000 calls so that I won\'t be charged if I accidentally go over the limit?':'Hi there! Yep, the best way for you to do this would be to sign up for a pay as you go account and don\'t put in a credit card (we don\'t require you to). When you hit 10,000 you will be locked out of your account and unable to make more calls until you put a credit card in or you can wait until the first of the month when it resets to 10,000.',
    'Hello! When I try to install indico with pip, I get this error on Windows. Do you know why?':'Hello, please try following the steps listed here: https://indico.io/blog/getting-started-indico-tutorial-for-beginning-programmers/#windows and let us know if you still continue to have problems.'
}

def make_feats(data):
    """
    Send our text data throught the indico API and return each text example's text vector representation
    """
    # TODO

def calculate_distances(feats):
    # cosine distance is the most reasonable metric for comparison of these 300d vectors
    distances = cdist(feats, feats, 'cosine')
    return distances

def similarity_text(idx, distance_matrix, data, n_similar=5):
    """
    idx: the index of the text we're looking for similar questions to
         (data[idx] corresponds to the actual text we care about)
    distance_matrix: an m by n matrix that stores the distance between
                     document m and document n at distance_matrix[m][n]
    data: a flat list of text data
    """
    t = Texttable()
    t.set_cols_width([50, 20])

    # these are the indexes of the texts that are most similar to the text at data[idx]
    # note that this list of 10 elements contains the index of text that we're comparing things to at idx 0
    sorted_distance_idxs = np.argsort(distance_matrix[idx])[:n_similar] # EX: [252, 102, 239, ...]
    # this is the index of the text that is most similar to the query (index 0)
    most_sim_idx = sorted_distance_idxs[1]

    # header for texttable
    t.add_rows([['Text', 'Similarity']])
    print t.draw()

    # set the variable that will hold our matching FAQ
    faq_match = None

    for similar_idx in sorted_distance_idxs:
        # actual text data for display
        datum = data[similar_idx]

        # distance in cosine space from our text example to the similar text example
        distance = distance_matrix[idx][similar_idx]

        # how similar that text data is to our input example
        similarity =  1 - distance

        # add the text + the floating point similarity value to our Texttable() object for display
        t.add_rows([[datum, str(round(similarity, 2))]])
        print t.draw()

        # set a confidence threshold
        # TODO

    # print the appropriate answer to the FAQ, or bring in a human to respond
    # TODO

def input_question(data, feats):
    # TODO

def run():
    # TODO


if __name__ == "__main__":
    run()
