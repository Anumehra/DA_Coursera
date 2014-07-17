import json
import sys
import re
from heapq import nlargest
from operator import itemgetter

#def lines(fp):
    #print str(len(fp.readlines()))



def tweet_dict(file):
    tweets = []
    for line in file:
        tweets.append(json.loads(line))
    return tweets

def all_hashtags(twt):
    encoded_hashtag_text = []
    for i in range(len(twt)):
        if u'entities' in twt[i]:
            entities = twt[i]["entities"]
            if entities != None:
                if u'hashtags' in entities:
                    hashtags = entities["hashtags"]
                    if hashtags != None:
                        for j in range(len(hashtags)):
                            if u'text' in hashtags[j]:
                                hashtag_text = hashtags[j]["text"]
                                encoded_hashtag_text.append(hashtag_text.encode('utf-8'))
    return encoded_hashtag_text


def calc_hashtag_frequency(twt):
    hash_freq = {}
    all_hash = all_hashtags(twt)
    for i in range(len(all_hash)):
        if all_hash[i] in hash_freq:
            hash_freq[all_hash[i]] = hash_freq[all_hash[i]] + 1
        else:
            hash_freq[all_hash[i]] = 1
    return hash_freq


def topten_hashtags(all_hash_freq):
    for hashtag, frequency in nlargest(10, all_hash_freq.iteritems(), key=itemgetter(1)):
        print hashtag, frequency


    
def main():
    
    tweet_file = open(sys.argv[1])
    tweet = tweet_dict(tweet_file)
    hashtag_frequency = calc_hashtag_frequency(tweet)
    topten_hashtags(hashtag_frequency)

if __name__ == '__main__':
    main()
