# Darwin Khay
# dkk8es

# Assignment 05, STAT 3250

# Two *very* important rules that must be followed in order for your assignment
# to be graded correctly:

# a) The Python file name must be exactly "assignment05.py" with the correct two digit
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
# 'Assignment 5 Code'.  The autograder will evaluate your answers to
# Questions 1-9, but all code (including that for the graphs) should be
# included.  

# The graphs in Questions 10-14 should be submitted under "Assignment 5 Graphs".
# Save each of your graphs as a separate PNG file, then submit each one
# separately under the corresponding question.  


# Question 1  

# Determine the number of plays (all games) for which the formation was
# UNDER CENTER.

import pandas as pd
import seaborn as sns
nfl_data02 = pd.read_csv('nfl_data02.csv')

under_center = nfl_data02[nfl_data02['Formation'] == 'UNDER CENTER']

q1 = len(under_center)


# Question 2  

# Determine the mean number of yards ToGo for a first down on the
# Down = 3 plays.
down_3_plays = nfl_data02[(nfl_data02['Down'] == 3)]

q2 = down_3_plays['ToGo'].mean()


# Question 3  

# Determine the mean number of net yards gained by IND on 2nd Down in 
# the IND vs NYJ game.

only_IND = nfl_data02[nfl_data02['OffenseTeam'] == 'IND']
second_down = only_IND[only_IND['Down'] == 2]

q3 = second_down['Yards'].mean()



# Question 4  

# Determine the combined total number of plays resulting in first downs by SF   
# and IND in their games. (Use SeriesFirstDown variable here.)

only_SF = nfl_data02[nfl_data02['OffenseTeam'] == 'SF']
play_1st_down_SF = only_SF[only_SF['SeriesFirstDown'] == 1]
play_1st_down_IND = only_IND[only_IND['SeriesFirstDown'] == 1]


q4 = len(play_1st_down_SF) + len(play_1st_down_IND)


# Question 5  

# Determine the mean net yards gained by IND on plays that had formation  
# UNDER CENTER or NO HUDDLE SHOTGUN.

formation_uc_nhd = only_IND[(only_IND['Formation'] == 'UNDER CENTER') | (only_IND['Formation'] == 'NO HUDDLE SHOTGUN')]

q5 = formation_uc_nhd['Yards'].mean()


# Question 6  

# For each of the teams BUF, DEN, IND, SF, determine the average Yards on 1st
# down. Give your answer as a Series with team identifiers for the index and 
# average yards as the corresponding values, sorted by value from smallest to
# largest.

only_BUF_1st_down = nfl_data02[(nfl_data02['OffenseTeam'] == 'BUF') & (nfl_data02['Down'] == 1)]
only_DEN_1st_down = nfl_data02[(nfl_data02['OffenseTeam'] == 'DEN') & (nfl_data02['Down'] == 1)]
only_IND_1st_down = nfl_data02[(nfl_data02['OffenseTeam'] == 'IND') & (nfl_data02['Down'] == 1)]
only_SF_1st_down = nfl_data02[(nfl_data02['OffenseTeam'] == 'SF') & (nfl_data02['Down'] == 1)]

average_yards_dict = {
    'BUF' : only_BUF_1st_down['Yards'].mean(), 
    'DEN' : only_DEN_1st_down['Yards'].mean(),
    'IND' : only_IND_1st_down['Yards'].mean(),
    'SF' : only_SF_1st_down['Yards'].mean()
    }



q6 = pd.Series(data=average_yards_dict).sort_values()


# Question 7

# For each of BUF, DEN, IND, SF, determine the percentage of plays classified
# as a pass (coded as 1 in the 'IsPass' variable). Give your answer as a 
# Series with team identifiers for the index and means as the corresponding 
# values, sorted alphbetically by team identifier.

only_BUF_pass = nfl_data02[(nfl_data02['OffenseTeam'] == 'BUF') & (nfl_data02['IsPass'] == 1)]
only_DEN_pass = nfl_data02[(nfl_data02['OffenseTeam'] == 'DEN') & (nfl_data02['IsPass'] == 1)]
only_IND_pass = nfl_data02[(nfl_data02['OffenseTeam'] == 'IND') & (nfl_data02['IsPass'] == 1)]
only_SF_pass = nfl_data02[(nfl_data02['OffenseTeam'] == 'SF') & (nfl_data02['IsPass'] == 1)]

only_BUF = nfl_data02[nfl_data02['OffenseTeam'] == 'BUF']
only_DEN = nfl_data02[nfl_data02['OffenseTeam'] == 'DEN']

BUF_pass_percent = len(only_BUF_pass)/len(only_BUF)*100
DEN_pass_percent = len(only_DEN_pass)/len(only_DEN)*100
IND_pass_percent = len(only_IND_pass)/len(only_IND)*100
SF_pass_percent = len(only_SF_pass)/len(only_SF)*100

percent_plays_dict = {
    'BUF' : BUF_pass_percent,
    'DEN': DEN_pass_percent,
    'IND' : IND_pass_percent,
    'SF': SF_pass_percent
    }
q7 = pd.Series(data = percent_plays_dict).sort_index()


# Question 8

# For each of the teams BUF, DEN, IND, SF, determine the average Yards on
# PlayType = PASS when Down = 3 in Quarter = 2.  Give your answer as a Series 
# with team identifiers for the index and average yards as the corresponding 
# values, sorted by value from largest to smallest.

