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

def perplexity(train_file_path, test_file_path):
    Unigram_count, Bigram_Dict, K_unigram, K_bigram = smoothing.smoothing(train_file_path)
    Corp = convert_unk(NGram.corpora_preprocess(test_file_path), Unigram_count)
    print train_file_path + " " + test_file_path + ": " + str(calc_perplexity(Corp, K_bigram, Unigram_count, Bigram_Dict))

#perplexity("train/obama.txt", "development/obama.txt")
#perplexity("train/obama.txt", "development/trump.txt")
#perplexity("train/trump.txt", "development/trump.txt")
#perplexity("train/trump.txt", "development/obama.txt")
