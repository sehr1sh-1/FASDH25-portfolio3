#loading necessary libraries 
import os
import pandas as pd
import plotly.express as px

#loading the csv file into a dataframe
df = pd.read_csv(r"C:\Users\aienullah.beg\Downloads\FASDH25-portfolio3\data\dataframes\tfidf\tfidf-over-0.3.csv")

#print number of rows and columns
print(df.shape)

#print first and last 5 rows
print(df.head())
print(df.tail())

#print column names
print(df.columns)

#print top 5 most common similarity values
print(df["similarity"].value_counts().head())

#create a new column to group years into "Before 2000" and "2000 and After" (chatgpt help)
df["year_group"] = df["year-1"].apply(lambda y: "Before 2000" if y < 2000 else "2000 and After")

#creating a histogram of similarity scores, colored by year group
fig = px.histogram(df, x="similarity", nbins=100, title="Distribution of Similarity Scores", color="year_group")

#set x-axis ticks outside with width 2
fig.update_xaxes(ticks = "outside", tickwidth = 2)

# set y-axis ticks outside with width 2
fig.update_yaxes(ticks = "outside", tickwidth = 2)

#set new y-axis label
fig.update_yaxes(title_text='Frequency(Count)')

#show the histogram
fig.show()

#save to outputs folder
fig.write_html(r"C:\Users\aienullah.beg\Downloads\FASDH25-portfolio3\data\Outputs\histogram_similarity_scores.html")

#extract date from 'filename-1' column in YYYY-MM-DD format(Chatgpt help)
df["date"] = pd.to_datetime(df["filename-1"].str.extract(r"(\d{4}-\d{2}-\d{2})")[0])

#sort data by extracted date
df = df.sort_values("date")

#create a line chart to show similarity over time
fig = px.line(df, x="date", y="similarity", title="Similarity over Time")


#setting x-axis label
fig.update_xaxes(title_text='Timeperiod')

#show the line chart
fig.show()

#save output
fig.write_html(r"C:\Users\aienullah.beg\Downloads\FASDH25-portfolio3\data\Outputs\similarity_over_time.html")

#creating a box plot to show spread and outliers of similarity scores
fig = px.box(df, y="similarity", title="Boxplot of Similarity Scores")

#show the boxplot
fig.show()

#save the ouput
fig.write_html(r"C:\Users\aienullah.beg\Downloads\FASDH25-portfolio3\data\Outputs\boxplot_similarity_scores.html")