BUF_pass_3_2 = only_BUF[(only_BUF['PlayType'] == 'PASS') & (only_BUF['Down'] == 3) & (only_BUF['Quarter'] == 2)]
DEN_pass_3_2 = only_DEN[(only_DEN['PlayType'] == 'PASS') & (only_DEN['Down'] == 3) & (only_DEN['Quarter'] == 2)]
IND_pass_3_2 = only_IND[(only_IND['PlayType'] == 'PASS') & (only_IND['Down'] == 3) & (only_IND['Quarter'] == 2)]
SF_pass_3_2 = only_SF[(only_SF['PlayType'] == 'PASS') & (only_SF['Down'] == 3) & (only_SF['Quarter'] == 2)]

average_yards_dict2 = {
    'BUF' : BUF_pass_3_2['Yards'].mean(),
    'DEN' : DEN_pass_3_2['Yards'].mean(),
    'IND' : IND_pass_3_2['Yards'].mean(),
    'SF' : SF_pass_3_2['Yards'].mean()
    }


q8 = pd.Series(data=average_yards_dict2).sort_values(ascending=False)


# Question 9  

# For each team (BUF, DEN, IND, SF) determine the proportion of plays on
# Down = 3 for which the ToGo value is less than the Yards value.  Give
# the proportions as a list in the order of the teams shown.

# filter for ToGo < Yards & Down = 3 & Team for numerator;
# filter for Down = 3 & Team for denominator;
# proportion is the quotient (do this for all 4 teams)

BUF_3_togo_less = only_BUF[(only_BUF['Down'] == 3) & (only_BUF['ToGo'] < only_BUF['Yards'])]
DEN_3_togo_less = only_DEN[(only_DEN['Down'] == 3) & (only_DEN['ToGo'] < only_DEN['Yards'])]
IND_3_togo_less = only_IND[(only_IND['Down'] == 3) & (only_IND['ToGo'] < only_IND['Yards'])]
SF_3_togo_less = only_SF[(only_SF['Down'] == 3) & (only_SF['ToGo'] < only_SF['Yards'])]


BUF_3 = only_BUF[only_BUF['Down'] == 3]
DEN_3 = only_DEN[only_DEN['Down'] == 3]
IND_3 = only_IND[only_IND['Down'] == 3]
SF_3 = only_SF[only_SF['Down'] == 3]

q9 = [len(BUF_3_togo_less)/len(BUF_3), len(DEN_3_togo_less)/len(DEN_3), len(IND_3_togo_less)/len(IND_3), len(SF_3_togo_less)/len(SF_3)]


#### Graphs

# The graphs in Questions 10-14 should be submitted under "Assignment 5 Graphs".
# Save each of your graphs as an individual PNG file, then submit each one
# separately under the corresponding question.  


## 10.  Generate a scatterplot of the variables 'Yards' (on the x-axis) vs.
##     'ToGo' (on the y-axis) for the SF offensive plays in the SF vs NYJ
##     game.  Your graph should match that given in Graph 10.

sns.relplot(data=only_SF, x = 'Yards', y = 'ToGo').set(xlabel='Yards gained', ylabel='Yards to go', title='SF vs NYJ')


## 11.  Generate a histogram of the values of the variable 'Yards' that are
##      no greater than 20 for the DEN offensive plays in the DEN vs NYJ game.  
##      Your graph should match that given in Graph 11.
only_DEN_lessthaneq20 = only_DEN[only_DEN['Yards'] <= 20]
sns.displot(data=only_DEN_lessthaneq20,x='Yards', binrange=[-3,21], binwidth=3).set(xlabel = 'Yards gained (<=20)', title='DEN vs NYJ', xticks=[-3,0,3,6,9,12,15,18,21])

## 12.  Generate side-by-side boxplots, one for each offensive team, of the
##      values of 'Yards' for plays classified as 'PASS' under 'PlayType'.
##      Your graph should match that given in Graph 12.


pass_playtype = nfl_data02[nfl_data02['PlayType'] == 'PASS']

sns.boxplot(data=pass_playtype,x='OffenseTeam', y='Yards', order=['BUF', 'DEN', 'IND', 'SF']).set(xlabel = 'Team on Offense', title = 'Distribution of yards gained by team')
## 13.  Generate a scatterplot of the variables 'Yards' (on the x-axis) vs.
##      'ToGo' (on the y-axis) from the offensive plays 'RUSH" (under 'PlayType') 
##      from the games involving SF and BUF.  Your graph should match that
##      given in Graph 13.

rush_SF_BUF = nfl_data02[(nfl_data02['PlayType'] == 'RUSH') & ((nfl_data02['OffenseTeam'] == 'SF') | (nfl_data02['OffenseTeam'] == 'BUF'))]
sns.relplot(data = rush_SF_BUF, x = 'Yards', y = 'ToGo', hue='OffenseTeam').set(xlabel = 'Yards gained', ylabel = 'Yards to go', title = 'Rushing Plays, BUF & SF')

## 14.  Generate side-by-side barplots, one for each team on offensive, that 
##      give the number of PASS and number of RUSH plays (both under 'PlayType').
##      (Each team will have two bars.)  Your graph should match that given in
##      Graph 14.
pass_rush = nfl_data02[(nfl_data02['PlayType'] == 'PASS') | (nfl_data02['PlayType'] == 'RUSH')]
sns.countplot(data=pass_rush, x='OffenseTeam', hue='PlayType', order=['BUF', 'DEN', 'IND', 'SF']).set(xlabel='Team on Offense', ylabel = 'Number of plays', title = 'Play type by team')




