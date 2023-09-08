# Assignment 11, STAT 3250

# Two *very* important rules that must be followed in order for your assignment 
# to be graded correctly:

# 1. The Python file name must be exactly "assignment11.py" with the correct 
#    two digit assignment number and without the quotes.
# 2. The variables names like q1, q2, ... will be used to grade the assignment. 
#    They are initially set to `None` but you must set them equal to your final 
#    answer. If you don't know the answer, leave the variable as `None`.

# Notes:
# The autograder will run your python file in order to grade the q1, q2, ... 
# variables. If your code throws an error, then the autograder will not be 
# able to grade it, and you will receive a zero.
# Before you submit, run your entire file locally to make sure there are no errors.

# The autograder's dataset will be slightly different from the one you are given.
# Make sure none of your answers are hard coded.

# For this assignment you will be working with Twitter data related to the
# opening of final Game of Thrones season on April 14, 2019.  You will use 
# a set of over 10,000 tweets for this purpose.  The data is in the file 
# 'GoT_tweets.txt'.  

# Note: See the file twitter.py for the code to read in the data.  That
# will make the assignment much easier than trying to read the data in as
# straight text. This file also has an example of tweet data that shows the
# dictionary structure.
import pandas as pd
import json
import re


tweetlist = []
for line in open('GoT_tweets.txt', 'r'): # Open the file of tweets
    tweetlist.append(json.loads(line))  # Add to 'tweetlist' after converting

tweets = pd.Series(tweetlist)



# Question 1

# Twitter users can have 'verified' accounts, which were previously at no cost
# but recently that has changed.  In our data, each tweet indicates that it was
# posted by a verified user by the flag 'verified' within the 'user' information.
# Determine the number of tweets posted by verified users.

verified_or_not = tweets.str['user'].str['verified']
only_verified = verified_or_not[verified_or_not == True]
q1 = len(only_verified)


# Question 2

# Tweets can be flagged as having potentially sensitive content, either by the
# individual posting the tweet or by an agent of Twitter.  Such tweets are
# indicated in the key 'possibly_sensitive'.  Determine the sscreen names of
# all users who posted more than one potentially sensitive tweet.  Give a
# Series with screen name as index and number of potentially sensitive tweets
# as value, sorted alphabetically by screen name.
possibly_sensitive = tweets.str['possibly_sensitive'].dropna()
possibly_sensitive_true = possibly_sensitive[possibly_sensitive == True]
possibly_sensitive_true_indices = possibly_sensitive_true.index

screen_names_sensitive = tweets[possibly_sensitive_true_indices].str['user'].str['screen_name']
count = screen_names_sensitive.value_counts()
only_more_than_one_sensitive = count[count > 1]
q2 = only_more_than_one_sensitive.sort_index(ascending = True)


# Question 3

# One might expect that the name Daenerys to appear in our collecction of tweets.
# Determine the percentage of tweets that include the name 'Daenerys' in the text 
# of the tweet. Any combination of upper and lower case should be included, and
# also include instances where Daenerys has non-alphanumeric (letters and numbers)
# before or after, such as #daenerys or Daenerys! or @Daenerys.  Do not include
# instances where Daenerys is immediately preceded or followed by letters or
# numbers, such as GoDaenerys or Daenerys87.
daenerys_regex = r'(?i)(?<![a-zA-Z0-9])daenerys(?![a-zA-Z0-9])'

includes_daenerys = tweets.str['text'].str.contains(daenerys_regex)
includes_daenerys_true = includes_daenerys[includes_daenerys == True]


q3 = len(includes_daenerys_true)/len(tweets)

 
# Question 4

# Determine the number of tweets that have 0 user mentions, 1 user mention, 
# 2 user mentions, and so on.  Give your answer as a Series with the number of 
# user mentions as index (sorted smallest to largest) and the corresponding 
# number of tweets as values. Include in your Series index only the number of   
# user mentions that occur for at least one tweet, so for instance, if there
# are no tweets with 7 user mentions then 7 should not appear as an index
# entry. Use the list of user mentions (within 'entities') from each tweet, 
# not the text of the tweet. 

user_mention_counts = tweets.str['entities'].str['user_mentions'].apply(len)
user_mention_counts_counts = user_mention_counts.value_counts()

q4 = user_mention_counts_counts.sort_index(ascending = True)


# Question 5

