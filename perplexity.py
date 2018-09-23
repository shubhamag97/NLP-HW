from collections import Counter, defaultdict
import NGram
import smoothing
import math

def convert_unk(Word_Lists, Unigram_count):
    for w_idx, paragraph in enumerate(Word_Lists):
        for idx in range(len(paragraph)):
            token = paragraph[idx]
            paragraph[idx] = identify_unk(token, Unigram_count)
    return Word_Lists

def identify_unk(token, Unigram_count):
    if token not in Unigram_count:
        return "<UNKNOWN>"
    return token

def get_unigram_pp(words):
    unigrams = [i for sub_list in words for i in sub_list]
    return unigrams

def get_bigram_pp(words):
    paragraph_bigrams = []
    for section in words:
        paragraph_bigrams += [(section[idx], section[idx+1]) for idx in range(len(section)-1)]
    return paragraph_bigrams

def calc_perplexity(corp, n_gram, Unigram_count, Bigram_Dict, n = 2):
    # probs is the development corpora. N_gram is the dictionary for N-gram
    ans = 0;temp=0;
    if n==2:
        probs = get_bigram_pp(corp)
    if n==1:
        probs = get_unigram_pp(corp)
    for i in probs:
        temp = get_bigram_prob(i, n_gram, Bigram_Dict)
        ans = ans - math.log(temp)
    ans = ans/len(probs)
    ans = math.exp(ans)
    return ans

def get_bigram_prob(bigram, K_bigram, Bigram_Dict):
    if bigram[1] in Bigram_Dict[bigram[0]]:
        return K_bigram[bigram]
    else:
        return K_bigram[(bigram[0], "<OTHERS>")]

def perplexity(train_file_path, test_file_path, k, threshold):
    Unigram_count, Bigram_Dict, K_unigram, K_bigram = smoothing.smoothing(train_file_path, k, threshold)
    Corp = convert_unk(NGram.corpora_preprocess(test_file_path), Unigram_count)
    perp = calc_perplexity(Corp, K_bigram, Unigram_count, Bigram_Dict)
    print train_file_path + " " + test_file_path + ": " + str(perp)
    return perp


def Perplexity_Validation(Outpath = "../Output/perplexity.csv"):
    k_range = [0.000001, 0.00001, 0.0001, 0.001, 0.01, 0.1]
    threshold_range = [x for x in range(1, 6)]

    f = open(Outpath, 'w')
    f.write('k,threshold,obama_obama,obama_trump,trump_trump,trump_obama\n')

    for k in k_range:
        for threshold in threshold_range:

            print k
            print threshold

            f.write(str(k) + ',')
            f.write(str(threshold) + ',')

            perp_oo = perplexity("../train/obama.txt", "../development/obama.txt", k, threshold)
            perp_ot = perplexity("../train/obama.txt", "../development/trump.txt", k, threshold)
            perp_tt = perplexity("../train/trump.txt", "../development/trump.txt", k, threshold)
            perp_to = perplexity("../train/trump.txt", "../development/obama.txt", k, threshold)           
            
            f.write(str(perp_oo) + ',')
            f.write(str(perp_ot) + ',')
            f.write(str(perp_tt) + ',')
            f.write(str(perp_to) + '\n')


# Perplexity_Validation()