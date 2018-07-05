#Import Python Packages

#Pandas
import inline as inline
import pandas as pd

#NumPy
import numpy as np

#Read CSV file
initial_dataset = pd.read_csv('tmdb-movies.csv')

#Matplotlib
import matplotlib.pyplot as plt
plt.interactive(False)

#-----DATA CLEANING-----

#Preliminary examination of CSV file
print(initial_dataset)

dataset = pd.DataFrame(initial_dataset)

print(dataset.shape)

#Delete columns we don't need for our analysis
columns_to_be_deleted =['id', 'imdb_id', 'cast', 'homepage', 'director', 'tagline', 'keywords', 'overview', 'production_companies', 'budget_adj', 'revenue_adj']

tmdb = dataset.drop(columns_to_be_deleted,1)

print(tmdb.head(5))
print(tmdb.dtypes)

#Delete any duplicates

tmdb.drop_duplicates(keep='first', inplace=True)

#Remove any rows with 0 in budget or revenue
tmdb = tmdb[tmdb.budget != 0]
tmdb = tmdb[tmdb.revenue != 0]

#Did we remove any budget or revenue rows with less than 1,000,000 in value successfully?
print(any(tmdb.budget == 0))
print(any(tmdb.revenue == 0))

#-----EXPLORING-----

#Popularity of movies?
avg_pop = tmdb.groupby(['release_year'])['popularity'].mean()

#Are movies becoming less/more popular?
plt.plot(avg_pop)
plt.xlabel('Year', fontsize = 15)
plt.ylabel('Popularity Score', fontsize=15)
plt.title('Average Popularity', fontsize=15)
plt.show()

#Movies are becoming increasingly more popular.

#If movies are becoming more popular then are they earning more money as a result?

#Profit (Revenue - Budget) for each movie?
tmdb['profit'] = tmdb['revenue'] - tmdb['budget']

avg_rev = tmdb.groupby(['release_year'])['revenue'].mean()
avg_budget = tmdb.groupby(['release_year'])['budget'].mean()
avg_profit = tmdb.groupby(['release_year'])['profit'].mean()

#Plotting financials
plt.plot(avg_rev)
plt.plot(avg_budget)
plt.plot(avg_profit)
plt.legend(['Average Revenue', 'Average Budget', 'Average Profit'], loc='upper left')
plt.xlabel('Year', fontsize = 15)
plt.ylabel('$ (100M)', fontsize=15)
plt.title('Average Financials by Year', fontsize=15)
plt.show()

#On an average level, there appears to be a correlation. Can we support this with statistics?

#Correlation of popularity and our data points.
pop_rev = np.round(tmdb['popularity'].corr(tmdb['revenue']),decimals=2)
pop_budget = np.round(tmdb['popularity'].corr(tmdb['budget']),decimals=2)
pop_profit = np.round(tmdb['popularity'].corr(tmdb['profit']),decimals=2)

print("The correlation coefficient between Popularity and Revenue is {}.\n"
      "The correlation coefficient between Popularity and Budget is {}.\n"
      "The correlation coefficient between Popularity and Profit is {}.\n".format(pop_rev,pop_budget,pop_profit))

#Most popular genres?
genres = tmdb['genres'].str.cat(sep = '|')
genres = pd.Series(genres.split('|'))
genres_count = genres.value_counts()
plt.figure(figsize=(10,10))
genres_count.plot(kind='bar')
plt.show()

