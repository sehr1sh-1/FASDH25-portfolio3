#import libraries 
import pandas as pd
import plotly.express as px

#Read the CSV file into a pandas DataFrame

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
print("\nDescription of 'lengths_sorted' DataFrame:")#Prints a header to label the upcoming output for clarity

#Calculates and shows count, average, middle, and spread values to summarize 'length' data
print(lengths_sorted['length'].describe())


#Display statistics for total and average article lengths per year
print("\nDescription of 'length_year_sorted' DataFrame:")
print(length_year_sorted[['length-sum', 'length-mean']].describe())

#Provide summary statistics for total and average article lengths per year-month
print("\nDescription of 'length_year_month_sorted' DataFrame:")
print(length_year_month_sorted[['length-sum', 'length-mean']].describe())



#Display entries from 2017 in the daily level data # Taken from Slide 30 -DHFAS-13.1-Dataframes and Pandas
#Helps check if 2017 has enough data to be meaningful or should be removed
print(lengths_sorted[lengths_sorted['year'] == 2017])

#Display 2017 row in the yearly summary DataFrame
#Allows you to inspect total and average article length for 2017 to assess consistency
print(length_year_sorted[length_year_sorted['year'] == 2017])

#Display 2017 entries in the monthly summary DataFrame
#Reveals how many months (if any) have data from 2017 and how much they contribute
print(length_year_month_sorted[length_year_month_sorted['year'] == 2017])



#Define the list of valid years we want to keep in our dataset with consistent and meaningful data
#Taken from slide 31 : DHFAS-13.1-Dataframes and Pandas and Conversation 
valid_years = [2021, 2022, 2023, 2024]

# Filter lengths_sorted to keep only rows from the valid years
lengths_sorted = lengths_sorted[lengths_sorted['year'].isin(valid_years)]

# Filter length_year_sorted to include only valid years
length_year_sorted = length_year_sorted[length_year_sorted['year'].isin(valid_years)]

#Filter length_year_month_sorted to include only valid years

length_year_month_sorted = length_year_month_sorted[length_year_month_sorted['year'].isin(valid_years)]

#Print the dataframe to check the updated dataframes
print(lengths_sorted)
print(length_year_sorted)
print(length_year_month_sorted)

#Box Graphs 
#Visualizes how individual article lengths are distributed across years to check variability and outliers
#Taken from Coolab cheatsheets: https://colab.research.google.com/drive/1_7AfMdtVT8v8iLVsEdI8huW3t4jHLe1D?usp=sharing#scrollTo=378f8029
fig_length_box = px.box(lengths_sorted,
             x="year",
             y="length",
             title="Distribution of Individual Article Lengths by Year",
             )

#Displays the plot
#fig_length_box.show()

#saves the graph in repository
fig_length_box.write_html("../Outputs/boxplot_article_lengths_by_day.html")

#This graph shows the average article length for each year and whether some years had more variation than others
fig_year_box = px.box(length_year_sorted,
                      y="length-mean",
                      title="Distribution of Yearly Average Article Lengths",
                       )          
#fig_year_box.show()
fig_year_box.write_html("../Outputs/boxplot_article_lengths_by_year.html")

# This graph compares monthly averages for each year, so we can see which years had longer or shorter articles overall
fig_monthly_box = px.box(length_year_month_sorted,
                         x="year",
                         y="length-mean",
                         title="Distribution of Monthly Average Article Lengths by Year",
                         )

#fig_monthly_box.show()
fig_monthly_box.write_html("../Outputs/boxplot_article_lengths_by_month.html")

##Bar Graphs

#Taken from slide no 10: DHFAS-13.2-Plotly and Visualisation and collab cheat sheet 

#Article length per day in from 2021 to 2024
#Count how many articles appear in each month (across all years)

month_counts_df = lengths_sorted['month'].value_counts().sort_index().reset_index()

#Rename columns for clarity in plotting
month_counts_df.columns = ['month', 'count']

#Create a bar chart showing article count per month
fig_length_bar = px.bar(
    month_counts_df,
    x='month',
    y='count',
    title='Number of Articles per Month',  
    labels={'count': 'Number of Articles', 'month': 'Month'}, 
    color='count',                          #Color intensity reflects article count
    
)

