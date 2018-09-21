from collections import Counter, defaultdict
import numpy as np
import NGram

# Random Sentence Generation
def gen_unigram_sentence(unigram, seeding = ""):
    words = [w for w in unigram]
    prob = [unigram[w] for w in words]
    sentence = seeding.split()
    sentence.insert(0, '<START>')
    while True:
        alp = np.random.choice(words, 1, p=prob)
        if alp == '<START>':
            continue
        sentence.append(alp[0])
        if alp in ['<END>', '.', '?', '!']:
            break
    return ' '.join(sentence)

def gen_bigram_sentence(bigram_dict, bigram, seeding = ""):
    sentence = seeding.split()
    sentence.insert(0, '<START>')
    while sentence[-1] not in ['<END>', '.', '?', '!']:
        Next_Words = list(bigram_dict[sentence[-1]])
        Probs = [bigram[(sentence[-1], w)] for w in Next_Words]
        alp = np.random.choice(Next_Words, 1, p=Probs)
        sentence.append(alp[0])
    return ' '.join(sentence)

def Generate_Sentence(file_path):
    Words = NGram.corpora_preprocess(file_path)
    Unigram_count, Unigram = NGram.unsmoothed_unigram(Words)
    Bigram_count, Bigram_Dict, Bigram = NGram.unsmoothed_bigram(Words, Unigram_count)
    print gen_unigram_sentence(Unigram, seeding = "I Don't Care about")
    print gen_bigram_sentence(Bigram_Dict, Bigram, seeding = "I Don't Care about")

Generate_Sentence("../train/obama.txt")
