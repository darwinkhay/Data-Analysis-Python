# Darwin Khay
# dkk8es

# Assignment 04, STAT 3250

# Two *very* important rules that must be followed in order for your assignment
# to be graded correctly:

# a) The Python file name must be exactly "assignment04.py" with the correct two digit
# assignment number and without the quotes.
# b) The variables names like q1, q2, ... will be used to grade the assignment.
# They are initially set to `None` but you must set them equal to your final answer.
# If you don't know the answer, leave the variable as `None`.

# Notes:
# The autograder will run your python file in order to grade the q1, q2, ... variables.
# If your code throws an error, then the autograder will not be able to grade it and
# you will receive a zero.
# Before you submit, run your entire file locally to make sure there are no errors.

# Submission Instructions: Submit your code file in Gradescope under 
# 'Assignment 4 Code'.  The autograder will evaluate your answers to
# Questions 1-8, but all code (including that for the graphs) must be
# included.  

# The graphs in Questions 9-16 should be submitted under "Assignment 4 Graphs".
# Save each of your graphs as a PNG file, then submit each one separately
# under the corresponding question.  


#### Questions 1-8

##  The questions in this section refer to the data in the file
##  'employee_data.csv'.  The data contains 711 records from an
##  employer, with 21 columns of data for each record.  (There
##  are a few missing values indicated by zeros where zeros 
##  are clearly not appropriate.)  The file 'README_employee_data.pdf' 
##  has a summary of the meanings for the variables.
##
##  All of these questions can be completed **without** loops.  You 
##  should try to do them this way, the time to run your code is impacted 
##  by loops.
import pandas as pd
import seaborn as sns

employee_data = pd.read_csv('employee_data.csv')

# Question 1

# Find the mean body mass index among all records.

q1 = employee_data['Body mass index'].mean()


# Question 2

# Determine the number of records corresponding to being absent on a Wednesday.
only_wednesday = employee_data[employee_data['Day of the week']==4]

# absent_on_wednesday = only_wednesday[only_wednesday['Month of absence'] != 0]

q2 = len(only_wednesday)


# Question 3

# Find the number of unique employees IDs for employees with a height of 
# at least 170 for at least one record.
at_least_170 = employee_data[employee_data['Height'] >= 170]

q3 = len(at_least_170['ID'].unique())




# Question 4

# Find the average transportation expense for the records of employees that 
# are social drinkers and have at least two pets

social_drinkers = employee_data[employee_data['Social drinker'] == 1]
drinkers_2_pets = social_drinkers[social_drinkers['Pet']>= 2]


q4 = drinkers_2_pets['Transportation expense'].mean()


# Question 5

# Find the number of records corresponding to each education group.
# Given your answer as a Series with index equal to the education group
# and values equal to the corresponding number of records, 
# sorted by number of records from most to least.

q5 = employee_data['Education'].value_counts()


# Question 6

# Find the number of records for an employee with 0 pets, the number for an
# employee with 1 pet, and so on. Given your answer as a Series with index equal
# to the number of pets and values equal to the corresponding number of records, 
# sorted by number of pets from least to most.

q6 = employee_data['Pet'].value_counts(ascending=True).sort_index()


# Question 7

# Find the 5 employee IDs that appear in the most records, along with the
# number of records for each.  Given your answer as a Series with index equal
# to the IDs and values equal to the corresponding number of records, sorted
# from most to least records.
employee_id_count = employee_data['ID'].value_counts()


q7 = pd.Series(data=employee_id_count.head())


# Question 8

# Among the records for absences of at least 4 hours, find the percentage
# that involved employees over 35 years old.  (Be sure your answer is in
# percentage and not proportion.)
absent_at_least_4_hours = employee_data[employee_data['Absenteeism time in hours'] >= 4]
over_35_years = absent_at_least_4_hours[absent_at_least_4_hours['Age'] > 35]

q8 =(len(over_35_years)/len(absent_at_least_4_hours))*100


#### Questions 9-16

## These questions use the data from "nfl_data01.csv".  There is information 
## about the data in this file in 'README_nfl_data01.txt'.
## For these questions you should generate graphs that match those given 
## in the file "assignment04-modelgraphs.pdf".

## The graphs in Questions 9-16 should be submitted under "Assignment 4 Graphs".
## Save each of your graphs as a PNG file, then submit each one separately
## under the corresponding question.  
nfl_data01 = pd.read_csv('nfl_data01.csv')

# Question 9

# Generate a histogram of the values of the variable 'Yards'.  Your
# graph should match that given in Graph 9.

sns.displot(data = nfl_data01, x = 'Yards', binrange=[-10,40], binwidth=5).set(xlabel='Yards gained', ylabel='Number of plays', title='Distribution of yards gained')

# Question 10

# Generate a histogram of the values of the variable 'ToGo'.  Your
# graph should match that given in Graph 10. (The edges of the bins 
# are Blue and the insides are Orange.)

sns.displot(data = nfl_data01, x ='ToGo',binrange=[0,16], binwidth=2, color='orange', edgecolor='blue', stat='probability').set(xticks=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16], yticks=[0,0.15,0.3,0.45],xlabel='Yards to go', title='Distribution of yards to go')

# Question 11

# Generate a boxplot of the values of the variable 'ToGo'.  Your
# graph should match that given in Graph 11.  (The color of the
# box is Red.)

sns.boxplot(data = nfl_data01, x='ToGo', color='Red').set(xlabel='Yards to go', title='Distribution of yards to go')

# Question 12

# Generate a boxplot of the values of the variable 'Yards'.  Your
# graph should match that given in Graph 12.  The width of the box 
# should be 30% of the width of the bounding box. (The color of
# the box is Green.)

sns.boxplot(data=nfl_data01, y='Yards', color='Green', width=0.3).set(ylabel='Yards gained', title='Boxplot of Yards Gained',yticks=[-10,-5,0,5,10,15,20,25,30,35,40])

# Question 13

# Generate a scatterplot of the values of the variables 'Yards' (on
# the x-axis) vs. 'ToGo' (on the y-axis).  Your graph should match 
# that given in Graph 13.  

sns.relplot(data=nfl_data01, x='Yards', y='ToGo').set(xlabel='Yards gained', ylabel='Yards to go', title='Yards gained vs. Yards to go')
# Question 14

# Generate a scatterplot of the values of the variables 'ToGo' (on
# the x-axis) vs. 'Yards' (on the y-axis), including a trend line.
# Your graph should match that given in Graph 14.  (The color of 
# the individual markers and trend line is Red.)

sns.regplot(data=nfl_data01, x='ToGo', y='Yards', ci=None,color='Red',marker='+').set(xticks=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15], yticks=[-10,-5,0,5,10,15,20,25,30,35,40],xlabel='Yards to go', ylabel='Yards gained', title='Yards to go vs. Yards gained')
# Question 15

# Generate a plot showing the counts of the variable 'Formation'. Your 
# graph should match that given in Graph 15.  

sns.countplot(data=nfl_data01, x='Formation').set(xlabel='Formation type', ylabel='Number of plays', title='Play formation counts')
# Question 16

# Generate a barplot showing the average values of the variable 'Yards' 
# for each variable 'PlayType'. Your graph should match that given in
# Graph 16. (The color of the bars is Orange.) 

sns.barplot(data=nfl_data01, y='Yards', x='PlayType', color='Orange',ci=None, order=['FUMBLES', 'PASS', 'RUSH','SACK']).set(xlabel='Type of play', ylabel='Average yards', title='Average yards by play type')