#Display the graph
#fig_length_bar.show()
fig_length_bar.write_html("../Outputs/number_of_articles_per_day_bar.html")


#Average article length per year 

#Create a bar chart showing how average article length has changed yearly
fig_year_bar = px.bar(
    length_year_sorted,
    x='year',
    y='length-mean',
    title='Average Article Length per Year',  
    labels={'length-mean': 'Average Length (tokens)', 'year': 'Year'},  
    color='length-mean',#Color intensity shows average length
   
)


#fig_year_bar.show()

fig_year_bar.write_html("../Outputs/number_of_articles_per_year_bar.html")

#Monthly average article length by year 

#Create grouped bar chart: each year is a different color group
#Shows how average article length changes per month, across years
fig_monthly_bar = px.bar(
    length_year_month_sorted,
    x='month',
    y='length-mean',
    color='year',              #Group bars by year
    barmode='group',           #Display bars side by side
    title='Monthly Average Article Length by Year',
    labels={'length-mean': 'Average Length (tokens)', 'month': 'Month'}
)

#fig_monthly_bar.show()
fig_monthly_bar.write_html("../Outputs/number_of_articles_per_month_bar.html")

##Scatter Plots

#Solution from Coolab Cheatsheet: plotly_cheatsheet_5_2.ipynb

#Explore how article lengths vary over time using scatter plots

#Individual Article Lengths Over Time (Daily)
#Combine 'year', 'month', and 'day' columns into a single datetime column for precise daily plotting
lengths_sorted['date'] = pd.to_datetime(lengths_sorted[['year', 'month', 'day']])

fig_scatter_daily = px.scatter(
    lengths_sorted,
    x='date',  # Use exact date for daily granularity (more detailed than just 'year')
    y='length',  # Article length in tokens
    title="Daily Article Lengths Over Time (2021-2024)",
    labels={'length': 'Article Length', 'date': 'Date'},  # Clear axis labels
    template='plotly_dark'  # Dark theme for better visual contrast
)
#fig_scatter_daily.show()
fig_scatter_daily.write_html("../Outputs/daily_article_lengths_scatter.html")

#Yearly Average Article Lengths

fig_scatter_yearly = px.scatter(
    length_year_sorted,
    x='year',  #Year on x-axis
    y='length-mean',  #Average length of articles that year
    title="Yearly Average Article Lengths",
    labels={'length-mean': 'Average Length', 'year': 'Year'},  #Axis labels for clarity
    template='plotly_dark'  #Consistent dark styling
)
#fig_scatter_yearly.show()
fig_scatter_yearly.write_html("../Outputs/yearly_article_lengths_scatter.html")
#Monthly Average Article Lengths

fig_scatter_monthly = px.scatter(
    length_year_month_sorted,
    x='month',    #Month number (1-12)
    y='length-mean',  #Average article length per month
    color='year',  #Color code points by year for comparison
    title="Monthly Average Article Lengths (2021-2024)",
    labels={'length-mean': 'Average Length', 'month': 'Month'},  #Axis labels for clarity
    template='plotly_dark'  #Maintain dark theme consistency
)
#fig_scatter_monthly.show()
fig_scatter_monthly.write_html("../Outputs/monthly_article_lengths_scatter.html")

##Histograms
#Taken from slide 15: DHFAS-13.2-Plotly and Visualisation



#Create a histogram of individual article lengths from daily-level data,with bars color-coded by publication year to allow year-wise comparison.
fig_daily_hist = px.histogram(
    lengths_sorted, #DataFrame containing individual article lengths
    x="length",  #x-axis shows article length (in tokens)
    color="year",   #Colors indicate publication year for comparative analysis
    title="Article Lengths in the Gaza Corpus (Daily Data)",
    labels={"length": "Length in tokens", "year": "Year of Publication"}  #Custom axis and legend labels
)

# Add an annotation to draw attention to a secondary peak in the distribution,indicating a different writing pattern or format in some articles.
fig_daily_hist.add_annotation(
    x=150, y=260,              #Coordinates for the arrow tip near the second peak
    ax=60, ay=-20,             #Arrow base offset to make the annotation more readable
    text="Second peak",        #Label text for the annotation
    showarrow=True,            #Display the arrow pointing to the feature
    arrowhead=1,               #Arrow style
    bgcolor="white"            #White background ensures label is visible over the plot
)

