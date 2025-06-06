#import libraries 
import pandas as pd
import plotly.express as px

# Read the CSV file into a pandas DataFrame

lengths = pd.read_csv("../dataframes/length/length.csv")

#Check the structure and summary of the dataframes to understand their content and data types.
#taken from ChatGpt Conversation 1 
lengths.info()

#Sorting the dataframes by year for comparison and analysis as the years are given randomly in the dataset 
#Taken from Slides: DHFAS-13.1-Dataframes and Pandas
lengths_sorted = lengths.sort_values(by=['year', 'month', 'day'])


#print the sorted version for analysing data
print("Sorted Dataframe:")

print(lengths_sorted)

#Show summary statistics for the 'length' column to understand distribution of article lengths
#Taken from ChatGpt : Conversation 2 
print("\nDescription of 'lengths_sorted' DataFrame:")## Prints a header to label the upcoming output for clarity

# Calculates and shows count, average, middle, and spread values to summarize 'length' data
print(lengths_sorted['length'].describe())


# Display entries from 2017 in the daily level data # Taken from Slide 30 -DHFAS-13.1-Dataframes and Pandas
# Helps check if 2017 has enough data to be meaningful or should be removed
print(lengths_sorted[lengths_sorted['year'] == 2017])

#Define the list of valid years we want to keep in our dataset with consistent and meaningful data
# Taken from slide 31 : DHFAS-13.1-Dataframes and Pandas and Conversation 
valid_years = [2021, 2022, 2023, 2024]

# Filter lengths_sorted to keep only rows from the valid years
lengths_sorted = lengths_sorted[lengths_sorted['year'].isin(valid_years)]

#Print the dataframe to check the updated dataframes
print(lengths_sorted)


# Tree map Graph
#Taken from collab cheet sheets : plotly_cheatsheet_6_2.ipynb

#Daily Article Lengths Treemap (using lengths_sorted)
fig_daily_treemap = px.treemap(
    lengths_sorted,
    path=[px.Constant("All Articles"), 'year', 'month', 'day'],  # Hierarchy: Year > Month > Day
    values='length',  # Size represents article length
    color='length',  # Color intensity represents length
    color_continuous_scale='Viridis',  # Color scale for length representation
    title='Article Length Distribution by Year and Month (Daily Data)'
)

fig_daily_treemap.update_layout(template='plotly_dark')
fig_daily_treemap.show()

