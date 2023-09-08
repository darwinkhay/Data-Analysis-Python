# Assignment 12 STAT 3250

# Two *very* important rules that must be followed in order for your assignment to be graded
# correctly:

# 1. The Python file name must be exactly "assignment00.py" with the correct two digit assignment
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

# The dataset contains data on books scraped from Goodread's Best Books Ever list.
# It includes information like title, series, author, genres, characters, etc as well as a score
# which determines a book's ranking in the list.
# Each row corresponds to a book.
import pandas as pd
import numpy as np
import statistics
import re
import ast

books = pd.read_csv('books.csv')

# Question 1

# How many books are written in each language?
# Submit a Series with the language as the index and the number of books as the values sorted in
# descending order.
language_count = books.groupby('language').size()
q1 = language_count.sort_values(ascending=False)


# Question 2

# How many books does each author have on this list?
# For each unique value in the author column, find the number of books for that value.
# Submit as a Series with the author as the index and the counts as the values in descending order.
author_count = books.groupby('author').size()
q2 = author_count.sort_values(ascending = False)


# Question 3

# It turns out the author column can contain the names of multiple contributors including authors,
# illustrators, and editors.
# Assume that each **contributor identifier** is separated by a comma.
# At the end of a contributor identifier, 0 or more **contributor metadata** can be present in
# parentheses like (Goodreads Author) and (Illustrator).
# Define a **contributor name** to be the contributor's identifier that excludes the contributor
# metadata.

# So the contributor identifier `Charlotte Gordon (Goodreads Author) (Introduction)` should become
# the contributor name `Charlotte Gordon`.

# Assume that the contributor name cannot contain any parentheses and do not treat the `"more..."`
# string as a name.

# We want to find out how many books each contributor name is associated with.
# For each contributor name, find the number of books they contributed to.
# Submit a Series with contributors who were associated with at least 10 books where the index is
# the contributor name and the values are the counts sorted in descending order.

# split by comma
# remove words with parenthesis
# have a list for each row that shows contributors?
contributors = books['author'].str.split(',')

for names in contributors:
    for i in range(len(names)):
        names[i] = names[i].split('(')[0].strip()
        names[i] = names[i].split(')')[-1].strip()
    # while '' in names:
    #     names.remove('')
    while 'more…' in names:
        names.remove('more…')
     
        #names[i] = re.sub(r'\s*\([^()]*\)', '', names[i])


       
books['contributors'] = contributors
books2 = books.explode('contributors')
contributor_counts = books2.groupby('contributors').size()
       
        

q3 = contributor_counts[contributor_counts >= 10].sort_values(ascending = False)


# Question 4

# We want to find books that were polarizing, i.e. books that readers either really loved it or
# really hated it.
# The numRatings column seems to be useful to measure this.
# It shows the number of each rating corresponding to 5, 4, 3, 2, 1 where 5 is the highest rating.
# One way to find polarizing books would be to find books that had a large amount of 5's and 1's
# relative to the other ratings.

# For a first attempt, we define the **extreme ratio** metric to be the number of 5 and 1 ratings
# divided by the number of 2, 3, and 4 ratings.
# Calculate the **extreme ratio** for each book that had at least 10000 ratings (`numRatings`).

# Submit a Series where the index is the title and values are the extreme ratio in descending order.
books_10000 = books.query('numRatings >= 10000')
ratingsByStars_lists = books_10000['ratingsByStars'].apply(ast.literal_eval)

#for i in range(len(ratingsByStars_lists)):
#   if i in ratingsByStars_lists.index:
#       ratingsByStars_lists[i] = [int(num) for num in ratingsByStars_lists[i]] 

books_10000['ratingsByStars_num'] = ratingsByStars_lists
number_5_ratings = pd.to_numeric(books_10000['ratingsByStars_num'].apply(lambda x : x[0] if len(x) > 0 else None))
number_4_ratings = pd.to_numeric(books_10000['ratingsByStars_num'].apply(lambda x : x[1] if len(x) > 0 else None))
number_3_ratings = pd.to_numeric(books_10000['ratingsByStars_num'].apply(lambda x : x[2] if len(x) > 0 else None))
number_2_ratings = pd.to_numeric(books_10000['ratingsByStars_num'].apply(lambda x : x[3] if len(x) > 0 else None))
number_1_ratings = pd.to_numeric(books_10000['ratingsByStars_num'].apply(lambda x : x[4] if len(x) > 0 else None))
books_10000['extreme_ratio'] = (number_5_ratings+number_1_ratings)/(number_4_ratings+number_3_ratings+number_2_ratings)

