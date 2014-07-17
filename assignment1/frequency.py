import json
import sys
import re



def tweet_dict(file):
    tweets = []
    for line in file:
        tweets.append(json.loads(line))
    return tweets

def allterms(twt):
	allterms = []
	for i in range(len(twt)):
		if u'text' in twt[i]:
			unicode_text = twt[i]["text"]
			encoded_text = unicode_text.encode('utf-8')
			tweet_word = re.split('; |, |\*|\n|\\s|\.|\!|\/|\?', encoded_text)
			
			for j in range(len(tweet_word)):
				if tweet_word[j] in ['','RT','-'] or tweet_word[j].startswith("http"):
					continue	
				else:
					allterms.append(tweet_word[j])
	return allterms

	
def	getUniqueTerms(terms):
	uniqueterms = []
	for i in range(len(terms)):
		if not terms[i] in uniqueterms:
			uniqueterms.append(terms[i])
	return uniqueterms

def getTermFrequency(unique, all):
	count = 0
	allterms_count = float(len(all))
	for i in range(len(all)):
		if all[i] == unique:
			count = float(count + 1)
	term_frequency = float(count/allterms_count)
	return term_frequency



def main():
    tweet_file = open(sys.argv[1])
    tweet = tweet_dict(tweet_file)
    #allterms_count = len(allterms)
    all_terms = allterms(tweet)
    unique_terms = getUniqueTerms(all_terms)
    for i in range(len(unique_terms)):
    	frequency = getTermFrequency(unique_terms[i], all_terms)
    	print unique_terms[i], frequency
    




if __name__ == '__main__':
    main()
