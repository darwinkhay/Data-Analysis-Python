# Assignment 08, STAT 3250

# Two *very* important rules that must be followed in order for your assignment to be graded
# correctly:

# 1. The Python file name must be exactly "assignment08.py" with the correct two digit assignment
# number and without the quotes.
# 2. The variables names like q1, q2, ... will be used to grade the assignment. They are initially
# set to `None` but you must set them equal to your final answer. If you don't know the answer,
# leave the variable as `None`.

# Notes:
# The autograder will run your python file in order to grade the q1, q2, ... variables.
# If your code throws an error, then the autograder will not be able to grade it, and
# you will receive a zero.
# Before you submit, run your entire file locally to make sure there are no errors.

# The autograder's dataset will be slightly different from the one you are given.
# Make sure none of your answers are hard coded.

# Dataset

# This assignment requires data from three files: 
#
#      'ratings.txt':  A file of over 1,000,000 movie ratings
#      'reviewers.txt':  A file of over 6000 reviewers who provided ratings
#      'movies.txt':  A file of nearly 3900 movies
#
# The file 'README08.txt' has more information about these files.
# You will need to consult the readme file to answer some of the questions.

# Suggestion

# It is recommended that you merge the data from the three files into a single
# dataframe.  Although this requires some initial preprocessing, it will make 
# questions requiring data from more than one file much easier.  Good luck!
import pandas as pd
import numpy as np
ratings = open('ratings.txt', encoding='utf8').read().splitlines()
reviewers = open('reviewers.txt', encoding='utf8').read().splitlines()
movies = open('movies.txt', encoding='utf8').read().splitlines()


rating = pd.Series(ratings)
reviewer = pd.Series(reviewers)
movie = pd.Series(movies)

movie_id = movie.str.split('::').str[0]
movie_names = movie.str.split('::').str[1]
movie_genre = movie.str.split('::').str[2]

movies_df = pd.DataFrame()
movies_df['movie_id'] = movie_id
movies_df['name'] = movie_names
movies_df['genre'] = movie_genre


reviewer_gender = reviewer.str.split('::').str[1]
reviewer_id = reviewer.str.split('::').str[0]
reviewer_age = reviewer.str.split('::').str[2]
reviewer_occupation = reviewer.str.split('::').str[3]
reviewer_zipcode = reviewer.str.split('::').str[4]
reviewer_state = reviewer.str.split('::').str[5]

reviewers_df = pd.DataFrame()
reviewers_df['reviewer_id'] = reviewer_id
reviewers_df['gender'] = reviewer_gender
reviewers_df['age'] = reviewer_age
reviewers_df['occupation'] = reviewer_occupation
reviewers_df['zipcode'] = reviewer_zipcode
reviewers_df['state'] = reviewer_state


rating_reviewerid = rating.str.split('::').str[0]
rating_movieid = rating.str.split('::').str[1]
rating_rating = rating.str.split('::').str[2]
rating_timestamp = rating.str.split('::').str[3]

ratings_df = pd.DataFrame()
ratings_df['reviewer_id'] = rating_reviewerid
ratings_df['movie_id'] = rating_movieid
ratings_df['rating'] = rating_rating
ratings_df['timestamp'] = rating_timestamp

reviewers_and_ratings = pd.merge(reviewers_df, ratings_df, on='reviewer_id')
df = pd.merge(reviewers_and_ratings, movies_df, on='movie_id')


# Question 1

# Which movies are most popular among reviewers? Determine the 10 movie IDs 
# that have the most ratings. (Plus any ties as usual.)  Give a Series with 
# the movie IDs as index and the number of ratings as values, sorted from most 
# to least ratings.


df['rating'] = pd.to_numeric(df['rating'])
only_5_stars = df.query('rating == 5')
movie_5_star_counts = df.groupby('movie_id').size()

q1 = movie_5_star_counts.nlargest(10, keep="all").sort_values(ascending=False)


# Question 2

# Determine the average rating for farmers in the 35-44 age group.
df['occupation'] = pd.to_numeric(df['occupation'])
df['age'] = pd.to_numeric(df['age'])
farmers = df.query('occupation == 8')

farmers_35_44 = farmers.query('age == 35')


q2 = farmers_35_44['rating'].mean()


# Question 3

# Determine the number of movies that received an average rating of greater
# than 4.65.  (Movies with different movie IDs should be considered different.)
avg_rating = df.groupby('movie_id')['rating'].mean()
high_avg_rating = avg_rating[avg_rating > 4.65]
q3 = high_avg_rating.size


# Question 4

# Determine the number of movies listed in the movies data for which there
# is no rating in ratings data.  
no_ratings = ~movies_df['movie_id'].isin(ratings_df['movie_id'])
movies_no_ratings = movies_df.loc[no_ratings]

q4 = len(movies_no_ratings)


# Question 5

# Among the ratings from female reviewers, determine the average  
# rating for each occupation classification (including 'other or not 
# specified'), and give the results in a Series sorted from highest to 
# lowest average with the occupation title (not the code) as index.

female_reviewers = df.query('gender == "F"')
avg_rating_occupation = female_reviewers.groupby('occupation')['rating'].mean()
avg_rating_occupation = avg_rating_occupation.rename(index={0: 'other', 1: 'academic/educator', 2: 'artist',
                                                            3 : 'clerical/admin', 4 : 'college/grad student', 5: 'customer service',
                                                            6: 'doctor/health care', 7: 'executive/managerial', 8: 'farmer', 9: 'homemaker',
                                                            10: 'K-12 student', 11: 'lawyer', 12: 'programmer', 13: 'retired',
                                                            14: 'sales/marketing', 15: 'scientist', 16: 'self-employed', 17: 'technician/engineer',
                                                            18: 'tradesman/craftsman', 19: 'unemployed', 20: 'writer'})