# Determine the number of tweets that include the hashtag '#GameofThrones'.
# (You may get the wrong answer if you use the text of the tweets instead of 
# the hashtag lists.) Note that Hashtags are not case sensitive, so any 
# combination of upper and lower case are all considered matches so should be 
# counted.
gameofthrones_hashtag_regex = r'(?i)gameofthrones'
match_got_hashtag = tweets.str['entities'].str['hashtags'].explode().str['text'].str.contains(gameofthrones_hashtag_regex)
match_got_hashtag_true = match_got_hashtag[match_got_hashtag == True]

q5 = len(match_got_hashtag_true)


# Question 6

# Some tweeters like to tweet a lot.  Find the screen name for all tweeters
# with at least 3 tweets in this data.  Give a Series with the screen name
# as index and the number of tweets as value, sorting by tweet count from
# largest to smallest

screen_name_tweets = tweets.str['user'].str['screen_name']
screen_name_counts = screen_name_tweets.value_counts()
at_least_three_tweets = screen_name_counts[screen_name_counts >= 3]

q6 = at_least_three_tweets.sort_values(ascending = False)


# Question 7

# Among the screen names with 3 or more tweets, find the average
# 'followers_count' for each and then give a table with the screen and average 
# number of followers.  (Note that the number of followers might change from 
# tweet to tweet.)  Give a Series with screen name as index and the average 
# number of followers as value, sorting by average from largest to smallest.  

at_least_three_tweets_indices = at_least_three_tweets.index
screen_name_indices = screen_name_tweets[screen_name_tweets.isin(at_least_three_tweets_indices)].index
followers_count = tweets[screen_name_indices].str['user'].str['followers_count']
screen_names = tweets[screen_name_indices].str['user'].str['screen_name']

screen_name_followers_counts = pd.DataFrame()
screen_name_followers_counts['screen_name'] = screen_names
screen_name_followers_counts['followers_count'] = followers_count

avg_followers_count = screen_name_followers_counts.groupby('screen_name')['followers_count'].mean()
q7 = avg_followers_count.sort_values(ascending = False)


# Question 8
                                                                
# Determine the hashtags that appeared in at least 25 tweets.  Give
# a Series with the hashtags (lower case) as index and the corresponding 
# number of tweets as values, sorted alphabetically by hashtag.
hashtags = tweets.str['entities'].str['hashtags'].explode().str['text'].str.lower()
hashtags_counts = hashtags.value_counts()
at_least_25 = hashtags_counts[hashtags_counts >= 25]
#cat_least_25.index = at_least_25.index.str.lower()
# **
# at_least_25 = at_least_25.groupby(at_least_25.index).sum()
q8 = at_least_25.sort_index(ascending = True)


# Question 9

# A tweet can contain links, but the Twitter algorithm will downgrade the
# visibility of such tweets when the link is to a site other than Twitter 
# because it considers the tweet to be spam.  Links can be found within 'urls'
# contained in 'entities' for each tweet.  Among the tweets that include links,
# what percentage will not interpreted as spam by Twitter? (Note that one can
# see the whole URL in 'expanded_url'.)
tweets_with_links = tweets.str['entities'].str['urls']

tweets_with_links_mask = tweets_with_links.apply(lambda x: len(x) > 0)

tweets_with_links = tweets_with_links[tweets_with_links_mask]

twitter_links = tweets_with_links.explode().str['expanded_url'].str.contains('https://twitter.com')
only_true = twitter_links[twitter_links == True]
q9 = (len(only_true)/len(tweets_with_links))*100


# Question 10

# Determine which tweets contain a sequence of three or more consecutive digits
# (no spaces between the digits!).  From among those tweets, determine the
# percentage that include a user mention (starts with '@') that has a sequence 
# of three or more consecutive digits.

three_consec_regex = r'\d{3,}'
tweets_with_seq_three_or_more = tweets.str['text'].str.contains(three_consec_regex)
seq_three_or_more_true = tweets_with_seq_three_or_more[tweets_with_seq_three_or_more == True]

user_mention_seq_regex = r'@\w*\d{3,}'
user_mention_three_more = tweets[seq_three_or_more_true.index].str['text'].str.contains(user_mention_seq_regex)
user_mention_three_more_true = user_mention_three_more[user_mention_three_more == True]


q10 = (len(user_mention_three_more_true)/len(seq_three_or_more_true))*100










