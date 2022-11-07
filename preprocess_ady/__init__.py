from preprocess_ady import utils

__version__="0.0.1"


def get_wordcounts(x):
	return utils._get_wordcounts(x)


def get_charcounts(x):
	return utils._get_charcounts(x)


def get_avg_wordlength(x):
	return utils._get_avg_wordlength(x)


def get_stopword_counts(x):
	return utils._get_stopword_counts(x)


def get_hashtag_counts(x):
	return utils._get_hashtag_counts(x)


def get_mention_counts(x):
	return utils._get_mention_counts(x)


def get_digit_counts(x):
	return utils._get_digit_counts(x)


def get_uppercase_counts(x):
	return utils._get_uppercase_counts(x)


def get_cont_exp(x):
	return utils._get_cont_exp(x)


def get_emails(x):
	return utils._get_emails(x)


def remove_emails(x):
	return utils._remove_emails(x)


def get_urls(x):
	return utils._get_urls(x)


def remove_urls(x):
	return utils._remove_urls(x)