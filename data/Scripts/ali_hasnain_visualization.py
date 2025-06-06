#importing neccessary libraries
import os
import pandas as pd
import plotly.express as px

#load the csv file 
df = pd.read_csv(r"C:\Users\aienullah.beg\Downloads\FASDH25-portfolio3\data\dataframes\tfidf\tfidf-over-0.3.csv")

#printing all the column names to check if its loaded
print(df.columns)
#show first 5 rows of the dataframe
df.head()

#combine year, month and day columns to create a full date column.
df["date"] = pd.to_datetime({
    "year": df["year-1"],
    "month": df["month-1"],
    "day": df["day-1"]
})

#extract month from date and convert to timestamp format (chatgpt help)
df["month"] = df["date"].dt.to_period("M").dt.to_timestamp()

#group by month and calculate avg. similarity for each month
monthly_df = df.groupby("month")["similarity"].mean().reset_index()

#print first few rows of the monthly average data
print(monthly_df.head())

#Another library for detailed plot customization (chatgpt help)
import plotly.graph_objects as go

#creating an empty figure
fig = go.Figure()

#add a line with markers to show average similarity over months (indirect help from chatgpt)
fig.add_trace(go.Scatter(
    x=monthly_df["month"],
    y=monthly_df["similarity"],
    mode="lines+markers",
    name="Average Similarity",
    line=dict(color="blue")
))

#customizing the layout with titles and white theme
fig.update_layout(
    title="Average Similarity Score by Month",
    xaxis_title="Month",
    yaxis_title="Average Similarity",
    template="plotly_white")


#find the row with highest avg. similarity
peak_row = monthly_df.loc[monthly_df["similarity"].idxmax()]
#get the month of the peak similarity
peak_month = peak_row["month"]
#get the peak similarity score
peak_value = peak_row["similarity"]

#add red marker and label to highlight the peak value on the chart (chatgpt help)
fig.add_trace(go.Scatter(
    x=[peak_month],
    y=[peak_value],
    mode="markers+text",
    name="Peak",
    marker=dict(color="red", size=10, symbol="circle"),
    text=["Peak"],
    textposition="top center"))
#adding an annotation pointing to the peak value
fig.add_annotation(
    x=peak_month,
    y=peak_value,
    text=f"Peak: {peak_value:.2f}",
    showarrow=True,
    arrowhead=2,
    ax=0,
    ay=-40,
    font=dict(color="red"))
#again updating layout to adjust font size
fig.update_layout(
    title="Average Similarity Score by Month",
    xaxis_title="Month",
    yaxis_title="Average Similarity",
    template="plotly_white",
    font=dict(size=15))

#show final line chart
fig.show()
#save the figure as an HTML file
fig.write_html(r"C:\Users\aienullah.beg\Downloads\FASDH25-portfolio3\data\Outputs\monthly_similarity_plot.html")

#filter original data to keep only rows from the peak month
peak_articles = df[df["month"] == peak_month]

#sort articles in the peak month by similarity score (descending order)
top_articles = peak_articles.sort_values("similarity", ascending=False)

#print top 20 similar article pairs from peak month
print(top_articles[["title-1", "title-2", "similarity"]].head(20))

#prepare a dataframe with titles from 'title-1' and their similarity(Chatgpthelp)
title_sim_1 = top_articles[["title-1", "similarity"]].rename(columns={"title-1": "title"})

#prepare a dataframe with titles from 'title-2' and their similarity(same as previous code)
title_sim_2 = top_articles[["title-2", "similarity"]].rename(columns={"title-2": "title"})


#combine both title sets into one dataframe
all_titles = pd.concat([title_sim_1, title_sim_2])
#sort all titles by similarity and remove duplicates (keep highest score for each title)
all_titles = all_titles.sort_values("similarity", ascending=False).drop_duplicates("title")

#get top 20 unique article titles by similarity
top_unique_titles = all_titles.head(20)

#print top 20 unique articles
print(top_unique_titles)

