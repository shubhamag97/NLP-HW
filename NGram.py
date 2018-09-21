from collections import Counter, defaultdict
import numpy as np

def corpora_preprocess(file_path):
    # Read data
    Fstream = open(file_path,'r')
    Speech = Fstream.read()
    Paragraphs = Speech.split('\n')
    #Paragraph_obama = ["the students like the assignment", "I see the students eating cake"]
    #Preprocess 1: Add <START> and <END> token for each paragraphs
    Word_Lists = [['<START>']+p.split()+['<END>'] for p in Paragraphs]
    for w_idx, paragraph in enumerate(Word_Lists):
        for idx in range(len(paragraph)):
            token = paragraph[idx]
            #Preprocess 2: take out single apostrophes by merging with words before/after
            if token == '\xe2\x80\x99':
                paragraph[idx] = paragraph[idx-1]+'\''+paragraph[idx+1]
                paragraph[idx-1] = ""
                paragraph[idx+1] = ""
            #Preprocess 2: take out apostrophes with trailing characters by merging with the word before
            if token in ['\'ve', '\'s', 'n\'t', '\'re']:
                paragraph[idx] = paragraph[idx-1]+paragraph[idx]
                paragraph[idx-1] = ""
            processed = [word for word in paragraph if len(word)>0]
            Word_Lists[w_idx] = processed
    return Word_Lists

# Count total # of tokens
def get_token_cnt(words):
	return sum(len(paragraph_words) for paragraph_words in words)

# Compute unigram probabilities
def unsmoothed_unigram(words):
	token_cnt = get_token_cnt(words)
	unigram_count = Counter([i for sub_list in words for i in sub_list])
	unigram = {k: v / float(token_cnt) for k, v in unigram_count.iteritems()}
	return unigram_count, unigram

# Compute bigram probabilities
def unsmoothed_bigram(words, unigram_count):
	bigram_count =  defaultdict(int)
	bigram_dict = defaultdict(set)
	for section in words:
	    paragraph_bigram_count = Counter([(section[idx], section[idx+1]) for idx in range(len(section)-1)])
	    for key, value in paragraph_bigram_count.items():
	        bigram_count[key] += value
	        bigram_dict[key[0]].add(key[1])
	bigram = {k: v / float(unigram_count[k[0]]) for k, v in bigram_count.iteritems()}
	return bigram_count, bigram_dict, bigram
