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
    
def tweet_dict(file):
    tweets = []
    for line in file:
        tweets.append(json.loads(line))
    return tweets

def assign_tweet_score(twt, scr):
	unicode_text = twt["text"]
	encoded_text = unicode_text.encode('utf-8')
	tweet_word = re.split('; |, |\*|\n|\\s|\.', encoded_text)
	sent_score = 0
	for j in range(len(tweet_word)):
		if tweet_word[j] in scr:
			sent_score = sent_score + scr[tweet_word[j]]
	return sent_score

def assign_state(twt):
	states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
	}
	place = twt["place"]
	if place != None:
		if twt["place"]["country"] == "United States" or twt["place"]["country_code"] == "US":
			full_name = twt["place"]["full_name"]
			encoded_full_name = full_name.encode('utf-8')
			split_full_name = re.split(', |', encoded_full_name)
			if split_full_name[1]  == 'USA':
				state_name = split_full_name[0]
				for k, v in states.iteritems():
					if v == state_name:
						state = k
						return state
			else : 
				state = split_full_name[1]
    			return state  


def assign_state_score (twt, scr):
	state_scores = {}
	for i in range(len(twt)):
		if u'text' in twt[i]:
			if u'place' in twt[i]:
				twt_state = assign_state(twt[i])
        		if twt_state != None:
        			twt_score = assign_tweet_score(twt[i], scr)
        			if twt_state in state_scores:
        				state_scores[twt_state] = state_scores[twt_state] + twt_score
        				#print twt_state, state_scores[twt_state]
        			else :
        				state_scores[twt_state] = twt_score
        				#print twt_state, state_scores[twt_state]
   	return state_scores



def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    #lines(sent_file)
   	#lines(tweet_file)
    score = sent_dict(sent_file)
    tweet = tweet_dict(tweet_file)
    state_sentiment = assign_state_score(tweet,score)
    happiest_state = max(state_sentiment, key = state_sentiment.get)
    print happiest_state

if __name__ == '__main__':
    main()
