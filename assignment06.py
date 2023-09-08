# Assignment 06, STAT 3250

# Two *very* important rules that must be followed in order for your assignment
# to be graded correctly:

# a) The Python file name must be exactly "assignment00.py" with the correct two digit
# assignment number and without the quotes.
# b) The variables names like q1, q2, ... will be used to grade the assignment.
# They are initially set to `None` but you must set them equal to your final answer.
# If you don't know the answer, leave the variable as `None`.

# Notes:
# The autograder will run your python file in order to grade the q1, q2, ... variables.
# If your code throws an error, then the autograder will not be able to grade it and
# you will receive a zero.
# Before you submit, run your entire file locally to make sure there are no errors.

# The autograder's dataset will be slightly different than the one you are given.
# Make sure none of your answers are hard coded.


# q0: Preprocessing
import pandas as pd


customer_service_tweets_small = pd.read_csv('customer-service-tweets-small.csv')

# Convert the `author_id` column to be all lowercase.
customer_service_tweets_small['author_id'] = customer_service_tweets_small['author_id'].str.lower()

# q1
# A tweet's author is identified by the `author_id` column.
# If the `author_id` is a number, then it is a user's account.
# Otherwise it is a company's account.
# Find the unique (lowercase) names of all the company accounts and submit it as a numpy array in 
# alphabetical order.
only_company_accounts = customer_service_tweets_small.query('~author_id.str.isnumeric()')
unique_company_names = only_company_accounts['author_id'].unique()
unique_company_names.sort()
q1 = unique_company_names

# q2

# On average, how many characters are each company's tweets?
# Submit a Series where the index in the company name and the values are the average
# characters per tweet in descending order.


only_company_accounts['length_tweet'] = only_company_accounts['text'].str.len()

q2 = pd.Series(data = only_company_accounts.groupby('author_id')['length_tweet'].mean()).sort_values(ascending=False)


# q3

# Some tweets have multiple responses.
# Find all the tweets where there is more than one `response_tweet_id`.
# Submit a Series of the corresponding original `tweet_id`s in ascending order.

# Hint: First, try converting the `response_tweet_ids` column from a string series to
# a list series where each element of a list contains all the responses for that tweet.

customer_service_tweets_small['response_tweet_id_list'] = customer_service_tweets_small['response_tweet_id'].str.split(',')
more_than_one_response = customer_service_tweets_small.query('response_tweet_id_list.str.len() > 1')

q3 = pd.Series(data = more_than_one_response['tweet_id']).sort_values()


# q4

# Convert the `created_at` column to a pandas datetime column if you have not already
# done so.
only_company_accounts['created_at'] = pd.to_datetime(only_company_accounts['created_at'])
# Do these companies work on the weekends?
# Find the ratio of the average number of tweets per day sent out by companies on the 
# weekdays vs the weekends.
# Submit a ratio of weekday average per day over weekend average per day.
# Do not hard code the final answer.

only_company_accounts['day_of_week'] = only_company_accounts['created_at'].dt.dayofweek

num_tweets_monday = len(only_company_accounts[only_company_accounts['day_of_week'] == 0])
num_tweets_tuesday = len(only_company_accounts[only_company_accounts['day_of_week'] == 1])
num_tweets_wednesday = len(only_company_accounts[only_company_accounts['day_of_week'] == 2])
num_tweets_thursday = len(only_company_accounts[only_company_accounts['day_of_week'] == 3])
num_tweets_friday = len(only_company_accounts[only_company_accounts['day_of_week'] == 4])
num_tweets_saturday = len(only_company_accounts[only_company_accounts['day_of_week'] == 5])
num_tweets_sunday = len(only_company_accounts[only_company_accounts['day_of_week'] == 6])

average_tweets_weekday=(num_tweets_monday+num_tweets_tuesday+num_tweets_wednesday+num_tweets_thursday+num_tweets_friday)/5
average_tweets_weekend=(num_tweets_saturday+num_tweets_sunday)/2
q4 = average_tweets_weekday/average_tweets_weekend


# q5

# Does this behavior differ between companies?
# For each company in the dataset, calculate the ratio of the average number of 
# tweets sent per day on the weekday over the average number of tweets sent
# per day on the weekends.
# Submit a Series of the companies who on average send at least 5 times more tweets 
# per day on the weekdays than on the weekends in descending order.
# The index should be the company name and the values should be the ratios.
customer_service_tweets_small['created_at'] = pd.to_datetime(customer_service_tweets_small['created_at'])
customer_service_tweets_small['day_of_week'] = customer_service_tweets_small['created_at'].dt.dayofweek
# only_weekdays = customer_service_tweets_small.query('0 <= day_of_week <= 4')
# only_weekends = customer_service_tweets_small.query('day_of_week == 5 or day_of_week == 6')

company_tweets_week = only_company_accounts.groupby(['author_id', 'day_of_week']).size()

company_tweets_week = company_tweets_week.to_frame()
company_tweets_week['num_tweets'] = company_tweets_week[0]

