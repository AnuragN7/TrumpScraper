import itertools 
import nltk
import re
from nltk.corpus import stopwords
from urllib.request import urlopen
from bs4 import BeautifulSoup

SPEECH_URL = "https://www.washingtonpost.com/news/the-fix/wp/2016/08/19/donald-trumps-best-speech-of-the-2016-campaign-annotated/?utm_term=.27e983cc1748"


def get_sentence_list(url):
	""" Returns a list of all the sentences across Donald Trump's speech
		Args:
		url - url to be scraped """
		
	html = urlopen(url)
	bsObj = BeautifulSoup(html) # Convert the website into a beautiful soup object
	tag_list = bsObj.findAll("p", {"style": ""})
	text_list = [] # Will contain all the raw data
	for tag in tag_list:
		if len(tag.attrs) == 0: # We are trying to isolate the <p> tags
			text_list.append(nltk.sent_tokenize(tag.get_text()))
	return list(itertools.chain(*text_list)) # Just return a list of words

def filter_sentences(target_word, sentence_lst):
	""" Returns a list only containing the sentences that have the target word 
	
	    Args:
	    word: the word we are looking for
	    sentence_lst: a list of sentences """ 
	
	return [sent for sent in sentence_lst if target_word in sent] 

def get_associated_words(target_word):
	""" Returns a list of words preceeding our target word 
	    
	    Args:
	    sentence_lst: a list of sentences """
	sentence_lst = get_sentence_list(SPEECH_URL)
	filtered_sentences = filter_sentences(target_word, sentence_lst)
	word_lst = []
	for sent in filtered_sentences:
		word_lst.extend(nltk.word_tokenize(sent)) # Tokenize the sentences of interest into word lists
	bigram_lst = nltk.bigrams(word_lst)
	associated_word_lst = [] # Will hold all the words associated with the target word
	stop_words = set(stopwords.words("english"))
	for (a,b) in bigram_lst:
		if a == target_word and b not in stop_words and not re.match(r'\W+', b):
			associated_word_lst.append(b)
		elif b == target_word and a not in stop_words and not re.match(r'\W+', a):
			associated_word_lst.append(a)
	return associated_word_lst
	
 
	     
	   
    
		
