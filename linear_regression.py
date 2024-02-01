# -*- coding: utf-8 -*-
"""Linear Regression.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1OO7Br3EPsszNDDp954KYVZgAFkvC0zs9

**Bike demand prediction**
"""

# import the pakages required
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math

# step 1 - Read the data
bikes = pd.read_csv('hour.csv')

bikes.head()

# step 2 - prelim Analysis and Feature selection
bikes_prep = bikes.copy()
bikes_prep = bikes_prep.drop(['index','date','casual','registered'], axis=1)

bikes_prep.head()

# Basic check of missing value
bikes_prep.isnull().sum(axis=0)

# visualize the data using pandas histogram
# tight_layout() used to remove overlap
bikes_prep.hist()
plt.tight_layout()

# step 3 - Data visualization for numerical
plt.subplot(2,2,1)
plt.title('temperature vs demand')
colors = ['g','r','m','b']
plt.scatter(bikes_prep['temp'],bikes_prep['demand'],s=0.5 , c = 'g')


plt.subplot(2,2,2)
plt.title('Atemperature vs demand')
plt.scatter(bikes_prep['atemp'],bikes_prep['demand'],s=0.5 , c = 'r')

plt.subplot(2,2,3)
plt.title('humidity vs demand')
plt.scatter(bikes_prep['humidity'],bikes_prep['demand'],s=0.5 , c = 'm')

plt.subplot(2,2,4)
plt.title('windspeed vs demand')
plt.scatter(bikes_prep['windspeed'],bikes_prep['demand'],s=0.5 , c = 'b')

plt.tight_layout()
plt.show()

# data visualization for categorical

# create list of unique season's values
cat_list = bikes_prep['season'].unique()

# create average demond per season using groupby
cat_average = bikes_prep.groupby('season').mean()['demand']

colors = ['g','r','m','b']
plt.subplot(3,3,1)
plt.title('Average demand per season')
plt.bar(cat_list,cat_average,color = colors)


cat_list = bikes_prep['year'].unique()
cat_average = bikes_prep.groupby('year').mean()['demand']
plt.subplot(3,3,2)
plt.title('Average demand per year')
plt.bar(cat_list,cat_average,color = colors)

cat_list = bikes_prep['month'].unique()
cat_average = bikes_prep.groupby('month').mean()['demand']
plt.subplot(3,3,3)
plt.title('Average demand per month')
plt.bar(cat_list,cat_average,color = colors)

cat_list = bikes_prep['hour'].unique()
cat_average = bikes_prep.groupby('hour').mean()['demand']
plt.subplot(3,3,4)
plt.title('Average demand per hour')
plt.bar(cat_list,cat_average,color = colors)

cat_list = bikes_prep['holiday'].unique()
cat_average = bikes_prep.groupby('holiday').mean()['demand']
plt.subplot(3,3,5)
plt.title('Average demand per holiday')
plt.bar(cat_list,cat_average,color = colors)

cat_list = bikes_prep['weekday'].unique()
cat_average = bikes_prep.groupby('weekday').mean()['demand']
plt.subplot(3,3,6)
plt.title('Average demand per weekday')
plt.bar(cat_list,cat_average,color = colors)

cat_list = bikes_prep['weather'].unique()
cat_average = bikes_prep.groupby('weather').mean()['demand']
plt.subplot(3,3,7)
plt.title('Average demand per weather')
plt.bar(cat_list,cat_average,color = colors)

cat_list = bikes_prep['workingday'].unique()
cat_average = bikes_prep.groupby('workingday').mean()['demand']
plt.subplot(3,3,8)
plt.title('Average demand per workingday')
plt.bar(cat_list,cat_average,color = colors)

plt.tight_layout()
plt.savefig('catgorial.png')
plt.show()

# check outliers
bikes_prep['demand'].describe()

bikes_prep['demand'].quantile([0.05,0.1,0.12,0.9,0.95,0.99])

# step 4 - check multiple Linear Regression Assumption

