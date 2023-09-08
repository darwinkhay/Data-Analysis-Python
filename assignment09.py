# Assignment 09, STAT 3250

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


# Datasets

# WeBWorK logs

# The first dataset contains the set of all WeBWorK log entries on April 1, 2011.
# The entries are organized by one log entry per line, with each line including the following:
# * the date and time of the entry
# * a number that is related to the user (but is not unique)
# * the epoch time stamp
# * a hyphen
# * the "WeBWorK url" that was accessed
# * the "runTime" required to process the problem

# Github Repository Metadata

# [Github](https://github.com/) is a web-based platform for version control and collaborating on
# code development.
# It uses the `git` version control tool and provides a place to store your code on the cloud.
# Users can upload and share code projects, called *repositories* so other can see and contribute.

# The second dataset contains metadata on public repos stored on Github that have more than 5 stars.
# The data is in the JSON format.
# Some important fields include:
# * owner: the username who owns the Github repo
# * name: the name of the repo
# * stars: the number of stars (similar to likes) a repo has
# * languages: a list of languages used as well the size in byes of code written in that language
# sorted in descending order
# * pushedAt: the most recent update to the repo
# * diskUsageKb: the disk usage of the repo in kilobytes (use base 10)
import pandas as pd
classlogs = open('classlogs.txt', encoding='utf8').read().splitlines()
github = pd.read_json('github-repo-metadata.json', orient='index')


classlogs_series = pd.Series(classlogs)
date = classlogs_series.str.split(' ').str[0].str.slice(start=1) + ' ' + classlogs_series.str.split(' ').str[1] + ' ' + classlogs_series.str.split(' ').str[2]
time = classlogs_series.str.split(' ').str[3]
year = classlogs_series.str.split(' ').str[4].str.slice(stop=-1)
date_time = date + ' ' + time + ' ' + year
number_user = classlogs_series.str.split(' ').str[5]
epoch_time_stamp = classlogs_series.str.split(' ').str[6]
webwork_url = classlogs_series.str.split(' ').str[8].str.slice(start=1, stop=-1)
runtime = classlogs_series.str.split(' ').str[11]

classlogs_df = pd.DataFrame()
classlogs_df['date_time'] = date_time
classlogs_df['number_user']= number_user
classlogs_df['epoch_time_stamp'] = epoch_time_stamp
classlogs_df['webwork_url'] = webwork_url
classlogs_df['runtime'] = runtime



# Question 1

# The second element of the Webwork url corresponds to the class name.
# Class names with different semesters or professor names should be treated as different classes.
# How many logs does each class have?
# Submit a Series where the the index is the class name and the values are the counts of the class
# in descending order.
class_name = classlogs_df['webwork_url'].astype(str).str.split('/').str[2]
classlogs_df['class_name'] = class_name 
class_log_count = classlogs_df.groupby('class_name').size()
class_log_count = class_log_count[~(class_log_count.index == '')]
q1 = class_log_count.sort_values(ascending=False)


# Question 2

# Which classes have the longest average run times?
# Submit a series where the index is the class and the values are the average run time in descending
# order.
classlogs_df['runtime'] = pd.to_numeric(classlogs_df['runtime'])
class_longest_avg_run_time = classlogs_df.groupby('class_name')['runtime'].mean()
class_longest_avg_run_time = class_longest_avg_run_time[~(class_longest_avg_run_time.index == '')]
q2 = class_longest_avg_run_time.sort_values(ascending=False)


# Question 3

# A log entry that came from an *initial log in* has a Webwork url of the form:

#     [/webwork2/ClassName] or [/webwork2/ClassName/]
#
# i.e the url terminates after the class name.
# Find the mean runtime in seconds of *initial log ins* and the mean runtime of log ins that were
# not initial log ins.
# Submit a series with 2 rows where the index is "initial_login" and "not_initial_login" and the
# values are the mean seconds.
# Sort by index in ascending order.


classlogs_df['url'] = classlogs_df['webwork_url'].astype(str).str.split('/').apply(lambda url: list(filter(None, url)))
classlogs_df['size_of_url'] = classlogs_df['url'].apply(len)
initial_login = classlogs_df.query('size_of_url == 2')
not_initial_login = classlogs_df.query('size_of_url != 2')

mean_runtime_intial_login = initial_login['runtime'].mean()
mean_runtime_not_initial_login = not_initial_login['runtime'].mean()


q3 = pd.Series(data={'initial_login': mean_runtime_intial_login, 'not_initial_login': mean_runtime_not_initial_login})


# Question 4