only_weekday_tweets = company_tweets_week.query('0 <= day_of_week <= 4')
only_weekend_tweets = company_tweets_week.query('day_of_week == 5 or day_of_week == 6')
# total_tweets_weekday = len(only_weekday_tweets)
# total_tweets_weekend = len(only_weekend_tweets)
weekday_averages = only_weekday_tweets.groupby('author_id')['num_tweets'].sum()/5
weekend_averages = only_weekend_tweets.groupby('author_id')['num_tweets'].sum()/2
both_averages = pd.DataFrame({'weekday_averages':weekday_averages, 'weekend_averages':weekend_averages})
both_averages['ratio'] = both_averages['weekday_averages']/both_averages['weekend_averages']
five_times_more = both_averages.query('ratio >= 5')




q5 = pd.Series(data=five_times_more['ratio']).sort_values(ascending=False)




# q6

# In 2017, what were the dates with the top 13 most tweets from companies?
# Submit a Series where the index is the date and the values are the counts
# sorted in descending order.
# Be sure to include all ties.


only_2017_companies = only_company_accounts.query('created_at.dt.year == 2017')
only_2017_companies['created_at'] = only_2017_companies['created_at'].dt.date
company_tweets_dates = only_2017_companies.groupby('created_at').size().sort_values(ascending=False)





q6 = company_tweets_dates.head(13)
# q7

# Calculate the total number of tweets sent out by each company.
# Submit a series with the company name as the index and the counts as the values
# sorted in descending order.
num_tweets_by_company = only_company_accounts.groupby('author_id').size().sort_values(ascending=False)
q7 = num_tweets_by_company


# q8

# First, find the company that sent out the most tweets.
# Do this without hardcoding the company name.

company_most_tweets = num_tweets_by_company.index[0]
# Next, find all the tweets in the dataset that involved this company.
# Tweets that involved the company include:
# 1. Tweets the company sent out
# 2. Other tweets the company responded to
# 3. Other tweets that responded to the company's tweets

# Submit a Series that contains all the tweet_ids in ascending order.

# Hint: To "flatten" a list series, consider using the `pd.Series.explode` method.


only_company_most_tweets = customer_service_tweets_small.query('author_id == @company_most_tweets')
in_response_to_tweet_id_most = only_company_most_tweets['in_response_to_tweet_id']
tweet_id_most = only_company_most_tweets['tweet_id']
# 1. tweets sent by company
# 2. tweets with in_response_to_tweet_id to tweet_id of all askciti's tweets
# 3. tweets that the company responded to 
includes_company_most_tweets = customer_service_tweets_small.query('(author_id == @company_most_tweets) or (text.str.contains(@company_most_tweets, case=False) and in_response_to_tweet_id.isin(@tweet_id_most)) or tweet_id.isin(@in_response_to_tweet_id_most)')


q8 = pd.Series(data=includes_company_most_tweets['tweet_id']).sort_values()


# q9

# Word Bigrams Part 1

# Say we want to find the most common word bigrams in the tweets.
# A word bigram is a sequence of two words.
# For example, in the previous sentence, (a, word) is a bigram as well as 
# (word, bigram), (bigram, is), and (is, a).

# There are a couple of things we must keep in mind.
# First, we want to make sure that the bigrams do not cross between tweets.
# We also want to clean the text to some extent.
# Specifically, we want to change all text to lower case and remove any leading or 
# trailing punctuation like `.,?!` on every word.

# Our goal is to create a string series of all the bigrams in all the tweets where 
# each row contains a single bigram.
# This would look like:

# [ our goal      ]
# [ goal is       ]
# [ is to         ]
# [ ...           ]
# [ single bigram ]

# Once we have this data structure, finding the most common bigrams will be easy.
# You could try a different approach if you would like to.

# Step 1

# First, create a short string that is not found in any of the tweets.
# Append the string to be the last word of every tweet (don't forget the space).
# This string will help us know when we are crossing into a new tweet.

customer_service_tweets_small['text'] = customer_service_tweets_small['text'] + " randomasdfsdf"
# Step 2

# Flatten the text of all the tweets so that each word is its own row.
# Lowercase all the words and remove leading and trailing punctuation.
# Submit this Series for Question 9 where the index starts from 0 and 
# increments by 1 every row.

lowercase_tweets = customer_service_tweets_small['text'].str.lower()
each_own_row = lowercase_tweets.str.split().explode()
strip_punc = each_own_row.str.strip('.,?!')



series_of_words = pd.Series(strip_punc).reset_index(drop=True)
q9 = series_of_words


# q10

# Word Bigrams Part 2

# Step 3

# Next, concatenate each row with the word on the next row.
# Include a space between the words.
# Find the top 25 most common bigrams excluding ones that contain your 
# special string from before.
# Submit a Series where the index is the bigram and the values 
# are the counts in descending order.

# Hint: Keep in mind how the Series Index affects computations.

cat_each_row = series_of_words.str.cat(series_of_words.shift(-1), sep=' ')
remove_added_string = pd.DataFrame(cat_each_row).query('~text.str.contains("randomasdfsdf", na=False)')
top_25 = remove_added_string.value_counts().head(25)
q10 = top_25