# Linearity using correliation coefficient matrix using corr
correlation = bikes_prep[['demand','temp','atemp','humidity','windspeed']].corr()

correlation

bikes_prep = bikes_prep.drop(['weekday','year','workingday','atemp','windspeed'],axis=1)

bikes_prep.head()

# check the autocorrelation in demand using acorr
df1 = pd.to_numeric(bikes_prep['demand'],downcast='float')

plt.acorr(df1,maxlags = 12)

# step 6 - create/Modify new features
# Log normalise the feature 'demand'
df1 = bikes_prep['demand']
df2 = np.log(df1)

plt.figure()
df1.hist(rwidth=0.9,bins=20)

plt.figure()
df2.hist(rwidth=0.9,bins=20)

bikes_prep['demand'] = np.log(bikes_prep['demand'])

bikes_prep

# autocorrelation in the demand column
t_1 = bikes_prep['demand'].shift(+1).to_frame()
t_1.columns = ['t-1']

t_2 = bikes_prep['demand'].shift(+2).to_frame()
t_2.columns = ['t-2']

t_3 = bikes_prep['demand'].shift(+3).to_frame()
t_3.columns = ['t-3']

bikes_prep_lag = pd.concat([bikes_prep,t_1,t_2,t_3],axis=1)

bikes_prep_lag.head()

bikes_prep_lag = bikes_prep_lag.dropna()

bikes_prep_lag.head()

# step 7 - create Dummy Variables and drop first, to avoid dummy variables trap using get_dummies
# season,holiday,weather,month,hour

bikes_prep_lag['season'] = bikes_prep_lag['season'].astype('category')
bikes_prep_lag['holiday'] = bikes_prep_lag['holiday'].astype('category')
bikes_prep_lag['weather'] = bikes_prep_lag['weather'].astype('category')
bikes_prep_lag['month'] = bikes_prep_lag['month'].astype('category')
bikes_prep_lag['hour'] = bikes_prep_lag['hour'].astype('category')

bikes_prep_lag.dtypes

bikes_prep_lag = pd.get_dummies(bikes_prep_lag,drop_first =True)

bikes_prep_lag.shape

# step 8 - create Train and test split
# split the X and Y dataset into training and testing set

# demand is the time dependent or time series
y = bikes_prep_lag[['demand']]
x = bikes_prep_lag.drop(['demand'],axis=1)

# create the size for 70% of the data
tr_size = 0.7 * len(x)
tr_size = int(tr_size)

x_train = x.values[0:tr_size]
x_test = x.values[tr_size: len(x)]
y_train = y.values[0:tr_size]
y_test = y.values[tr_size: len(y)]

# prediction using multi linar regression
# step 9 - Fit and score the model
# Linear Regression
from sklearn.linear_model import LinearRegression
std_reg = LinearRegression()
std_reg.fit(x_train,y_train)

# predict the y_values
y_predict = std_reg.predict(x_test)

r2_train = std_reg.score(x_train,y_train)
r2_test = std_reg.score(x_test,y_test)

from sklearn.metrics import mean_squared_error
rmse = math.sqrt(mean_squared_error(y_test,y_predict))
rmse

from sklearn.metrics import mean_absolute_error
rmse = math.sqrt(mean_absolute_error(y_test,y_predict))
rmse

# Final step - calculate RMSLE and compare rmse
y_test_e = []
y_predict_e =[]

for i in range(0,len(y_test)):
  y_test_e.append(math.exp(y_test[i]))
  y_predict_e.append(math.exp(y_predict[i]))

# Do the sum of the
log_sq_sum = 0.0
for i in range(0,len(y_test_e)):
  log_a = math.log(y_test_e[i] + 1)
  log_p = math.log(y_predict_e[i] + 1)
  log_diff = (log_p - log_a )**2
  log_sq_sum = log_sq_sum + log_diff
rmsle = math.sqrt(log_sq_sum/len(y_test))

print("")
print(rmsle)

x = pd.DataFrame(y_predict)
print(x)
# x.to_csv('y_predict')