#Compute the overall mean length of articles to show the central tendency of the data.
mean_length_daily = lengths_sorted["length"].mean()

#Add a vertical dashed line to mark the mean length, making it easy to compare the average with the distribution's spread.
fig_daily_hist.add_vline(x=mean_length_daily, line_dash="dash")

#Add a label to the mean line so viewers know what the dashed line represents.
fig_daily_hist.add_annotation(
    x=mean_length_daily,
    y=320,                     #Y-position places label clearly above data bars
    xshift=50,                 #Slight horizontal offset to avoid overlapping with the line
    showarrow=False,           #No arrow needed—just a static label
    text="Mean length"
)

#fig_daily_hist.show()
fig_daily_hist.write_html("../Outputs/daily_article_length_hist.html")


#Yearly average article lengths (one bar per year)

#Create a histogram of yearly average article lengths (no color needed since x-axis is time-aggregated).
fig_yearly_hist = px.histogram(
    length_year_sorted,              #DataFrame with one row per year
    x="length-mean",                 #x-axis represents average article length per year
    title="Yearly Average Article Lengths in the Gaza Corpus",
    labels={"length-mean": "Average Length (tokens)"}  #Label for clarity
)

#Calculate the mean of these yearly averages to understand overall trends over time.
mean_length_yearly = length_year_sorted["length-mean"].mean()

#Add a dashed line to indicate the global mean across years.
fig_yearly_hist.add_vline(x=mean_length_yearly, line_dash="dash")

#Annotate this line to help viewers immediately recognize its significance.
fig_yearly_hist.add_annotation(
    x=mean_length_yearly,
    y=5,                          #Adjust y to position label above the bars
    xshift=50,
    showarrow=False,
    text="Mean yearly average length"
)

#Show the finalized histogram 
#fig_yearly_hist.show()
fig_yearly_hist.write_html("../Outputs/yearly_article_length_hist.html")


#Monthly average article lengths, colored by year

#Plot a histogram of average article lengths per month,color-coded by year to enable cross-year pattern analysis.
fig_monthly_hist = px.histogram(
    length_year_month_sorted,       #DataFrame with monthly aggregated article lengths
    x="length-mean",                #x-axis shows average article length
    color="year",                   #Color coding highlights changes in monthly trends across years
    title="Monthly Average Article Lengths by Year",
    labels={"length-mean": "Average Length (tokens)", "year": "Year"}
)

#Compute the mean across all monthly averages to show general central tendency over time.
mean_length_monthly = length_year_month_sorted["length-mean"].mean()

#Add a vertical dashed line at this mean to visually anchor comparisons.
fig_monthly_hist.add_vline(x=mean_length_monthly, line_dash="dash")

#Add an annotation to clarify the line's meaning without cluttering the plot.
fig_monthly_hist.add_annotation(
    x=mean_length_monthly,
    y=10,                        #Y-position of the label for visibility
    xshift=50,
    showarrow=False,
    text="Mean monthly average length"
)

#Display the final monthly histogram
#fig_monthly_hist.show()
fig_monthly_hist.write_html("../Outputs/monthly_article_length_hist.html")

##Line Graphs
#Taken from Collab Cheatsheet plotly_cheatsheet_4_1.ipynb and Slide: 15 DHFAS-13.2



#Daily average article lengths overtime 

#Convert 'year', 'month', and 'day' columns into a single datetime column for precise plotting of trends over time with daily granularity.
lengths_sorted['date'] = pd.to_datetime(lengths_sorted[['year', 'month', 'day']])

#Group the data by each day and compute the mean article length for that day to condense multiple articles per day into a single representative value.
daily_avg = lengths_sorted.groupby('date')['length'].mean().reset_index(name='avg_length')

#Generate a line plot showing how average article length varies day by day.
#`markers=True` adds visible dots at each data point for better readability.
fig_line_daily = px.line(
    daily_avg,
    x='date',
    y='avg_length',
    markers=True,
    title="Daily Average Article Length",
    labels={'avg_length': 'Average Length (tokens)', 'date': 'Date'},
    template='plotly_dark'  #Use a dark background theme for visual contrast
)

# Display the chart
#fig_line_daily.show()
fig_line_daily.write_html("../Outputs/daily_avg_article_length_line.html")


#Yearly average lengths 