q4 = books_10000.set_index('title')['extreme_ratio'].sort_values(ascending=False)

# Question 5

# A problem with the **extreme ratio** is that books that were extremely highly rated, and books
# that were extremely lowly rated may be ranked high on the list, even if they were not polarizing.
# For example, *The Complete Calvin and Hobbes* overwhelmingly received 5 stars relative to 2, 3,
# and 4s, with only a tiny fraction of 1 stars.
# We should not consider this book as "polarizing".

# So perhaps a better and more principled approach would be to calculate the **variance** of the
# ratings.
# Then, by definition, this would tell us how spread out the ratings are and would be highest for
# books that had a large number of both 5 and 1 stars relative to others.
# For a given list of ratings counts like `[3, 2, 1, 2, 2]` first convert it to its raw ratings `[5,
# 5, 5, 4, 4, 3, 2, 2, 1, 1]`.
# Then the variance can be easily calculated from the raw ratings.

# Calculate the **ratings variance** of each book.
# Submit a Series where the index is the title and the values are the rating variance sorted in
# descending order.
# Notice how *The Complete Calvin and Hobbes* actually has one of the smallest variance in ratings.

# *Hint: the np.repeat function may be useful*.

# if not right, try books_10000?
# ratingsByStars_lists_all = books_10000['ratingsByStars'].apply(ast.literal_eval)

# for i in range(len(ratingsByStars_lists_all)):
#     if i in ratingsByStars_lists_all.index and len(ratingsByStars_lists_all[i]) > 0:
#         ratingsByStars_lists_all[i] = [int(num) for num in ratingsByStars_lists_all[i]]
#         temp = list(np.repeat(5, ratingsByStars_lists_all[i][0])) + list(np.repeat(4, ratingsByStars_lists_all[i][1])) + list(np.repeat(3, ratingsByStars_lists_all[i][2])) + list(np.repeat(2, ratingsByStars_lists_all[i][3])) + list(np.repeat(1, ratingsByStars_lists_all[i][4]))
#         #temp.append(np.repeat(5, ratingsByStars_lists_all[i][0]))
#         #temp.append(np.repeat(4, ratingsByStars_lists_all[i][0]))
#         #temp.append(np.repeat(3, ratingsByStars_lists_all[i][2]))
#         #temp.append(np.repeat(2, ratingsByStars_lists_all[i][3]))
#         #temp.append(np.repeat(1, ratingsByStars_lists_all[i][4]))
#         ratingsByStars_lists_all[i] = temp

# test = np.array(ratingsByStars_lists_all)
# variance = np.var(test, axis = 0)
#for i in range(len(ratingsByStars_lists_all)):
#    if i in ratingsByStars_lists_all.index:
#        temp_variance = statistics.variance(list(ratingsByStars_lists_all[i]))
#        variance_ratings.append(temp_variance)



q5 = pd.Series()


# Question 6

# What is the amount of memory we save by converting the language column and the bookFormat column
# into a categoricals without ordering?
# Submit the number of kiloBytes saved (1000 bytes = 1 kilobyte) by converting those two columns
# into categoricals.
# Use the `Series.memory_usage()` method.
books_language_categorical = books['language'].astype('category')
books_bookformat_categorical = books['bookFormat'].astype('category')


books_language_mem = books['language'].memory_usage() - books_language_categorical.memory_usage()
books_bookformat_mem = books['bookFormat'].memory_usage() - books_bookformat_categorical.memory_usage()

q6 = (books_language_mem + books_bookformat_mem)/1000


# Question 7

# Calculate the number of times each individual genre appears.
# Submit a Series of the top 10 genres (including ties) as the index and their counts in descending
# order.
books['genres'] = books['genres'].apply(ast.literal_eval)
books_genre_exploded = books.explode('genres')
genre_counts = books_genre_exploded.groupby('genres').size()
q7 = genre_counts.nlargest(n=10, keep='all').sort_values(ascending = False)


# Question 8

# We want to convert those top 10 genres from question 7 to their own columns.
# Add the 10 genre columns to the dataframe, where a book has a 1 in a column if it contains that
# genre.
# Use the genre names as the column names.
# Books that do not have any genres should have all zeros for their columns.

# Submit a DataFrame that contains the `title` column as well as the 10 new columns we just created.
# Sort the rows by index in increasing order and the columns by column name in increasing order
# (alphabetical).

# This idea is similar to *one-hot encoding* which is a common feature engineering method in machine
# learning.

# *Hint: the `pd.get_dummies` function may be useful.*

