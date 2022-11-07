import re
import os
import sys

import pandas as pd
import numpy as np
import spacy

import unicodedata
from bs4 import BeautifulSoup
from spacy.lang.en.stop_words import STOP_WORDS as stopwords
from textblob import TextBlob

def _get_wordcounts(x):
	length=len(str(x).split())

	return length


def _get_charcounts(x):
	count=0
	for i in x:
		if i.isspace():
			count+=1

	return len(x)-count


def _get_avg_wordlength(x):
	count=_get_charcounts(x)/_get_wordcounts(x)

	return count


def _get_stopword_counts(x):
	count=0
	for token in x:
		if token in stopwords:
			count+=1

	return count


def _get_hashtag_counts(x):
	count=0
	for i in x.split():
		if i.startswith("#"):
			count+=1

	return count


def _get_mention_counts(x):
	count=0
	for i in x.split():
		if i.startswith("@"):
			count+=1

	return count


def _get_digit_counts(x):
	count=0
	for i in x.split():
		if i.isdigit():
			count+=1

	return count


def _get_uppercase_counts(x):
	count=0
	for i in x.split():
		if i.isupper():
			count+=1

	return count


def _get_cont_exp(x):

	contractions = { 

	"ain't": "am not",
	"aren't": "are not",
	"can't": "cannot",
	"can't've": "cannot have",
	"'cause": "because",
	"could've": "could have",
	"couldn't": "could not",
	"couldn't've": "could not have",
	"didn't": "did not",
	"doesn't": "does not",
	"don't": "do not",
	"hadn't": "had not",
	"hadn't've": "had not have",
	"hasn't": "has not",
	"haven't": "have not",
	"he'd": "he would",
	"he'd've": "he would have",
	"he'll": "he will",
	"he'll've": "he will have",
	"he's": "he is",
	"how'd": "how did",
	"how'd'y": "how do you",
	"how'll": "how will",
	"how's": "how is",
	"I'd": "I would",
	"I'd've": "I would have",
	"I'll": "I will",
	"I'll've": "I will have",
	"I'm": "I am",
	"I've": "I have",
	"isn't": "is not",
	"it'd": "it would",
	"it'd've": "it would have",
	"it'll": "it will",
	"it'll've": "it will have",
	"it's": "it is",
	"let's": "let us",
	"ma'am": "madam",
	"mayn't": "may not",
	"might've": "might have",
	"mightn't": "might not",
	"mightn't've": "might not have",
	"must've": "must have",
	"mustn't": "must not",
	"mustn't've": "must not have",
	"needn't": "need not",
	"needn't've": "need not have",
	"o'clock": "of the clock",
	"oughtn't": "ought not",
	"oughtn't've": "ought not have",
	"shan't": "shall not",
	"sha'n't": "shall not",
	"shan't've": "shall not have",
	"she'd": "she would",
	"she'd've": "she would have",
	"she'll": "she will",
	"she'll've": "she will have",
	"she's": "she is",
	"should've": "should have",
	"shouldn't": "should not",
	"shouldn't've": "should not have",
	"so've": "so have",
	"so's": "so as",
	"that'd": "that would",
	"that'd've": "that would have",
	"that's": "that is",
	"there'd": "there would",
	"there'd've": "there would have",
	"there's": "there is",
	"they'd": "they would",
	"they'd've": "they would have",
	"they'll": "they will",
	"they'll've": "they will have",
	"they're": "they are",
	"they've": "they have",
	"to've": "to have",
	"wasn't": "was not",
	"we'd": "we would",
	"we'd've": "we would have",
	"we'll": "we will",
	"we'll've": "we will have",
	"we're": "we are",
	"we've": "we have",
	"weren't": "were not",
	"what'll": "what will",
	"what'll've": "what will have",
	"what're": "what are",
	"what's": "what is",
	"what've": "what have",
	"when's": "when is",
	"when've": "when have",
	"where'd": "where did",
	"where's": "where is",
	"where've": "where have",
	"who'll": "who will",
	"who'll've": "who will have",
	"who's": "who is",
	"who've": "who have",
	"why's": "why is",
	"why've": "why have",
	"will've": "will have",
	"won't": "will not",
	"won't've": "will not have",
	"would've": "would have",
	"wouldn't": "would not",
	"wouldn't've": "would not have",
	"y'all": "you all",
	"y'all'd": "you all would",
	"y'all'd've": "you all would have",
	"y'all're": "you all are",
	"y'all've": "you all have",
	"you'd": "you would",
	"you'd've": "you would have",
	"you'll": "you will",
	"you'll've": "you will have",
	"you're": "you are",
	"you've": "you have",
	"dis":"this",
	"brng":"bring",
	"bak":"back",
	"dnt":"dont"
	}

	for key in contractions:
		val=contractions[key]
		x=x.replace(key,val)

	return x


def _get_emails(x):
	email=re.findall(r"([a-z0-9_\.\-]+[@][a-z]+[\.][a-z]+)",x)
	count=len(email)

	return count,email


def _remove_emails(x):
	return re.sub(r"([a-z0-9_\.\-]+[@][a-z]+[\.][a-z]+)","",x)


def _get_urls(x):
	url=re.findall(r"(http|https|ftp|ssh)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?",x)
	count=len(url)

	return count,url


def _remove_urls(x):
	return re.sub(r"(http|https|ftp|ssh)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?","",x)


def _remove_special_chars(x):
	x=re.sub(r"[^\w ]+","",x)
	x=" ".join(x.split())
	return x


def _remove_htmltags(x):
	return BeautifulSoup(x,"lxml").get_text().strip()


def _remove_accented_text(x):
	x=unicodedata.normalize("NFKD",x).encode("ascii","ignore").decode("utf-8","ignore").strip()
	return x


def _remove_stopwords(x):
	li=[]
	for i in x.split():
		if i not in stopwords:
			li.append(i)

	return " ".join(li)


def _convert_base(x):
	li=[]
	
	doc=nlp(x)
	for tok in doc:
		lemma=tok.lemma_
		if lemma=="-PRON-" or lemma=="be":
			lemma=tok.text
			
		li.append(lemma)
	
	return " ".join(li)


def _remove_common_words(x,n=20):
	text=x.split()
	freq_comm=pd.Series(text).value_counts()
	fn=freq_comm[:n]

	li=[]
	for i in x.split():
		if i not in fn:
			li.append(i)
	return " ".join(li)


def _remove_rare_words(x,n=20):
	text=x.split()
	freq_comm=pd.Series(text).value_counts()
	fn=freq_comm.tail(20)

	li=[]
	for i in x.split():
		if i not in fn:
			li.append(i)
	return " ".join(li)


def _spelling_correction(x):

	x=TextBlob(x).correct()
	return x
