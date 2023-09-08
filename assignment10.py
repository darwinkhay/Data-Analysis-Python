# Assignment 10, STAT 3250

# Two *very* important rules that must be followed in order for your assignment 
# to be graded correctly:

# 1. The Python file name must be exactly "assignment10.py" with the correct 
#    two digit assignment number and without the quotes.
# 2. The variables names like q1, q2, ... will be used to grade the assignment. 
#    They are initially set to `None` but you must set them equal to your final 
#    answer. If you don't know the answer, leave the variable as `None`.

# Notes:
# The autograder will run your python file in order to grade the q1, q2, ... variables.
# If your code throws an error, then the autograder will not be able to grade it, and
# you will receive a zero.
# Before you submit, run your entire file locally to make sure there are no errors.

#  For this assignment we revisit past men's NCAA basketball tournaments 
#  (including the glorious 2019 edition) using data from the file 
#
#      'ncaa.csv':  NCAA Men's Tournament Scores, 1985-201
#
#  The organization of the file is fairly clear.  Each record has information
#  about one game, including the year, the region, the teams, the final score, 
#  and each team's tournament seed.  

#  Two important points:
#    1) Each team is assigned a "seed" at the start of the tournament.  The
#       teams thought to be better are assigned smaller number seeds.  (So 
#       the best teams are assigned 1 and the worst assigned 16.)  In this 
#       assignment a "lower seed" refers to a worse team and hence larger 
#       seed number, with the opposite meaning for "higher seed". 
#    2) All questions refer only to the data in this in 'ncaa.csv' so you
#       don't need to worry about tournaments prior to 1985 or after 2019.

#  The data set is from Data.World, with the addition of the 2019
#  tournament provided by your dedicated instructors. 

import pandas as pd
ncaa = pd.read_csv('ncaa.csv')
# Question 1

# Find all schools that have lost the championship more than one time. Report 
# your results in a Series that has the schools as index and number of 
# championships lost for values, sorted alphabetically by school.
championships = ncaa[ncaa['Region Name'] == 'Championship']
championships['Team_loss'] = championships['Score'] < championships['Score.1']
championships['Team1_loss'] = championships['Score.1'] < championships['Score']
losers1 = championships.query('Team_loss == True')
losers2 = championships.query('Team1_loss == True')
losers1_count = losers1.groupby('Team')['Team_loss'].size()
losers2_count = losers2.groupby('Team.1')['Team1_loss'].size()
combined_losers_count = pd.concat([losers1_count, losers2_count], axis = 1)
combined_losers_count.fillna(0, inplace=True)
combined_losers_count['total_losses'] = combined_losers_count['Team_loss'] + combined_losers_count['Team1_loss']
more_than_one_time = combined_losers_count.query('total_losses > 1')
q1 = more_than_one_time['total_losses'].sort_index(ascending = True)



# Question 2

# Determine all schools that have progressed to the Sweet-16 of the tournament
# at least 15 times.  (The Sweet-16 is the 3rd round of the toournament.)
# Report your results as a Series with schools as index and number of times
# in the Sweet-16 as values, sorted by values from largest to smallest.
round_three_schools = ncaa.query('Round == 3')
team1_three_counts = round_three_schools.groupby('Team').size()
team2_three_counts = round_three_schools.groupby('Team.1').size()
combined_round_three_schools = pd.concat([team1_three_counts, team2_three_counts], axis = 1)
combined_round_three_schools.fillna(0, inplace=True)
combined_round_three_schools['total_games'] = combined_round_three_schools[0] + combined_round_three_schools[1]
only_at_least_15 = combined_round_three_schools.query('total_games >= 15')
q2 = only_at_least_15['total_games'].sort_values(ascending = False)


# Question 3

# Find all years when the school that won the tournament was seeded 
# 3 or lower. (Remember that "lower" seed means a bigger number!) Give  
# a DataFrame with years as index and corresponding school and seed
# as columns (from left to right).  Sort by year from least to most recent.

