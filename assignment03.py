# Assignment 03, STAT 3250

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

# You should not use a for loop for any of these problems!

import numpy as np
import pandas as pd

# Question 1

# Using the numpy library create a 1d array of integers from 0 to 10000 (exclusive).
# Raise each element to the power of 3.
# Find the sum of the numbers that are evenly divisible by 7.

temp_array = np.arange(0,10000)
power_three = temp_array**3
divisible_by_7 = power_three[power_three%7 == 0]

q1 = np.sum(divisible_by_7)

# Question 2

# Say we want to find the total population of a city.
# The city can be divided into an m x n grid of neighborhoods where each neighborhood has a
# certain number of buildings.
# Conveniently due to zoning laws, all buildings within a neighborhood must have the same number of people.

# In the data, a column of buildings per neighborhood is followed by a column of people per building.
# For example:

toy_city_data = np.array([[11, 3, 8, 4], [7, 2, 15, 1]])

# The toy city above is a 2 x 2 city.
# The buildings per neighborhood matrix looks like

buildings = np.array([[11, 8], [7, 15]])

# The people per buildng looks like

people_per_building = np.array([[3, 4], [2, 1]])

# Then the total population of the city is:
# 11*3 + 8*4 + 7*2 + 15*1
# Find the population of the city from the `city_data` variable below.

city_data = np.array(
    [
        [30, 2, 3, 8, 41, 5, 29, 8, 22, 1, 22, 1, 47, 2],
        [37, 4, 29, 4, 4, 3, 39, 3, 26, 8, 23, 4, 6, 4],
        [25, 2, 29, 2, 3, 5, 15, 5, 33, 3, 39, 8, 24, 6],
        [4, 9, 8, 8, 6, 4, 2, 9, 11, 1, 22, 6, 35, 9],
        [10, 4, 32, 9, 10, 7, 25, 3, 33, 7, 16, 9, 24, 2],
        [49, 6, 47, 9, 37, 3, 33, 8, 43, 5, 31, 2, 5, 3],
        [40, 2, 41, 8, 12, 3, 22, 7, 31, 7, 8, 5, 44, 2],
        [3, 9, 39, 8, 39, 9, 33, 3, 33, 4, 23, 8, 9, 2],
        [47, 3, 21, 1, 3, 3, 28, 4, 39, 1, 21, 2, 37, 4],
        [11, 1, 35, 6, 1, 1, 46, 3, 12, 4, 36, 6, 30, 5],
    ]
)
num_buildings = city_data[:, 0::2] # gets only the even indices starting from 0 (step is 2)
num_people = city_data[:, 1::2] # gets only the odd indices starting from 1 (step is 2)
population_each_neighborhood = num_buildings * num_people

q2 = population_each_neighborhood.sum()

# Question 3

# From the city data, how many people live in neighborhoods that have an odd number of buildings?
only_odd = np.where(num_buildings%2 != 0, num_buildings, 0)
population_odd_buildings = only_odd * num_people

q3 = population_odd_buildings.sum()

# Question 4

# The following data is the average daily temperature over a period of 10 weeks.
# Create a Pandas series using the data with the default index and the name `daily_temps`.

temps = [
    84,
    46,
    81,
    54,
    21,
    70,
    16,
    60,
    64,
    20,
    26,
    66,
    49,
    78,
    65,
    51,
    85,
    64,
    72,
    74,
    89,
    72,
    16,
    85,
    71,
    66,
    15,
    24,
    22,
    59,
    49,
    49,
    50,
    69,
    73,
    89,
    78,
    69,
    82,
    64,
    87,
    89,
    71,
    66,
    78,
    21,
    59,
    66,
    81,
    73,
    64,
    75,
    58,
    68,
    63,
    56,
    76,
    62,
    67,
    59,
    62,
    75,
    68,
    72,
    64,
    69,
    16,
    60,
    61,
    71,
]

# However, it turns out that there are problems with the data.
# On some days, the temperature was measured in Celsius instead of Fahrenheit.
# When this happened, the temperature was recorded to be lower than 30 degrees.
# The temperature never went below 30 degrees Fahrenheit otherwise.
# Change the Celsius values back to Fahrenheit values using the equation.
# F = C * 9/5 + 32

# Then convert the Pandas series to a series of strings so that each row is `"TEMP F"`, where TEMP is the integer temperature in Fahrenheit.
# For example, the first row should be `"84 F"`

daily_temps = pd.Series(data=temps, name='daily_temps')
daily_temps.loc[daily_temps < 30] = daily_temps * 9/5 + 32
int_series = daily_temps.astype(int)
string_series = int_series.astype(str) + ' F'
q4 = string_series

# Question 5

# Consider the long string below.
# Convert it into a pandas series where each row contains one character of the string.
# Without using a for loop, count how many vowels appear in the series.

sentences = "The Pandas library is a powerful data analysis and manipulation tool. It makes working with tabular data very easy and provides similar functionality Dataframes in R. The two most important data structures in Pandas are the Pandas Series and Pandas DataFrame."
sentences_series = pd.Series(data=list(sentences))
vowels = ['a','e','i','o','u', 'A', 'E', 'I', 'O', 'U']
only_vowels = sentences_series[sentences_series.isin(vowels)]

