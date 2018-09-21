from collections import Counter, defaultdict
import NGram
import smoothing
from perplexity import identify_unk as check_unk
from perplexity import get_bigram_prob as b_prob
import math

# FilePath: "../test/test.txt"

'''
Helper Functions:
perplexity.identify_unk(str, set_of_words_in_dictionary):
    Check whether a given word is <UNKNOWN>
perplexity.get_bigram_prob(tuple, Bigram, set_of_words_in_bigram):
    Check bigram probability, if not exist, use default value of add-k smoothing
'''

def Predict_Prob(Paragraph, Uni_dict, Bi_dict, Bigram):
    '''
    Input a paragraph, return log probability calculated on given Bigram
    '''
    # Split A speech into list of bigram tuples
    Tups = [(check_unk(Paragraph[idx], Uni_dict), check_unk(Paragraph[idx+1], Uni_dict)) for idx in range(len(Paragraph)-1)]
    # Obtain Bigram probability for each bigram tuples
    Probs = [math.log(b_prob(Tup, Bigram, Bi_dict)) for Tup in Tups]
    # Instead of multiplying, we calculate summation of log values to prevent floating point issues
    return sum(Probs)

def Predict_Ngram(Inpath = "../test/test.txt", Outpath = "../Output/t1.csv", Train_Trump = "../train/trump.txt", Train_Obama = "../train/obama.txt"):
    '''
    Input:
        Inpath  : file path for test data
        Outpath : file path for output csv file
        Train_Trump : file path to train Trump's bigram model
        Train_Obama : file path to train Obama's bigram model
    Output:
        Return None, Output should go straight to .csv file
    '''
    f = open(Outpath, 'w')
    f.write('Id,Prediction\n')

    #Preprocess the test set
    Paragraphs = NGram.corpora_preprocess(Inpath)

    #Generate Bigrams for Obama and Trump Speech
    Dictionary_Obama, Bigram_Dict_Obama, _, Bigram_Obama = smoothing.smoothing(Train_Obama)
    Dictionary_Trump, Bigram_Dict_Trump, _, Bigram_Trump = smoothing.smoothing(Train_Trump)

    #Iterate through test cases, decide whose speech it is
    for idx, paragraph in enumerate(Paragraphs):
        Trump_prob = Predict_Prob(paragraph, Dictionary_Trump, Bigram_Dict_Trump, Bigram_Trump)
        Obama_prob = Predict_Prob(paragraph, Dictionary_Obama, Bigram_Dict_Obama, Bigram_Obama)
        f.write(str(idx)+',')
        if Trump_prob >= Obama_prob:
            f.write('1')
        else:
            f.write('0')
        f.write('\n')

Predict_Ngram()