team1_seed3 = championships[championships['Seed'] >= 3]
team2_seed3 = championships[championships['Seed.1'] >= 3]

team1_seed3['Team_win'] = team1_seed3['Score'] > team1_seed3['Score.1']
team2_seed3['Team1_win'] = team2_seed3['Score.1'] > team2_seed3['Score']

team1_seed3 = team1_seed3.query('Team_win == True')
team2_seed3 = team2_seed3.query('Team1_win == True')

team1_seed3_winners = pd.DataFrame()
team1_seed3_winners['Team'] = team1_seed3['Team']
team1_seed3_winners['Seed'] = team1_seed3['Seed']
team1_seed3_winners.index = team1_seed3['Year']


team2_seed3_winners = pd.DataFrame()
team2_seed3_winners['Team'] = team2_seed3['Team.1']
team2_seed3_winners['Seed'] = team2_seed3['Seed.1']
team2_seed3_winners.index = team2_seed3['Year']





all_winners = pd.concat([team1_seed3_winners, team2_seed3_winners], axis = 0)

q3 = all_winners.sort_index(ascending = True)


# Question 4

# Determine the average tournament seed for each school.  Make a Series
# of all schools that have an average seed of 5.0 or higher (that is,
# the average seed number is <= 5.0).  The Series should have schools
# as index and average seeds as values, sorted alphabetically by
# school

team_seed1 = ncaa['Seed'].groupby([ncaa['Year'], ncaa['Team']]).first().reset_index()
team_seed2 = ncaa['Seed.1'].groupby([ncaa['Year'], ncaa['Team.1']]).first().reset_index()


team_seeds = pd.DataFrame()
team_seeds['Year'] = team_seed1['Year'].append(team_seed2['Year'], ignore_index=True)
team_seeds['Team'] = team_seed1['Team'].append(team_seed2['Team.1'], ignore_index=True)
team_seeds['Seed'] = team_seed1['Seed'].append(team_seed2['Seed.1'], ignore_index=True)
team_seeds = team_seeds.drop_duplicates()


avg_seed_school = team_seeds['Seed'].groupby(team_seeds['Team']).mean().reset_index()
less_than_five = avg_seed_school[avg_seed_school['Seed'] <= 5.0]

q4 = less_than_five.groupby('Team')['Seed'].first().sort_index(ascending = True)


# Question 5

# For each tournament round, determine the percentage of wins by the
# higher seeded team. (Ignore games of teams with the same seed.)
# Give a Series with round number as index and percentage of wins
# by higher seed as values sorted by round in order 1, 2, ..., 6. 
# (Remember, a higher seed means a lower seed number.)
rounds_count = ncaa.groupby('Round').size()
ncaa['win_higher_seed'] = ((ncaa['Seed'] < ncaa['Seed.1']) & (ncaa['Score'] > ncaa['Score.1'])) | ((ncaa['Seed.1'] < ncaa['Seed']) & (ncaa['Score.1'] > ncaa['Score']))

only_higher_seed_wins = ncaa.query('win_higher_seed == True') 

rounds_win_count = only_higher_seed_wins.groupby('Round').size()


q5 = ((rounds_win_count/rounds_count)*100)


# Question 6

# For each seed 1, 2, 3, ..., 16, determine the average number of games
# won per tournament by a team with that seed.  Give a Series with seed 
# number as index and average number of wins as values, sorted by seed 
# number 1, 2, 3, ..., 16. (Hint: There are 35 tournaments in the data set
# and each tournament starts with 4 teams of each seed.  We are not 
# including "play-in" games which are not part of the data set.)


seed_games = ncaa.groupby('Seed').size()
seed1_games = ncaa.groupby('Seed.1').size()
total_seed_games = pd.concat([seed_games, seed1_games], axis = 1)
total_seed_games['total_seed_games'] = total_seed_games[0] + total_seed_games[1]
total_seed_games = total_seed_games['total_seed_games'] # ****
 # _____
 
