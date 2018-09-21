from collections import Counter, defaultdict
import NGram

ADD_K = 0.2

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

def smoothing(file_path, add_k = ADD_K):
	Words = NGram.corpora_preprocess(file_path)
	Token_cnt = NGram.get_token_cnt(Words)
	Unigram_count, Unigram = NGram.unsmoothed_unigram(Words)
	Bigram_count, Bigram_Dict, Bigram = NGram.unsmoothed_bigram(Words, Unigram_count)
	Unigram_count["<UNKNOWN>"] = 0;
	K_unigram = get_k_unigram(add_k, Unigram_count, Token_cnt)
	K_bigram = get_k_bigram(add_k, Unigram_count, Bigram_count)
	return Unigram_count, Bigram_Dict, K_unigram, K_bigram

#smoothing("train/obama.txt")