q5 = only_vowels.count()

# Question 6

# The dataframe below shows the homework grades for 30 students where each student is one row and the index is the student id.
# Create a new column called "mean" that calculates the mean grade for each student.
# Find the ids of students that had a mean grade of an A or better. (greater than or equal to 90).
# Submit the ids as a list sorted in ascending order.
# Do not use a for loop.

grades = pd.DataFrame(
    {
        "hw1": [
            85,
            92,
            77,
            96,
            81,
            69,
            102,
            86,
            90,
            86,
            90,
            77,
            97,
            78,
            74,
            98,
            76,
            91,
            84,
            67,
            96,
            67,
            75,
            84,
            81,
            87,
            89,
            77,
            83,
            89,
        ],
        "hw2": [
            99,
            96,
            85,
            95,
            89,
            85,
            88,
            87,
            76,
            71,
            76,
            86,
            82,
            81,
            85,
            77,
            87,
            84,
            84,
            106,
            90,
            87,
            85,
            75,
            87,
            75,
            93,
            83,
            91,
            72,
        ],
        "hw3": [
            99,
            85,
            91,
            81,
            81,
            83,
            84,
            73,
            92,
            79,
            65,
            93,
            93,
            97,
            84,
            87,
            89,
            111,
            102,
            84,
            87,
            72,
            84,
            82,
            91,
            78,
            71,
            97,
            78,
            78,
        ],
    },
    index=[
        40974,
        83633,
        61948,
        15127,
        48775,
        28586,
        89789,
        89694,
        28268,
        14087,
        77936,
        88955,
        48789,
        13526,
        62940,
        76420,
        91036,
        94822,
        27722,
        40631,
        98282,
        23297,
        60682,
        35104,
        83790,
        93414,
        91328,
        40094,
        42009,
        54895,
    ],
)
grades['mean'] = (grades['hw1'] + grades['hw2'] + grades['hw3'])/3
a_or_better = grades[grades['mean'] >= 90]
top_students = list(a_or_better.index)
top_students.sort()
q6 = top_students

# Question 7

# Some students from problem 6 turned in extra credit.
# The result was that all the students who had a mean score of less than 80
# received extra credit that boosted them to an 80.
# No other students submitted extra credit.

# Create a new column called `"extra_credit"` with a value of 0.
# Then, for the students whose mean was less than 80, change their extra credit value
# so that the extra credit + mean value is equal to 80.
# Submit the extra_credit column as a pandas series.

# Hint: when changing values on slices, be sure to use `.loc[]`.
# To start, consider creating a mask variable that tells you which rows you want to add extra credit to.

grades['extra_credit'] = 0
mask = grades['mean'] < 80
grades.loc[mask, 'extra_credit'] = 80 - grades.loc[mask]['mean']

q7 = grades['extra_credit']

# Question 8

# Read in the `hotel_reservations.csv` file into a dataframe.
# The first few rows are descriptive text and should not be included in the dataframe.

# Do reservations with children usually require parking spots more often than those without children?
# Calculate the absolute mean difference in the `required_car_parking_space` variable between the two groups.
hotel_reservations = pd.read_csv('hotel_reservations.csv', skiprows=26)
with_children = hotel_reservations[hotel_reservations['no_of_children'] > 0]
without_children = hotel_reservations[hotel_reservations['no_of_children'] == 0]


q8 = abs(with_children['required_car_parking_space'].mean()-without_children['required_car_parking_space'].mean())


# Question 9

# For reservations with "Meal Plan 1" and lead times greater than 100, what is the median total nights?
meal_plan_1 = hotel_reservations[hotel_reservations['type_of_meal_plan'] == 'Meal Plan 1']
lead_time_more_than_100 = meal_plan_1[meal_plan_1['lead_time']>100]
total_nights = lead_time_more_than_100['no_of_weekend_nights'] + lead_time_more_than_100['no_of_week_nights']

q9 = total_nights.median()

# Question 10

# What is the total monetary value of cancelled reservations during the summer of 2018.
# Summer was from June 21st to Sept 22nd (inclusive).
only_2018 = hotel_reservations[hotel_reservations['arrival_year']==2018]
only_summer_2018 = only_2018.loc[
                                 (only_2018['arrival_month']==6) & (only_2018['arrival_date'] >= 21) |
                                 (only_2018['arrival_month']==9) & (only_2018['arrival_date']<=22) |
                                 (only_2018['arrival_month']> 6) & (only_2018['arrival_month'] < 9)
                                 
                                 
                                 ]
cancelled = only_summer_2018[only_summer_2018['booking_status'] == 'Canceled']
total_nights_cancelled = cancelled['no_of_weekend_nights'] + cancelled['no_of_week_nights']

total_cost = (cancelled['avg_price_per_room']*total_nights_cancelled).sum()

q10 = total_cost
