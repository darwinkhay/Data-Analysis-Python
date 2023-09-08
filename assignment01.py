# Darwin Khay
# Wed Jan 18

# Assignment 01, STAT 3250

# Two *very* important rules that must be followed in order for your assignment
# to be graded correctly:

# a) The Python file name must be exactly "assignment00.py" with the correct two digit
# assignment number and without the quotes.
# b) The variables names like q1, q2, ... will be used to grade the assignment.
# They are initially set to `None` but you must set them equal to your final answer.
# If you don't know the answer, leave the variable as `None`.

# Notes:
# The autograder will run your python file in order to grade the q1, q2, ... variables.
# If your code throws an error, then the autograder will not be able to grade it, and
# you will receive a zero.
# Before you submit, run your entire file locally to make sure there are no errors.

# Question 1

# Assume that there are 365 days in a year and that a full week goes from Sunday to Saturday.
# Then in a given year some days will not be a part of a full week (at the start and end).
# What is the minimum number of such days?
# What is the maximum?

# Submit the answer as a list with the first element being the minimum and the second element
# being the maximum.

q1 = [1, 8]

# Question 2

# Create a sequence of numbers from -100 (inclusive) to 100 (inclusive) in increments of 2.
# The results should look like -100, -98, ..., 0, 2, 4, ..., 98, 100.
# Add the first 3 elements together.
# Add values for indices 13, 14, and 15.
# Add the last 3 elements together using negative indices.
# What is the product of the three sums?

sequence = range(-100,101,2)
add_first_three = sequence[0]+sequence[1]+sequence[2]
add_other = sequence[13]+sequence[14]+sequence[15]
add_last_three = sequence[-1]+sequence[-2]+sequence[-3]

q2 = add_first_three * add_other * add_last_three

# Question 3

# Save the following three different strings into three different variables.
# string 1: Adding
# string 2: strings
# string 3: together

# Concatenate the three strings to make a sentence that includes spaces and a period.
string1 = 'Adding'
string2 = 'strings'
string3 = 'together'
q3 = string1 + ' ' + string2 + ' ' + string3 + '.'

# Question 4

list01 = [2, 5, 4, 9, 10, -3, 5, 5, 3, -8, 0, 2, 3, 8, 5, 2, -3, 8, 7]
list02 = [-7, -3, 8, -5, -5, 2, 4, 9, 10, -7, 9, 10, 2, 13, -12, -4, 1, 3, 5]
list03 = [2, -5, 6, 0, 7, -2, -3, 5, 0, 2, 8, 7, 9, 2, 0, -2, 5, 5, 6]
list04 = [3, 5, -10, 2, 0, 4, -5, -7, 6, 2, 3, 3, 5, 12, -5, -9, -7, 4]

# Using the 4 lists above, concatenate them into one large list in the order they are initialized.
# With this large list starting from with the 3rd element, extract the sublist (slice)
# of every 5th element.
big_list = list01 + list02 + list03 + list04
q4 = big_list[2:-1:5]

# Question 5

# Create a set that is the set intersection of the 4 lists from problem 4.
# This should create a set where every element is contained in all 4 sets.
# Use the set.intersection() method as in the lecture notes.

q5 = set.intersection(set(list01),set(list02),set(list03),set(list04))

# Question 6

# Create a new empty list.
# Then use the list.append() method to add the 7th element of each list from question 4.
# You should append the values one at a time (4 calls to the list.append() method).
# Set q6 equal to this new list.
empty = []
empty.append(list01[6])
empty.append(list02[6])
empty.append(list03[6])
empty.append(list04[6])


q6 = empty

# Question 7

# Given a single string character, the ord() built-in function will return the character's Unicode
# integer code.
# Every string character maps to a unique integer.
# For example, the Unicode value of "j" is ord("j") which equals 106.

# For the first 5 letters of the alphabet, create a dictionary that maps the string to its
# Unicode integer value.
# Each key should be a string, and its corresponding value should be an integer.

q7 = {'a':ord('a'), 'b':ord('b'), 'c':ord('c'), 'd':ord('d'), 'e':ord('e')}

# Question 8

# Given the sentence below, use string methods to remove all punctuation and convert it into a
# list where each element is a word in ALL CAPS.
# For example, the sentence "Hello, world!" should become ["HELLO", "WORLD"]

winnie_the_pooh = "People say nothing is impossible, but I do nothing every day."
upper = winnie_the_pooh.upper()
temp1 = upper.split()
temp1[4] = "".join(temp1[4].split(','))
temp1[10] = "".join(temp1[10].split('.'))
q8 =temp1

# Question 9

# Using the big list from problem 4, slice the list to select only the odd indices excluding the last element.
# For example, big_list[0] is an even index and big_list[1] is an odd index.

q9 = big_list[1:-1:2]

# Question 10

# Remove duplicate entries from the list below.
# Submit the final answer as a list with the elements in any order.

my_list = [
    19,
    22,
    16,
    19,
    4,
    3,
    24,
    20,
    3,
    0,
    5,
    24,
    14,
    2,
    12,
    1,
    3,
    2,
    21,
    20,
    21,
    8,
    8,
    15,
    15,
    19,
    10,
    4,
    21,
    9,
    19,
    24,
    17,
    4,
    3,
    16,
    2,
    9,
    20,
    7,
]



q10 = list(set(my_list))