q5 = avg_rating_occupation.sort_values(ascending=False)


# Question 6

# For the reviewers classified as 'lawyer', determine the average rating for 
# each genre, and give the results in a Series with genre as index and average 
# rating as values, sorted alphabetically by genre.
df['genre_exploded'] = df['genre'].str.split('|')
lawyer_reviewers = df.query('occupation == 11')
lawyer_reviewers = lawyer_reviewers.explode('genre_exploded')
avg_rating_each_genre = lawyer_reviewers.groupby('genre_exploded')['rating'].mean()

q6 = avg_rating_each_genre


# Question 7

# Find the top-8 states in terms of average rating.  Give as a Series
# with the state as index and average rating as values, sorted from 
# highest to lowest average.
# Note: See the readme file for information on what constitutes a
# "state" for this assignment.

avg_rate_states = df.groupby('state')['rating'].mean()
top_8_states = avg_rate_states.nlargest(8, keep='all').sort_values(ascending=False)

q7 = top_8_states


# Question 8

# For the reviewer age category, assume that the reviewer has age at the 
# midpoint of the given range.  (For instance '35-44' has age (35+44)/2 = 39.5)
# For 'under 18' assume an age of 16, and for '56+' assume an age of 60.
# For each possible genre, determine the average age of the reviewers of
# movies with that genre. Give your answer as a Series with genre as index
# and average age as values, sorted by average age from highest to lowest.
def midpointage(reviewers_df):
    # age = reviewers_df['age']
    # midpoint_age = age.copy()
    # midpoint_age[age == 1] = 16
    # midpoint_age[age == 18] = 21
    # midpoint_age[age == 25] = 29.5
    # midpoint_age[age == 35] = 39.5
    # midpoint_age[age == 45] = 47
    # midpoint_age[age == 50] = 52.5
    # midpoint_age[age == 56] = 60
    # reviewers_df['midpoint_age'] = midpoint_age
    # return reviewers_df
    age = reviewers_df['age']
    reviewers_df['midpoint_age'] = np.where(age == 1, 16,
                                             np.where(age == 18, 21,
                                                      np.where(age == 25, 29.5,
                                                               np.where(age == 35, 39.5,
                                                                        np.where(age == 45, 47,
                                                                                 np.where(age == 50, 52.5,
                                                                                          np.where(age == 56, 60, age)))))))
    return reviewers_df
   


reviewers_midpoint_age = midpointage(df)
reviewers_midpoint_age = reviewers_midpoint_age.explode('genre_exploded')
avg_age_reviewers_genre = reviewers_midpoint_age.groupby('genre_exploded')['midpoint_age'].mean()


q8 = avg_age_reviewers_genre.sort_values(ascending=False)


# Question 9

# For each state (including 'Unknown'), determine the occupation that gave the  
# lowest average rating.  Give a Series that includes the state code and 
# occupation title as a multiindex, and average rating as values.  Sort  
# the Series alphabetically by state code. 

occupation_low_avg_rating = df.set_index(['state', 'occupation'])['rating']
occupation_low_avg_rating = occupation_low_avg_rating.groupby(['state', 'occupation']).mean()
occupation_low_avg_rating = occupation_low_avg_rating.rename(index={0: 'other', 1: 'academic/educator', 2: 'artist',
                                                            3 : 'clerical/admin', 4 : 'college/grad student', 5: 'customer service',
                                                            6: 'doctor/health care', 7: 'executive/managerial', 8: 'farmer', 9: 'homemaker',
                                                            10: 'K-12 student', 11: 'lawyer', 12: 'programmer', 13: 'retired',
                                                            14: 'sales/marketing', 15: 'scientist', 16: 'self-employed', 17: 'technician/engineer',
                                                            18: 'tradesman/craftsman', 19: 'unemployed', 20: 'writer'})

q9 = occupation_low_avg_rating.sort_index(level=0)


# Question 10

# We want to find the highest rated movies. However, each reviewer may have 
# different tendencies to give lower or higher ratings. To account for this, 
# we first normalize the ratings per reviewer. For each reviewer, subtract all 
# their ratings by the reviewer's mean rating then divide by the standard error 
# (standard deviation) of the reviewer's rating. Once you have the normalized 
# ratings, determine the mean normalized rating by movie.  Give a Series of
# the top-15 (plus any ties) with movie titles (with year) as index and mean normalized
# ratings as values, sorted by normalized ratings from biggest to smallest.

reviewer_mean_sd = df.groupby('reviewer_id')['rating'].agg(['mean', 'std'])
df_with_reviewer_mean_sd = pd.merge(df, reviewer_mean_sd, on='reviewer_id')
df_with_reviewer_mean_sd['normalized_rating'] = (df_with_reviewer_mean_sd['rating'] - df_with_reviewer_mean_sd['mean'])/df_with_reviewer_mean_sd['std']

mean_normalized_rating_each_movie = df_with_reviewer_mean_sd.groupby('name')['normalized_rating'].mean()


q10 = mean_normalized_rating_each_movie.nlargest(n=15, keep='all').sort_values(ascending=False)