# Let's define work hours to be between 9 am to 5 pm (inclusive).
# For each class, find the proportion of logs that were outside of work hours.
# Submit a Series where the index in the class and the values are the proportion of logs that were
# outside of work hours in ascending order.
classlogs_df['time'] = pd.to_datetime(classlogs_df['date_time'])
outside_of_work_hours = classlogs_df.query("~('2011-04-01 09:00:00' <= time <= '2011-04-01 17:00:00')")
outside_class_counts = outside_of_work_hours.groupby('class_name').size()
outside_class_counts = outside_class_counts[~(outside_class_counts.index == '')]
total_class_counts = classlogs_df.groupby('class_name').size()
total_class_counts = total_class_counts[~(total_class_counts.index == '')]
q4 = (outside_class_counts/total_class_counts).sort_values(ascending=True)


# Question 5

# Determine the proportion of log entries that were accessing a problem.
# For those, the WeBWorK url has the form

#     [/webwork2/ClassName/AssignmentName/Digit]
#
# or

#     [/webwork2/ClassName/AssignmentName/Digit/]

# where "ClassName" is the name of the class, "AssignmentName" the name of the assignment, and
# "Digit" is a positive digit.
# (Any digit in the 'Digit' position is considered a problem.)


accessing_a_problem = classlogs_df.query('size_of_url == 4')
accessing_a_problem['digit'] = accessing_a_problem['url'].apply(lambda url: url[3]) 
accessing_a_problem = accessing_a_problem.query('digit.str.isnumeric()')

q5 = len(accessing_a_problem)/len(classlogs_df)


# Question 6

# Which problems have the the highest average runtimes?
# A specific problem can be identified by the ClassName, AssignmentName, and Digit.
# Find the average runtimes for each problem in the logs.
# Submit a series where the index is `ClassName:AssignmentName:Digit` and the values are the average
# runtime in descending order.

accessing_a_problem['specific_problem'] = accessing_a_problem['url'].apply(lambda url: url[1]) + ':' + accessing_a_problem['url'].apply(lambda url: url[2]) + ':' + accessing_a_problem['url'].apply(lambda url: url[3])

avg_runtime_each_problem = accessing_a_problem.groupby('specific_problem')['runtime'].mean()
q6 = avg_runtime_each_problem.sort_values(ascending = False)


# Question 7

# Which Github owners have the most cumulative stars+forks+watchers?
# Submit your answer as a series with the index as the owner and the values as the cumulative stars
# + forks + watchers.
github['cumulative'] = github['stars'] + github['forks'] + github['watchers']
most_cumulative_all = github.groupby('owner')['cumulative'].sum()
q7 = most_cumulative_all


# Question 8

# How much code was written for each language?

# Find the size in *megabytes* of the code written in each language in the repos dataset.
# Submit a Series where the index is the language and the values are the size of the code written in
# megabytes.

languages = pd.json_normalize(github['languages'])
def get_size(d):
    if d is None:
        return 0
    return d['size']
def get_names(d):
    if d is None:
        return None
    return d['name']
sizes_df = languages.applymap(get_size)
names_df = languages.applymap(get_names)

all_languages = pd.concat([sizes_df[size].groupby(names_df[name]).sum()
                    for size, name in zip(sizes_df.columns, names_df.columns)], axis=1)



all_languages_sizes = all_languages.sum(axis=1)
q8 = all_languages_sizes/1000000


# Question 9

# Is the primary language of a repository always the one with the most written code?

# Find the repos where the primary language is **not** the language with the most code written.
# Include repos where the languages field is empty but not when the primaryLanguage is empty.
# For these repos, find the number of occurences of each primary language.

# Submit a Series where the index is the primaryLanguage and the values are the counts in descending
# order.


github['most_language'] = names_df[0]

not_most_language = github.query('primaryLanguage != most_language')
not_most_language = not_most_language.query('primaryLanguage.isna() == False')
num_occurences_primary_language = not_most_language.groupby('primaryLanguage').size()
q9 = num_occurences_primary_language.sort_values(ascending = False)


# Question 10

# The languages field contains the top 10 most used languages in the repo as well as the size in
# bytes of the amount of code written in that language.
# Find the difference in kilobytes between `diskUsageKb` and the sum of the sizes in the languages
# column of each repo.

# Submit a Series of the repos where the sum of the language sizes is greater than the disk usage
# Kb, since that seems unusual.
# The index should be `nameWithOwner` and the values should be the diskUsageKb minus the sum of the
# language sizes sorted in ascending order.

all_languages2 = sizes_df
all_languages2['size_sum'] = all_languages2.sum(axis = 1)
github['size_sum'] = all_languages2['size_sum']/1000
github['size_difference'] = github['diskUsageKb'] - github['size_sum']  
sum_greater_than_disk = github.query('size_difference < 0')
q10 = sum_greater_than_disk.set_index('nameWithOwner')['size_difference'].sort_values(ascending = True)
