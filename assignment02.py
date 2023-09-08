# Assignment 02, STAT 3250

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

# read and writing files
# if/then, loops, functions
# classes

# Question 1

my_list = [1, 2, -3, 4, 3, 2, -1, 2, 3, 2, 1, -2, 1]

# Using a for loop, find the sum of the numbers in my_list.
sum = 0
for i in my_list:
    sum += i

q1 = sum

# Question 2

# Using a for loop, find the sum of the positive numbers in my_list.

positive_sum = 0
for j in my_list:
    if j > 0:
        positive_sum += j
q2 = positive_sum

# Question 3

my_strings = [
    "zo78_",
    "4_sg",
    "o92r_",
    "_3fwji_",
    "zulbijo1",
    "46_4k0",
    "_3d_dw_7vh2_",
    "d1r746_",
]

# Using a for loop, create a list that contains the length of each string in my_strings.
# For example, the first element should be 5 and the second should be 4.

list_of_lengths = []
for i in my_strings:
    list_of_lengths.append(len(i))
q3 = list_of_lengths

# Question 4

# It turns out the trailing underscores (underscores at the end only) in my_strings were a typo.
# Create a new list from my_strings that removes all the trailing underscores.
# Do not remove underscores that are not trailing.
# Hint: the str.removesuffix() method may be useful.
new_list = []
for string in my_strings:
    new_list.append(string.removesuffix('_'))
q4 = new_list

# Question 5

# The "gibberish.txt" file contains a string on each line.
# Read the file into a list so that each string is an element in the list.
# The "\n" characters at the end of a string stand for a newline and should NOT be
# a part of the string.
# Remove the newline characters from any string that contains them.
# Submit the list of the strings with the newlines removed.

read_list =  []
with open("gibberish.txt") as f:
    read_list = f.readlines()
    
for i in range(len(read_list)):
    read_list[i] = read_list[i].removesuffix('\n')

q5 = read_list

# Question 6

# What is the length of the line with the longest string in the "gibberish.txt" file?

max_length = 0
for string in read_list:
    if len(string) > max_length:
        max_length = len(string)

q6 = max_length

# Question 7

# Say you send out a survey to a group of people using their emails.
# Some respond to the survey, but some do not.
# The "survey_recipients.txt" file contains the emails of all the people who received the survey.
# The "survey_respondents.txt" file contains the emails of those who responded to the survey.
# Find the set of people that did not respond to the survey (so you can bug them to respond).
# Hint: Check https://docs.python.org/3/library/stdtypes.html#set for a list of set operations.


with open("survey_recipients.txt") as f:
    recipients_list = f.readlines()

with open("survey_respondents.txt") as f:
    respondents_list = f.readlines()

for i in range(len(recipients_list)):
    recipients_list[i] = recipients_list[i].removesuffix('\n')
for i in range(len(respondents_list)):
    respondents_list[i] = respondents_list[i].removesuffix('\n')
recipients_set = set(recipients_list)
respondents_set = set(respondents_list)

    
    
    
final_set = recipients_set.difference(respondents_set)
q7 = final_set

# Question 8

# Loop through the numbers from -99 (inclusive) to 3250 (exclusive) in increments of 13.
# For example -99, -86, -73, ...
# The score starts from 0.
# If the number is evenly divisible by 3 the score increases by 3
# If the number is evenly divisible by 4 the score decreases by 2
# If the number is evenly divisible by both 3 and 4 then the score is increased
# by the number itself.
# What is the final score?
final_score = 0
for i in range(-99, 3250, 13):
    if i%3 == 0 and i%4 == 0:
        final_score += i
    elif i%4 == 0:
        final_score -= 2
    elif i%3 == 0:
        final_score += 3
    
        

q8 = final_score

# Question 9

# What is the difference between Python functions and methods and how are methods typically used?
# Answer the question as a single string using complete sentences.
q9 = "Methods are functions that belong to a class and modify the attributes of that class, and a function is just an independent Python object that takes in inputs and returns outputs. To use a method, it is invoked by using dot syntax."


# Question 10

# Consider a board game similar to Go where 2 players place stones on an n x n grid.
# In this game, the final score of each player is determined by layout on the grid at the end of the game.
# For each row, a player adds the number of their pieces on the row to their score.
# However, if a row has an odd number of empty spots, player 1 loses 1 point.
# If a row has an even number of empty spots, player 2 loses 1 point.
# The player with the higher score wins.
# We can represent the grid as n lists with n elements each (similar to a matrix) where a 1
# means player 1's stone was on that spot and 2 means player 2's stone was on that spot.
# A 0 would mean no stone was on that spot.
# Given the board state represented as a list of lists, calculate the score of the winner.

# For example, on this toy board

toy_board = [
    [1, 1, 1, 0],  # row 1
    [0, 2, 0, 1],  # row 2
    [2, 0, 2, 1],  # row 3
    [1, 0, 2, 1]   # row 4
]

# We see that player 1 has (2+1+0+1)=4 points while player 2 has (0+0+2+1)=3 points.
# The actual board state is stored as a string in the "board_state.txt" file, where each line represents a row on the grid.
# Calculate the score of the winner.
# First, try converting the file from a string into a list of lists of integers (like toy_board).
# But if after a while you are still stuck you can copy and paste the data and add 
# brackets to turn it into one.

with open("board_state.txt") as f:
    board = f.read()
board
board_list = []
row = []


for i in range(len(board)):
    if board[i].isdigit():
        row.append(int(board[i]))
        if i == len(board)-1:
            board_list.append(row)
            row = []
    elif board[i] == '\n':
        board_list.append(row)
        row = []
        
player1_score = 0
player2_score = 0
num_zeros = 0
for i in range(len(board_list)):
    for j in range(len(board_list[i])):
        if board_list[i][j] == 1:
            player1_score += 1
            if j == len(board_list[i])-1:
                if num_zeros%2 == 0:
                    player2_score -= 1
                    num_zeros = 0
                else:
                    player1_score -= 1
                    num_zeros = 0
        elif board_list[i][j]  == 2:
            player2_score += 1
            if j == len(board_list[i])-1:
                if num_zeros%2 == 0:
                    player2_score -= 1
                    num_zeros = 0
                else:
                    player1_score -= 1
                    num_zeros = 0
        elif board_list[i][j]  == 0:
            num_zeros += 1
            if j == len(board_list[i])-1:
                if num_zeros%2 == 0:
                    player2_score -= 1
                    num_zeros = 0
                else:
                    player1_score -= 1
                    num_zeros = 0
        
                

q10 = max(player1_score, player2_score)