genres_dummies = pd.get_dummies(books_genre_exploded['genres'])
only_top_10_genres = genres_dummies.loc[:, list(q7.index)]
only_top_10_genres = only_top_10_genres.groupby(only_top_10_genres.index).sum()
genres_and_title = pd.DataFrame()
genres_and_title['title'] = books['title']
genres_and_title = pd.concat([genres_and_title, only_top_10_genres], axis = 1)

# make title column the index
#genres_and_title = genres_and_title.set_index('title')

# sort columns in alphabetical order
genres_and_title = genres_and_title.sort_index(axis = 1)
q8 = genres_and_title


# Question 9

# For a random sample of the dataset, we want to find the average price of each `bookFormat`.

# However, there are some prices with unusual formatting like `1.852.88`.
# For all prices that have 2 decimal symbols, replace their price with `NaN`.
# Then, find all books that are classified as English.

# Create a random generator with a seed equal to 3250.
# Then, sample 25% of the rows of the DataFrame using the the `DataFrame.sample` method and pass the
# generator as the `random_state`.
# Calculate the average price for each `bookFormat` and ignore prices that are `NaN`.
# Submit a Series where the index is the bookFormat and the values are the average prices sorted in
# descending order.

rng = np.random.default_rng(
    seed=3250
)
books['price'].loc[books['price'].str.contains('\d+\.\d+\.\d+') & ~books['price'].isna()] = np.nan
english_books = books.query('language == "English"')
random_sample = english_books.sample(frac = 0.25, random_state = rng)



#random_sample['price'].loc[random_sample['price'].str.contains('\d+\.\d+\.\d+') & ~random_sample['price'].isna()] = np.nan

random_sample['price'] = pd.to_numeric(random_sample['price'])
 
avg_price_bookformat = random_sample['price'].groupby(random_sample['bookFormat']).mean()

q9 = avg_price_bookformat.sort_values(ascending = False).dropna()


# Question 10

# In the card game *NotBlackJack*, each player is dealt 2 cards from a standard deck.
# The player's score is determined by the sum of the scores of both cards.
# Numbered cards score their respective number, while Jack, Queen, and King score 10 point.
# Aces always score 11 points.
# Furthermore, of the four ranks: spades, clubs, diamonds, and hearts, a card with spades will
# **subtract** a point while a card with hearts will **add** a point.
# A player (or multiple players) wins if the scores of their two cards sum up to 21.

# For example, the two cards Ace of spades and 5 of diamonds will score $11-1+5+0=15$ points and
# they are not a winner.
# But the two cards Queen of hearts and Jack of clubs will score $10+1+10+0=21$ points and they are
# a winner.

# In a game with 3 players, simulate 200,000 games and calculate what proportion of games have a
# winner.
# Do **not** hardcode the final answer.


ranks = list(str(x) for x in range(2, 11)) + ["Jack", "Queen", "King", "Ace"]
ranks = np.array(ranks)
ranks = pd.Categorical(ranks.repeat(4), categories=ranks, ordered=True)
suits = np.array(["spades", "clubs", "diamonds", "hearts"])
suits = pd.Categorical(np.tile(suits, 13), categories=suits, ordered=True)
deck_of_cards = pd.DataFrame(
    {"rank": ranks, "suit": suits},
)

deck_of_cards['value'] = pd.to_numeric(deck_of_cards['rank'], errors='coerce').astype('Int64')
value_10 = ['Jack', 'Queen', 'King']
deck = []

for i in range(len(deck_of_cards)):
    if deck_of_cards['rank'][i] in value_10:
        deck_of_cards['value'][i] = 10
    elif deck_of_cards['rank'][i] == "Ace":
        deck_of_cards['value'][i] = 11
    if deck_of_cards['suit'][i] == "spades":
        deck_of_cards['value'][i] = deck_of_cards['value'][i] - 1
    elif deck_of_cards['suit'][i] == 'hearts':
        deck_of_cards['value'][i] = deck_of_cards['value'][i] + 1
        
    deck.append({'rank' : deck_of_cards['rank'][i], 'suit': deck_of_cards['suit'][i], 'value' : deck_of_cards['value'][i]})
the_cards = rng.choice(deck, size=(3, 2), replace=False)

def one_game():
    the_cards = rng.choice(deck, size=(3, 2), replace=False)
    the_scores = np.array([
        [the_cards[i][0]['value'], the_cards[i][1]['value']]
        for i in range(3)
    ])
    # check for 21
    for i in range(3):
        if np.sum(the_scores[i]) == 21:
            return True
    return False # otherwise
        
    
winners = sum([one_game() for _ in range(200000)])





q10 = (winners / 200000)
