from collections import Counter, defaultdict
from sets import Set
import NGram

Unknown_threshold = 1
ADD_K = 0.0001

def get_unknown_words(Unigram_count, unknown_threshold = Unknown_threshold):
	return Set([word for word in Unigram_count if Unigram_count[word]<=unknown_threshold])

def convert_unk_threshold(Word_Lists, Unknown_words):
    for w_idx, paragraph in enumerate(Word_Lists):
        for idx in range(len(paragraph)):
            token = paragraph[idx]
            paragraph[idx] = identify_unk_threshold(token, Unknown_words)
    return Word_Lists

def identify_unk_threshold(token, Unknown_words):
    if token in Unknown_words:
        return "<UNKNOWN>"
    return token

def get_k_unigram(add_k, unigram_count, token_cnt):
	k_unigrams = {k: (v + add_k) / float(token_cnt + len(unigram_count) * add_k) for k, v in unigram_count.iteritems()}
	return k_unigrams

def get_k_bigram(add_k, unigram_count, bigram_count):
	k_bigram = {k: (v + add_k) / float(unigram_count[k[0]] + len(unigram_count) * add_k) for k, v in bigram_count.iteritems()}

	all_words = unigram_count.keys()
	for word in all_words:
		if word != "<END>":
			bigram = (word, "<OTHERS>")
			k_bigram[bigram] = add_k / float(unigram_count[word] + len(unigram_count) * add_k)
	return k_bigram

def smoothing(file_path, add_k = ADD_K, unknown_threshold = Unknown_threshold):
	Words = NGram.corpora_preprocess(file_path)
	Unigram_count, Unigram = NGram.unsmoothed_unigram(Words)
	Unknown_words = get_unknown_words(Unigram_count, unknown_threshold)
	Words = convert_unk_threshold(Words, Unknown_words)
	# print Unigram_count

	Token_cnt = NGram.get_token_cnt(Words)
	Unigram_count, Unigram = NGram.unsmoothed_unigram(Words)
	Bigram_count, Bigram_Dict, Bigram = NGram.unsmoothed_bigram(Words, Unigram_count)
	# print Unigram_count
	# print Bigram_count
	# print "# of Unigram: " + str(len(Unigram_count))
	K_unigram = get_k_unigram(add_k, Unigram_count, Token_cnt)
	K_bigram = get_k_bigram(add_k, Unigram_count, Bigram_count)
	# print K_unigram
	# print K_bigram
	return Unigram_count, Bigram_Dict, K_unigram, K_bigram