ncaa['Team_loss'] = ncaa['Score'] < ncaa['Score.1']
ncaa['Team1_loss'] = ncaa['Score.1'] < ncaa['Score']

team1_seed_winners = ncaa.query('Team1_loss == True')
team2_seed_winners = ncaa.query('Team_loss == True')

avg_team1_seed_winners = team1_seed_winners.groupby('Seed').size()

avg_team2_seed_winners = team2_seed_winners.groupby('Seed.1').size()

avg_team_seed_winners = pd.concat([avg_team1_seed_winners, avg_team2_seed_winners], axis = 1)
avg_team_seed_winners.fillna(0, inplace=True)
avg_team_seed_winners['total_seed_winners'] = avg_team_seed_winners[0] + avg_team_seed_winners[1]
avg_team_seed_winners = avg_team_seed_winners['total_seed_winners'] # ****


q6 = (avg_team_seed_winners/total_seed_games).sort_index(ascending = True)


# Question 7

# Are some schools particularly good at winning games as a lower seed?  For
# each team, determine the percentage of games won by that team when that team 
# was a lower seed than their opponent.  Give a Series of all schools that have 
# won more than 60% of their games while the lower seed, with school as index
# and percentage of victories as values, sorted by percentage from greatest 
# to least.
team1_seed_winners['lower_seed_wins'] = team1_seed_winners['Seed'] > team1_seed_winners['Seed.1']
team2_seed_winners['lower_seed_wins'] = team2_seed_winners['Seed.1']  > team2_seed_winners['Seed']
team1_seed_winners_lower = team1_seed_winners.query('lower_seed_wins == True')
team2_seed_winners_lower = team2_seed_winners.query('lower_seed_wins == True')

team1_lower_wins_schools = team1_seed_winners_lower.groupby('Team').size()
team2_lower_wins_schools = team2_seed_winners_lower.groupby('Team.1').size()

total_school_lower_wins = pd.concat([team1_lower_wins_schools, team2_lower_wins_schools], axis = 0)
total_school_lower_wins = total_school_lower_wins.groupby(level=0).sum()
#total_school_lower_wins.fillna(0, inplace=True)
#total_school_lower_wins['total_wins'] = total_school_lower_wins[0] + total_school_lower_wins[1]
#total_school_lower_wins = total_school_lower_wins['total_wins']
# _____
team1_school_winners = team1_seed_winners.groupby('Team').size()
team2_school_winners = team2_seed_winners.groupby('Team.1').size()

total_school_winners = pd.concat([team1_school_winners, team2_school_winners], axis = 0)
total_school_winners = total_school_winners.groupby(level=0).sum()
#total_school_winners.fillna(0, inplace=True)
#total_school_winners['total_school_wins'] = total_school_winners[0] + total_school_winners[1]
#total_school_winners = total_school_winners['total_school_wins']
# _____
proportion_lower_seed_wins = total_school_lower_wins/total_school_winners
proportion_lower_seed_wins.fillna(0, inplace=True)
percent_lower_seed_wins = proportion_lower_seed_wins*100

q7 = percent_lower_seed_wins[percent_lower_seed_wins > 60].sort_values(ascending = False)


# Question 8

# Is there a region that consistently has the closest games?  For each year,
# determine which region has the lowest average point differential (winning 
# minus losing score), ignoring the games in 'Final Four' and 'Championship'.
# Give you answer as a data frame, with year as index, a column with the
# name of the region that has the lowest average, and a column with the average
# (in that order). Note that the names of the four regions are not always the
# same.

ncaa['point_differential'] = abs(ncaa['Score'] - ncaa['Score.1'])
year_avg_point_diff = ncaa.groupby('Year')['point_differential'].mean()
point_diff_year_region = ncaa.groupby(['Year', 'Region Name'])['point_differential'].mean()
no_champs = point_diff_year_region.loc[point_diff_year_region.index.get_level_values('Region Name') != 'Championship']
no_final_four = no_champs.loc[no_champs.index.get_level_values('Region Name') != 'Final Four']

