from collections import Counter, defaultdict
from sets import Set
import numpy as np

Stop_words = Set(['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"])

def corpora_preprocess(file_path):
    # Read data
    Fstream = open(file_path,'r')
    Speech = Fstream.read()
    #Speech = "<START> the students liked the assignment <END>"
    Paragraphs = Speech.split('\n')
    # Paragraphs = ["the students like the assignment", "I see the students eating cake"]
    Word_Lists = [['<START>']+p.split()+['<END>'] for p in Paragraphs]
    for w_idx, paragraph in enumerate(Word_Lists):
        for idx in range(len(paragraph)):
            token = paragraph[idx]
            if token == '\xe2\x80\x99':
                paragraph[idx] = paragraph[idx-1]+'\''+paragraph[idx+1]
                paragraph[idx-1] = ""
                paragraph[idx+1] = ""
            if token in ['\'ve', '\'s', 'n\'t', '\'re']:
                paragraph[idx] = paragraph[idx-1]+paragraph[idx]
                paragraph[idx-1] = ""
            #Words_obama[idx] = [word for word in paragraph if len(word)>0]
            processed = [word for word in paragraph if len(word)>0]
            #processed = [word for word in processed if not word in Stop_words] 
            Word_Lists[w_idx] = processed
    return Word_Lists

Words_obama = corpora_preprocess("train/trump.txt")

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
