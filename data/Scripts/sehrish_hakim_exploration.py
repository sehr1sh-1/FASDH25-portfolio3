#import libraries 
import pandas as pd
import plotly.express as px

# Read the CSV file into a pandas DataFrame

lengths = pd.read_csv("../dataframes/length/length.csv")


length_year = pd.read_csv("../dataframes/length/length-year.csv")


length_year_month = pd.read_csv("../dataframes/length/length-year-month.csv")


#printing the data frames to explore
#https://docs.google.com/presentation/d/1PbnpWuS_kh2LV5MitxvFx9FT-v6pXmhkccmwkLwzqQs/edit?slide=id.g3553d974d0f_1_0#slide=id.g3553d974d0f_1_0
print(lengths)
print(length_year)
print(length_year_month)

#Check the structure and summary of the dataframes to understand their content and data types.
#taken from ChatGpt Conversation 1 
lengths.info()
length_year.info()
length_year_month.info()

#Sorting the dataframes by year for comparison and analysis as the years are given randomly in the dataset 
#Taken from Slides: DHFAS-13.1-Dataframes and Pandas
lengths_sorted = lengths.sort_values(by=['year', 'month', 'day'])
length_year_sorted = length_year.sort_values(by='year')
length_year_month_sorted = length_year_month.sort_values(by=['year', 'month'])


#print the sorted version for analysing data
print("Sorted Dataframe:")

print(lengths_sorted)
print(length_year_sorted)
print(length_year_month_sorted)


#Show summary statistics for the 'length' column to understand distribution of article lengths
#Taken from ChatGpt : Conversation 2 
print("\nDescription of 'lengths_sorted' DataFrame:")## Prints a header to label the upcoming output for clarity

# Calculates and shows count, average, middle, and spread values to summarize 'length' data
print(lengths_sorted['length'].describe())


#Display statistics for total and average article lengths per year
print("\nDescription of 'length_year_sorted' DataFrame:")
print(length_year_sorted[['length-sum', 'length-mean']].describe())

#Provide summary statistics for total and average article lengths per year-month
print("\nDescription of 'length_year_month_sorted' DataFrame:")
print(length_year_month_sorted[['length-sum', 'length-mean']].describe())













