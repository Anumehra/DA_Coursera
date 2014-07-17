import json
import sys
import re


#def lines(fp):
    #print str(len(fp.readlines()))

def sent_dict(file):
    scores = {} # initialize an empty dictionary
    for line in file:
        term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
        scores[term] = int(score)  # Convert the score to an integer.
    return scores
    # print scores.items() # Print every (term, score) pair in the dictionary

def tweet_dict(file):
    tweets = []
    for line in file:
        tweets.append(json.loads(line))
    return tweets

def assign_score(twt, scr):
	total_score = {}
	newterm = []
	for i in range(len(twt)):
		if u'text' in twt[i]:
			unicode_text = twt[i]["text"]
			encoded_text = unicode_text.encode('utf-8')
			tweet_word = re.split('; |, |\*|\n|\\s|\.', encoded_text)
			sent_score = 0
			for j in range(len(tweet_word)):
				if tweet_word[j] in scr:
					sent_score = sent_score + scr[tweet_word[j]]
				else:
					newterm.append(tweet_word[j])
			total_score[encoded_text] = int(sent_score)
	return total_score, newterm;

def score_newterm(term, twt_score):
	pos = 0
	neg = 0
	term_score = 0
	for i in sorted(twt_score.keys()):
		if term in i and twt_score[i] > 0:
				pos = pos + 1
		if term in i and twt_score[i] < 0:
				neg = neg + 1
	if pos < neg and pos != 0:
		term_score = -(neg/pos)
	if neg !=0 and pos == 0:
		term_score = -(neg)
	if pos > neg and neg !=0:
		term_score = pos/neg
	if pos !=0 and neg == 0:
		term_score = pos
	if pos == neg:
		term_score = 0
	return term_score



def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    #lines(sent_file)
   	#lines(tweet_file)
    score = sent_dict(sent_file)
    tweet = tweet_dict(tweet_file)
    tweet_score, new_terms = assign_score(tweet,score)
    for i in range(len(new_terms)):
    	newterm_sentiment = score_newterm(new_terms[i], tweet_score)
    	print new_terms[i], newterm_sentiment
    
    

if __name__ == '__main__':
    main()