avg_point_diff = pd.DataFrame(no_final_four).reset_index()
point_diff_indices = avg_point_diff.groupby('Year')['point_differential'].idxmin()
region_names_pd = avg_point_diff.loc[point_diff_indices, 'Region Name']
years_pd = avg_point_diff.loc[point_diff_indices, 'Year']
point_diff_pd = avg_point_diff.loc[point_diff_indices, 'point_differential']

avg_point_diff_region = pd.DataFrame()
avg_point_diff_region['Year'] = years_pd
avg_point_diff_region['Region Name'] = region_names_pd
avg_point_diff_region['point_differential'] = point_diff_pd
avg_point_diff_region = avg_point_diff_region.set_index('Year')
q8 = avg_point_diff_region


# Question 9

# For each year's champion, determine their average margin of victory 
# across all of their games in that year's tournament. Find the champions
# that have an average margin of victory of no more than 10. Give a DataFrame 
# with year as index and champion and average margin of victory as columns
# (from left to right), sorted by from lowest to highest average victory 
# margin.
championships = ncaa[ncaa['Region Name'] == 'Championship']


championship_winners_1 = championships.query('Team1_loss == True')
championship_winners_1 = championship_winners_1[['Team', 'Year']]

championship_winners_2 = championships.query('Team_loss == True')
championship_winners_2 = championship_winners_2[['Team.1', 'Year']]
championship_winners_2 = championship_winners_2.rename(columns={'Team.1' : 'Team'})
championship_winners = pd.concat([championship_winners_1, championship_winners_2], axis = 0)
exact_champions = set(championship_winners[['Year', 'Team']].apply(tuple, axis=1))

# ______

only_champions = ncaa[ncaa['Team'].isin(championship_winners['Team']) | ncaa['Team.1'].isin(championship_winners['Team'])]
only_champions['margin_of_victory'] = abs(only_champions['Score'] - only_champions['Score.1'])
only_champions_1 = only_champions[only_champions[['Year', 'Team']].apply(tuple, axis=1).isin(exact_champions)] 
only_champions_2 = only_champions[only_champions[['Year', 'Team.1']].apply(tuple, axis=1).isin(exact_champions)]


all_champion_team_games = pd.concat([only_champions_1, only_champions_2], axis = 0)

winning_team1 = all_champion_team_games.query('Team_loss == True')
winning_team1['winning_team'] = winning_team1['Team.1']

winning_team2 = all_champion_team_games.query('Team1_loss == True')
winning_team2['winning_team'] = winning_team2['Team']

winning_teams = pd.concat([winning_team1, winning_team2], axis = 0)
#______


avg_margin_of_victory_team = winning_teams.groupby(['winning_team', 'Year'])['margin_of_victory'].mean()
avg_margin_of_victory_team = pd.DataFrame(avg_margin_of_victory_team).reset_index()
avg_margin_of_victory_team = avg_margin_of_victory_team.set_index('Year')

no_more_than_10 = avg_margin_of_victory_team.query('margin_of_victory <= 10')


q9 = no_more_than_10.sort_values('margin_of_victory')

    
# Question 10

# Determine the 2019 champion.  Use code to extract the correct school,
# not your knowledge of college backetball history.

only_2019_championship = ncaa[(ncaa['Year'] == 2019) & (ncaa['Region Name'] == 'Championship')]
champion_2019_1 = only_2019_championship.query('Team_loss == True')
champion_2019_1['winning_team'] = champion_2019_1['Team.1']
champion_2019_2 = only_2019_championship.query('Team1_loss == True')
champion_2019_2['winning_team'] = champion_2019_2['Team']
overall_champ = pd.concat([champion_2019_1, champion_2019_2], axis = 0)
q10 = str(overall_champ['winning_team'].iloc[0])

