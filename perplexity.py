from collections import Counter, defaultdict
import NGram
import smoothing
import math

def identify_unk(token, Unigram_count):
    if token not in Unigram_count:
        return "<UNKNOWN>"
    return token

def get_unigram_pp(words, Unigram_count):
    unigrams = [identify_unk(i, Unigram_count) for sub_list in words for i in sub_list]
    return unigrams

def get_bigram_pp(words, Unigram_count):
    paragraph_bigrams = []
    for section in words:
        paragraph_bigrams += [(identify_unk(section[idx], Unigram_count), identify_unk(section[idx+1], Unigram_count)) for idx in range(len(section)-1)]
    return paragraph_bigrams

def calc_perplexity(corp, n_gram, Unigram_count, Bigram_Dict, n = 2):
    # probs is the development corpora. N_gram is the dictionary for N-gram
    ans = 0;temp=0;
    if n==2:
        probs = get_bigram_pp(corp, Unigram_count)
    if n==1:
        probs = get_unigram_pp(corp, Unigram_count)
    for i in probs:
        temp = get_bigram_prob(i, n_gram, Bigram_Dict)
        ans = ans - math.log(temp)
    ans = ans/len(probs)
    ans = math.exp(ans)
    return ans

def get_bigram_prob(bigram, K_bigram, Bigram_Dict):
    if bigram in Bigram_Dict:
        return K_bigram[bigram]
    else:
        return K_bigram[(bigram[0], "<OTHERS>")]

def perplexity(train_file_path, test_file_path):
    Unigram_count, Bigram_Dict, K_unigram, K_bigram = smoothing.smoothing(train_file_path)
    Corp = NGram.corpora_preprocess(test_file_path)
    print calc_perplexity(Corp, K_bigram, Unigram_count, Bigram_Dict)

perplexity("train/obama.txt", "development/obama.txt")
perplexity("train/trump.txt", "development/trump.txt")
perplexity("train/trump.txt", "development/obama.txt")
perplexity("train/obama.txt", "development/trump.txt")
