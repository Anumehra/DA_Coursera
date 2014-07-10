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
	for i in range(len(twt)):
		if u'text' in twt[i]:
			unicode_text = twt[i]["text"]
			encoded_text = unicode_text.encode('utf-8')
			tweet_word = re.split('; |, |\*|\n|\\s|\.', encoded_text)
			sent_score = 0
			for j in range(len(tweet_word)):
				if tweet_word[j] in scr:
					sent_score = sent_score + scr[tweet_word[j]]
			print sent_score


def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    #lines(sent_file)
   	#lines(tweet_file)
    score = sent_dict(sent_file)
    tweet = tweet_dict(tweet_file)
    assign_score(tweet,score)

if __name__ == '__main__':
    main()