#Create a line graph showing average article lengths per year to summarize annual trends and helps identify long-term patterns.
fig_line_year = px.line(
    length_year_sorted,
    x='year',
    y='length-mean',
    markers=True,
    title="Yearly Average Article Length",
    labels={'length-mean': 'Average Length (tokens)', 'year': 'Year'},
    template='plotly_dark'
)

#Show the line chart for yearly averages
#fig_line_year.show()
fig_line_year.write_html("../Outputs/yearly_avg_article_length_line.html")


#Monthly Avergae article lengths over time 

#Construct a 'year-month' string column in "YYYY-MM" format to use as x-axis values which enables plotting data points in correct monthly chronological order.
length_year_month_sorted['year_month'] = (
    length_year_month_sorted['year'].astype(str) + '-' +
    length_year_month_sorted['month'].astype(str).str.zfill(2)  #Ensures two-digit month format(e.g., 03 not 3)
)

#Create a line plot showing how monthly average lengths change over time.
#Useful for detecting seasonal or short-term variation.
fig_line_month = px.line(
    length_year_month_sorted,
    x='year_month',
    y='length-mean',
    markers=True,
    title="Monthly Average Article Length Over Time",
    labels={'length-mean': 'Average Length (tokens)', 'year_month': 'Month'},
    template='plotly_dark'
)

#Rotate x-axis tick labels for better readability, especially for long month sequences.
fig_line_month.update_layout(xaxis_tickangle=-45)

#Display the monthly line chart
#fig_line_month.show()
fig_line_month.write_html("../Outputs/monthly_avg_article_length_line.html")


##Tree map Graphs

#Taken from collab cheet sheets : plotly_cheatsheet_6_2.ipynb

#Daily Article lengths treemap
#Create a treemap showing the distribution of article lengths for each day folling this format Year, Month, Day
fig_daily_treemap = px.treemap(
    lengths_sorted,
    path=[px.Constant("All Articles"), 'year', 'month', 'day'],  #Define format for visualization
    values='length',                  #Size of each box corresponds to the length of individual articles
    color='length',                  #Color intensity reflects the length, helping spot longer/shorter articles visually
    color_continuous_scale='Viridis', #To make the graph visually appealing and interactive #Taken from ChatGpt Conversation 4 
    title='Article Length Distribution by Year and Month (Daily Data)'  #chart title
)

#Apply a dark theme for better contrast and modern look
fig_daily_treemap.update_layout(template='plotly_dark')

#Display the graph 
#fig_daily_treemap.show()
fig_daily_treemap.write_html("../Outputs/daily_article_length_treemap.html")



#Yearly Aggregated article lengths treemap 

#Create a treemap showing total article lengths per year to help visualize which years had more article content overall
fig_yearly_treemap = px.treemap(
    length_year_sorted,
    path=[px.Constant("Yearly Totals"), 'year'],  #Simple hierarchy with just years under a root label
    values='length-sum',             #Size of each block corresponds to total article length for that year
    color='length-mean',             #Use average length as color metric to reveal writing trends within the year
    color_continuous_scale='Reds',   #Use 'Reds' to visually distinguish this chart from others
    title='Total Article Length by Year' 
)

#Apply the dark theme to match visual consistency across plots
fig_yearly_treemap.update_layout(template='plotly_dark')

#Show the yearly treemap
#fig_yearly_treemap.show()
fig_yearly_treemap.write_html("../Outputs/yearly_article_length_treemap.html")


#Monthly Aggregated article lengths treemap 

# Create a treemap to show how article lengths change each month over the years which helps us see which months had more or less news coverage
fig_monthly_treemap = px.treemap(length_year_month_sorted,
    path=[px.Constant("Monthly Data"), 'year', 'month'],  #year and month format 
    values='length-sum',             #Block size represents total article length in each month
    color='length-mean',             #Color reflects average article length for that month (writing style/tone)
    color_continuous_scale='Greens', #Use 'Greens' to visually distinguish this from daily/yearly plots
    title='Article Length Distribution by Year and Month' 
)

#Apply dark mode for better readability 
fig_monthly_treemap.update_layout(template='plotly_dark')

#Show the monthly treemap
#fig_monthly_treemap.show()
fig_monthly_treemap.write_html("../Outputs/monthly_article_length_treemap.html")
