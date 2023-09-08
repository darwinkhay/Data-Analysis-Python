# Assignment 13 STAT 3250

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

# The datasets contain info on the prices of used cars in the UK.


# Preprocessing

# The `car-data` directory must be in the current working directory (most likely in the same spot as
# the `assignment13.py` file).
# 1. Read in all the datasets and combine them into one large dataset.
# 2. Rename the `tax(£)` column to be `tax` so it all aligns.
# 3. Include a column called `make` which should be the car's make (file name without suffix).
from pathlib import Path
from sklearn.model_selection import train_test_split
import pandas as pd
import statsmodels.formula.api as smf
import statsmodels.api as sm
from sklearn import linear_model

all_cars_list = []
all_cars_brands_list = []
cars_path = Path.cwd() /"car-data"

for i in cars_path.iterdir():
    if i.is_file():
        file_name = i.name.replace('.csv', '')
        all_cars_brands_list.append(file_name)

    temp = pd.read_csv(i)
    
    temp['make'] = file_name
    temp = temp.rename(columns={'tax(£)': 'tax'})
    all_cars_list.append(temp)

all_cars = pd.concat(all_cars_list)
# Question 1

# Let's do some cleaning!
# * Drop the rows that contain `NaN` values.
# * Filter out cars that were built after 2023.
# * Remove any leading/trailing whitespace on the string columns
# * Convert the 4 string columns to categorical unordered columns.
# * Sort the *columns* in ascending order

# Sort the cleaned dataframe by the values of `make`, `model`, `price`, and `mileage` in that order
# in ascending order and submit the first 100 rows.

all_cars = all_cars.dropna()
all_cars = all_cars.query('year <= 2023')
all_cars = all_cars.applymap(lambda x: x.strip() if isinstance(x, str) else x)
category_mem = all_cars['model'].memory_usage() + all_cars['transmission'].memory_usage() + all_cars['fuelType'].memory_usage() + all_cars['make'].memory_usage()

all_cars2 = all_cars
all_cars2['model'] = all_cars['model'].astype('category')
all_cars2['transmission'] = all_cars['transmission'].astype('category')
all_cars2['fuelType'] = all_cars['fuelType'].astype('category')
all_cars2['make'] = all_cars['make'].astype('category')
all_cars2 = all_cars2.sort_values(by=['make', 'model', 'price', 'mileage'])
string_mem = all_cars2['model'].memory_usage() + all_cars2['transmission'].memory_usage() + all_cars2['fuelType'].memory_usage() + all_cars2['make'].memory_usage()

cars_100 = all_cars2[:100]
q1 = cars_100


# Question 2

# How much memory usage was saved by converting the string columns to categorical ones in kilobytes
# (kb) (base 10)?



q2 = abs(string_mem - category_mem)/1000


# Question 3

# For each `make`, what is the average car price?
# Submit a Series where the index is the car make and the values are the mean price in ascending
# order.

avg_car_price_make = all_cars2.groupby('make')['price'].mean()
q3 = avg_car_price_make.sort_values(ascending = True)


# Question 4

# A bit more cleaning...
# We don't want to use car models that only have a very few data points.
# Filter out models that had less than 10 data points and be sure to remove those unused categories
# as well.
model_counts = all_cars2.groupby('model').count()
filtered = model_counts[model_counts >= 10].dropna()
keep = list(filtered.index)
all_cars3 = all_cars2[all_cars2['model'].isin(keep)]


# Submit a Series of the counts for each model for all models that had at least 10 occurrences in
# descending order with the model as the index.
# Be sure to filter out models who had less than 10 data points before moving on to question 5.
model_counts_series = all_cars3.groupby('model').size().sort_values(ascending = False)
model_counts_series = model_counts_series[model_counts_series >= 10]
q4 = model_counts_series


# Question 5

# Now before we do any more analysis (we probably could have done this at the very beginning), let's
# split the data after question 4 into a training and test set.
# This is important to prevent test data leakage.
# Use the `train_test_split` function with `random_state=1` to select 90% of the data to be in the
# training set.
# The remaining rows should be in the test set.

# For each car model, find the proportion of values that ended up in the training set.
# Submit a Series with the model as the index and the values as the proportion that ended up in the
# training set sorted by index ascending.

# The resulting train and test set will be used for the other problems.
train_df, test_df = train_test_split(all_cars3, test_size=0.1, random_state=1)

all_cars3_model_counts = all_cars3.groupby('model').size()
train_df_model_counts = train_df.groupby('model').size()
q5 = ((train_df_model_counts/all_cars3_model_counts)).sort_index(ascending = True).dropna()


# Question 6

# Let's train a model using the statsmodels formula api.
# Create an Ordinary Least Squares model to predict the `price` based on `transmission`, `mileage`,
# `make`, and `mpg` (with an intercept).
# Remember to use only the training set to fit the model.
# Do not change the names of the columns.

