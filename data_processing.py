from __future__ import division

import MySQLdb
import numpy as np
import pandas as pd
import pandas_datareader as web
import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot')
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
from sklearn import preprocessing
from ConfigParser import SafeConfigParser

config = SafeConfigParser()
config.read('config.ini')

def initializeDatabase():
	try:
		db = MySQLdb.connect(host=config.get('sql', 'host'),
							user=config.get('sql', 'user'),
							passwd=config.get('sql', 'passwd'),
							db=config.get('sql', 'db'))
		print('Database initialized!')
	except ValueError:
		print('Error connecting to database!')
	
	return db

def databaseToDataframe(database):
	df_mysql = pd.read_sql('select * from data;', con=database)
	df_mysql.set_index('time', inplace=True)
	return df_mysql

def calculateMarketStats(dataframe):

	#calculate SMA at different time intervals
	dataframe_first_sma = calculateSMA(dataframe, 10)
	dataframe_second_sma = calculateSMA(dataframe_first_sma, 20)
	dataframe_third_sma = calculateSMA(dataframe_second_sma, 100)

	#add percentage change by interval
	dataframe_returns = addReturns(dataframe_third_sma)

	return dataframe_returns

def addReturns(dataframe):

	percentage_change = []

	#take first item (no percentage change) from row_iterator
	row_iterator = dataframe.iterrows()
	_, last = row_iterator.next()
	percentage_change.append(0)

	#calculate percentage change, add to list
	for i, row in row_iterator:
		price_delta = (row['price']-last['price'])/last['price']
		percentage_change.append(price_delta)
		last = row

	#assign values back to the dataframe
	returns = pd.Series(percentage_change)
	dataframe = dataframe.assign(returns=returns.values)

	return dataframe


def calculateSMA(dataframe, ticks):

	#Calculate Simple Moving Average over specified tick count
	df_tail = dataframe.tail(ticks)
	price_sum = df_tail['price'].sum()
	sma = price_sum/ticks
	print('Simple Moving Average over {} ticks: {}'.format(ticks, sma))

	#Populate SMA into list
	sma_list = []
	for x in range (0, len(dataframe)):
		if x < len(dataframe)-ticks:
			sma_list.append(0)
		else:
			sma_list.append(sma)

	#Concatenate SMA list into dataframe
	sma_calc = pd.Series(sma_list)
	dataframe = dataframe.assign(column_name=sma_calc.values)

	#Rename to unique column name with tick count
	column_name = 'sma_{}'.format(ticks)
	dataframe = dataframe.rename(columns={'column_name': column_name})

	return dataframe

def main_execute():
	db = initializeDatabase()
	df = databaseToDataframe(db)
	processed_data = calculateMarketStats(df)
	
	#predict_price(df, 50, 10)

	print(processed_data)

	#plot the current data by price
	processed_data['price'].plot()
	plt.show()

	db.close()

main_execute()


#function to calculate exponential moving average
#WARNING: ema values incorrect

'''
def calculateEMA(dataframe, ticks):

	#prepare prices and multiplier
	df_tail = dataframe.tail(ticks)
	prices_list = df_tail['price'].tolist()
	prices_array = np.asarray(prices_list)

	#use stack for ema calculations
	ema_stack = []
	curr_index = 0
	ema_stack.append(prices_array[curr_index])
	multiplier = 2 / ticks + 1

	#calculate ema
	#while curr_index >= len(prices_array):
	while len(ema_stack) > 0:
		if curr_index != len(prices_array)-1:
			previous_ema = ema_stack.pop()
			current_ema = (prices_array[curr_index] - previous_ema) * multiplier + previous_ema
			ema_stack.append(current_ema)
			curr_index += 1
		else:
			ema = ema_stack.pop()
			print('Exponential Moving Average over {} ticks: {}'.format(ticks, ema))
			return ema
'''

#function to plot linear regression model 

'''
def show_plot(dataframe, ticks):

	df_tail = dataframe.tail(ticks)
	times = list(df_tail.index.values)
	prices = list(df_tail['price'].values)

	linear_mod = linear_model.LinearRegression()
	times = np.reshape(times,(len(times),1))
	linear_mod.fit(times,prices)

	plt.scatter(times,prices,color='yellow')
	plt.plot(times,linear_mod.predict(times),color='blue',linewidth=3)
	plt.show()

	return

'''

#function to predict price

'''
def predict_price(dataframe, ticks, prediction_tick):

	#pair dates with ticks in dictionary

	df_tail = dataframe.tail(ticks)
	prices_list = list(df_tail['price'].values)
	for(prices_list)
	dates_list = list(df_tail.index.values)


	tick_list = []
	for x in range (0, ticks - 1):
		tick_list.add(x)

	prediction_date = dates_list[-prediction_tick]
	prediction = [prediction_date]

	linear_mod = linear_model.LinearRegression()
	dates = np.reshape(dates_list,(len(dates_list),1))
	prices = np.reshape(prices_list,(len(prices_list),1))

	linear_mod.fit(dates, prices)
	predicted_price = linear_mod.predict(prediction)
	return predicted_price[0][0],linear_mod.coef_[0][0],linear_mod.intercept_[0]

'''