# Submit a Series with the parameter names as the index and the parameter estimates as the values
# sorted by index.
# Note how the categorical variables are automatically converted to be one hot encoded (indicator
# variables).
results = smf.ols("price ~ transmission + mileage + make + mpg", data=train_df).fit()

q6 = results.params.sort_index(ascending = True)


# Question 7

# Next, let's train a Lasso model using statsmodels *without* formulas.
# Fit a Lasso Regression model with `price` as the response and `transmission`, `mileage`, `make`,
# `mpg`, and `model` as the predictors.
# Using the training set, you will need to create dummy variables for the categorical columns
# (including dropping the first category).
# Do not change the names of the columns.
# You will also need to add a constant.
# Use `alpha=15` for fitting the Lasso regression.
# Submit a Series with the parameter names as the index and the parameter estimates as the values
# sorted by index

# *Note: Since `model` contains many categories, this will results in a large number of dummy
# columns.
# Lasso regresssion can be useful way to select a fewer number of columns that have a large effect
# on the response (variable selection) and to deal with multicollinearity.*
y = train_df["price"]
X = train_df[["transmission", "mileage", "make", "mpg", "model"]]
X = pd.get_dummies(X, drop_first=True)
X = sm.add_constant(X)  # add an intercept

results_lasso = sm.OLS(y, X)
results_lasso = results_lasso.fit_regularized(alpha=15, L1_wt=1)

results_lasso_params = results_lasso.params.sort_index(ascending = True)
#results_lasso_params = results_lasso_params[results_lasso_params != 0].dropna()
q7 = results_lasso_params


# Question 8

# Use scikit-learn to fit a Linear Regression model that predicts the car price based on the
# numerical variables `engineSize`, `mileage`, `mpg`, `tax`, and `year` (make the columns in that
# order).
# Again use only the train set for fitting the model.

# Submit a Series where the index is the parameter name (column name) and the values are the
# parameter coefficients (do not include the intercept) sorted by index.
ols_model = linear_model.LinearRegression()
y_2 = train_df['price']
X_2 = train_df[['engineSize', 'mileage', 'mpg', 'tax', 'year']]
ols_model.fit(X=X_2, y=y_2)
param_coef = {'engineSize' : ols_model.coef_[0], 'mileage' : ols_model.coef_[1], 'mg' : ols_model.coef_[2], 'tax' : ols_model.coef_[3], 'year' : ols_model.coef_[4]}
q8 = pd.Series(param_coef).sort_index(ascending = True)


# Question 9

# Train a scikit-learn Lasso Regression model with `alpha=1` and `max_iter=2000` on the training
# data using `transmission`, `fuelType`, `tax`, and `mpg` as predictors and `price` as the response.
# Use `OneHotEncoding` on the categorical variables (no dropping) and standardize the numerical
# variables using `StandardScalar`.
# Also, if using the `ColumnTransformer` (recommended), set `verbose_feature_names_out=False` to
# make the column names more readable.
# Make sure to wrap the data transformations and Lasso Regression estimator into a pipeline so we
# can easily make predictions on the test data.

# Calculate the residuals on the **test data set**.
# Submit a Series where the index matches the test set's index and the values are the corresponding
# residuals.


q9 = pd.Series()


# Question 10

# When we fit a Linear Regression model on some data, we get back point estimates of the parameter
# values - one value per parameter.
# But sometimes we want to know more than just the point estimates, we may want to know the
# distribution of the parameters or even the distribution of a function of the parameters.
# If the parameter of interest is *nice* we might be able to pull out some theory to find
# approximate distributions, but this may not be feasible for some parameters of interest.

# Another option is to use some resampling techniques to get an empirical distribution of the
# parameters of interest (like histograms).
# This general idea is called *bootstrapping*.
# Given some large number $N$, a specific type of *bootstrapping* is to sample the entire dataset
# *with replacement* $N$ times to create $N$ different datasets data are the same size as the
# original dataset.
# For each of those datasets, you can fit your model and get $N$ different versions of the parameter
# estimates.
# With a large enough $N$, you can find an approximate distribution of the parameters or functions
# of the parameters.

# To see this in action, first filter the training dataset to be cars whose `make` is toyota.
# We will fit a Linear Regression model on the toyota data to predict `price` using the
# `engineSize`, `mileage`, `mpg`, and `tax` columns.
# The parameter of interest is the ratio of the parameters for `engineSize` and `mpg` which would
# look like `coef_engineSize` / `coef_mpg`.
# Use 1000 bootstrap samples to estimate the **median** of the distribution of `coef_engineSize` /
# `coef_mpg`.

# Submit the estimate of the median of the parameter of interest.

# *Hint: you could keep track of all 1000 versions of the parameter estimates. For a given dataset,
# the estimate of the ratio can be calculated by taking the ratio of the two coefficients*. Then
# you'll have 1000 samples of the parameter of interest.

q10 = 0
