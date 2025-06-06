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



# Display entries from 2017 in the daily level data # Taken from Slide 30 -DHFAS-13.1-Dataframes and Pandas
# Helps check if 2017 has enough data to be meaningful or should be removed
print(lengths_sorted[lengths_sorted['year'] == 2017])

# Display 2017 row in the yearly summary DataFrame
# Allows you to inspect total and average article length for 2017 to assess consistency
print(length_year_sorted[length_year_sorted['year'] == 2017])

# Display 2017 entries in the monthly summary DataFrame
# Reveals how many months (if any) have data from 2017 and how much they contribute
print(length_year_month_sorted[length_year_month_sorted['year'] == 2017])



#Define the list of valid years we want to keep in our dataset with consistent and meaningful data
# Taken from slide 31 : DHFAS-13.1-Dataframes and Pandas and Conversation 
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

#Visualizes how individual article lengths are distributed across years to check variability and outliers
#Taken from Coolab cheatsheets: https://colab.research.google.com/drive/1_7AfMdtVT8v8iLVsEdI8huW3t4jHLe1D?usp=sharing#scrollTo=378f8029
fig_length_box = px.box(lengths_sorted,
             x="year",
             y="length",
             title="Distribution of Individual Article Lengths by Year")
#Displays the plot
fig_length_box.show()

#This graph shows the average article length for each year and whether some years had more variation than others
fig_year_box = px.box(length_year_sorted, y="length-mean", title="Distribution of Yearly Average Article Lengths")
fig_year_box.show()

# This graph compares monthly averages for each year, so we can see which years had longer or shorter articles overall
fig_monthly_box = px.box(length_year_month_sorted, x="year", y="length-mean", title="Distribution of Monthly Average Article Lengths by Year")

fig_monthly_box.show()


#Bar Graphs
#Taken from slide no 10: DHFAS-13.2-Plotly and Visualisation and collab cheat sheet 

#Count how many articles fall into each month (1–12)
month_counts = lengths_sorted['month'].value_counts().sort_index()  # Ensures chronological month order

#Create bar chart of article counts per month
fig_length_bar = px.bar(
    x=month_counts.index,  #X-axis is month number
    y=month_counts.values,  #Y-axis is article count
    labels={'x': 'Month', 'y': 'Number of Articles'},  #Axis labels for clarity
    title='Number of Articles per Month'  #Title for plot context
)

#Set X-axis ticks inside for visual alignment 
fig_length_bar.update_xaxes(
    ticks="inside",  #Main ticks inside the axis line
    tickwidth=2,  #Thickness of tick lines
    minor_ticks="inside",  #Minor ticks inside as well
    minor_tickwidth=2,  #Width of minor tick lines
    tickvals=list(range(1, 13))  #Explicit ticks for months 1–12
)

#Set Y-axis ticks outside for contrast 
fig_length_bar.update_yaxes(
    ticks="outside",  #Main ticks outside the axis line
    tickwidth=2,  #Tick thickness
    minor_ticks="outside",  #Minor ticks outside as well
    minor_tickwidth=2  #Width of minor tick lines
)

#Show values above bars to improve readability 
fig_length_bar.update_traces(
    text=month_counts.values,  #Use article counts as labels
    textposition='outside'  #Position labels above bars
)

fig_length_bar.show() 


#Bar chart to show how average article length has changed across years
fig_year_bar = px.bar(
    x=length_year_sorted['year'],
    y=length_year_sorted['length-mean'],
    labels={'y': 'Average Length (tokens)'},
    title='Average Article Length per Year'
)

#Same axis tick styling as before (see first chart)
fig_year_bar.update_xaxes(
    ticks="inside",
    tickwidth=2,
    minor_ticks="inside",
    minor_tickwidth=2
)

fig_year_bar.update_yaxes(
    ticks="outside",
    tickwidth=2,
    minor_ticks="outside",
    minor_tickwidth=2
)

#Show rounded average lengths above bars for easy comparison
fig_year_bar.update_traces(
    text=length_year_sorted['length-mean'].round(0),
    textposition='outside'
)

fig_year_bar.show()


# Group data by year and month to compute monthly average article lengths per year
monthly_grouped = length_year_month_sorted.groupby(['year', 'month'])['length-mean'].mean().reset_index()

# Bar chart comparing monthly average article lengths across years
fig_monthly_bar = px.bar(
    monthly_grouped,
    x='month',
    y='length-mean',
    color='year',  # Color distinguishes years for comparison
    barmode='group',  # Group bars side-by-side for clarity
    title='Monthly Average Article Length by Year'
)

# Repeated axis styling (already explained above)
fig_monthly_bar.update_xaxes(
    ticks="inside",
    tickwidth=2,
    minor_ticks="inside",
    minor_tickwidth=2,
    tickvals=list(range(1, 13))
)

fig_monthly_bar.update_yaxes(
    ticks="outside",
    tickwidth=2,
    minor_ticks="outside",
    minor_tickwidth=2
)

fig_monthly_bar.show()

#Scatter Plots


#Explore how article lengths vary over time using scatter plots
# Scatter plot for individual article lengths
fig_scatter_daily = px.scatter(
    lengths_sorted,
    x="year",
    y="length",
    title="Scatter Plot of Individual Article Lengths by Year"
)
fig_scatter_daily.show()

# Scatter plot for yearly average article lengths
fig_scatter_yearly = px.scatter(
    length_year_sorted,
    x="year",
    y="length-mean",
    title="Scatter Plot of Yearly Average Article Lengths"
)
fig_scatter_yearly.show()

# Scatter plot for monthly average article lengths
fig_scatter_monthly = px.scatter(
    length_year_month_sorted,
    x="month",
    y="length-mean",
    color="year",  # Differentiate years using color
    title="Scatter Plot of Monthly Average Article Lengths by Year"
)
fig_scatter_monthly.show()


#Histogram
#Taken from slide 15: DHFAS-13.2-Plotly and Visualisation
# Histogram of individual article lengths colored by year for daily data
fig_daily_hist = px.histogram(
    lengths_sorted,
    x="length",
    color="year",  # Color bars by publication year for easy comparison across years
    title="Article Lengths in the Gaza Corpus (Daily Data)",
    labels={"length": "Length in tokens", "year": "Year of Publication"}  # Clear axis and legend labels
)

#Highlight a notable second peak in the distribution with an annotation arrow
fig_daily_hist.add_annotation(
    x=150, y=260,  # Position of the arrow tip on the plot (adjust to fit your data)
    ax=60, ay=-20,  # Offset of the arrow base from the tip for better visibility
    text="Second peak",  # Annotation text
    showarrow=True,
    arrowhead=1,
    bgcolor="white"  # Background color for annotation text for readability
)

#Calculate mean article length from daily data to indicate central tendency
mean_length_daily = lengths_sorted["length"].mean()

#Add a vertical dashed line on the histogram at the mean length
fig_daily_hist.add_vline(x=mean_length_daily, line_dash="dash")

#Label the mean line for clarity
fig_daily_hist.add_annotation(
    x=mean_length_daily,
    y=320,  # Y position for annotation label (adjust based on plot scale)
    xshift=50,  # Shift label slightly right from the line to avoid overlap
    showarrow=False,
    text="Mean length"
)

#Display the completed daily histogram with annotations
fig_daily_hist.show()


#Histogram of yearly average article lengths (no color since year is categorical x-axis)
fig_yearly_hist = px.histogram(
    length_year_sorted,
    x="length-mean",
    title="Yearly Average Article Lengths in the Gaza Corpus",
    labels={"length-mean": "Average Length (tokens)"}
)

#Compute the mean of yearly average lengths for reference line
mean_length_yearly = length_year_sorted["length-mean"].mean()

#Add vertical dashed line at the mean yearly average length
fig_yearly_hist.add_vline(x=mean_length_yearly, line_dash="dash")

#Label the mean line on the yearly histogram
fig_yearly_hist.add_annotation(
    x=mean_length_yearly,
    y=5,  # Y position for annotation label, adjust if necessary
    xshift=50,
    showarrow=False,
    text="Mean yearly average length"
)

#Show the yearly average length histogram with mean line and label
fig_yearly_hist.show()


#Histogram of monthly average article lengths colored by year for comparison
fig_monthly_hist = px.histogram(
    length_year_month_sorted,
    x="length-mean",
    color="year",  # Color bars by year to compare monthly averages across years
    title="Monthly Average Article Lengths by Year",
    labels={"length-mean": "Average Length (tokens)", "year": "Year"}
)

#Calculate mean monthly average length for reference line
mean_length_monthly = length_year_month_sorted["length-mean"].mean()

#Add vertical dashed line at the mean monthly average length
fig_monthly_hist.add_vline(x=mean_length_monthly, line_dash="dash")

#Label the mean line on the monthly histogram
fig_monthly_hist.add_annotation(
    x=mean_length_monthly,
    y=10,  # Y position for label (adjust based on plot)
    xshift=50,
    showarrow=False,
    text="Mean monthly average length"
)

#Display the monthly histogram with color coding and mean line
fig_monthly_hist.show()


#Line Graphs
#Taken from Collab Cheatsheet plotly_cheatsheet_4_1.ipynb and Slide: 15 DHFAS-13.2


#Line chart of individual article lengths over time (daily data)
fig_line_daily = px.line(
    lengths_sorted,
    x='month',        # Using 'month' for time progression within each year
    y='length',       # Individual article lengths
    color='year',     # Differentiate years by color to show trends across years
    title="Line Plot of Individual Article Lengths by Month and Year",
    markers=True,     # Show markers for each data point
    labels={'length': 'Article Length (tokens)', 'month': 'Month', 'year': 'Year'}
)

#Update x-axis ticks to show all months clearly (1 to 12)
fig_line_daily.update_xaxes(
    tickvals=list(range(1, 13)),
    ticks="inside",
    tickwidth=2,
    minor_ticks="inside",
    minor_tickwidth=2
)

#Consistent y-axis styling with other plots
fig_line_daily.update_yaxes(
    ticks="outside",
    tickwidth=2,
    minor_ticks="outside",
    minor_tickwidth=2
)

fig_line_daily.show()


#Line chart of yearly average article length (already provided)
fig_line_year = px.line(
    length_year_sorted,
    x='year',
    y='length-mean',
    title="Line Plot of Yearly Average Article Lengths",
    markers=True,
    labels={'length-mean': 'Average Length (tokens)'}
)
fig_line_year.show()


# 3. Line chart of monthly average article length by year (already provided)
fig_line_month = px.line(
    length_year_month_sorted,
    x='month',
    y='length-mean',
    color='year',
    title="Line Plot of Monthly Average Article Lengths by Year",
    markers=True,
    labels={'length-mean': 'Average Length (tokens)', 'month': 'Month'}
)

#X-axis and Y-axis styling to maintain consistent appearance
fig_line_month.update_xaxes(
    tickvals=list(range(1, 13)),
    ticks="inside",
    tickwidth=2,
    minor_ticks="inside",
    minor_tickwidth=2
)

fig_line_month.update_yaxes(
    ticks="outside",
    tickwidth=2,
    minor_ticks="outside",
    minor_tickwidth=2
)

fig_line_month.show()

# Tree map Graphs
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

#Yearly Aggregated Lengths Treemap (using length_year_sorted)
fig_yearly_treemap = px.treemap(
    length_year_sorted,
    path=[px.Constant("Yearly Totals"), 'year'],  # Hierarchy: Year level
    values='length-sum',  # Size represents total yearly length
    color='length-mean',  # Color represents average article length
    color_continuous_scale='Reds',  # Different color scale for distinction
    title='Total Article Length by Year'
)
fig_yearly_treemap.update_layout(template='plotly_dark')
fig_yearly_treemap.show()

# 3. Monthly Aggregated Lengths Treemap (using length_year_month_sorted)
fig_monthly_treemap = px.treemap(
    length_year_month_sorted,
    path=[px.Constant("Monthly Data"), 'year', 'month'],  # Hierarchy: Year > Month
    values='length-sum',  # Size represents total monthly length
    color='length-mean',  # Color represents monthly average
    color_continuous_scale='Greens',  # Distinct color scheme
    title='Article Length Distribution by Year and Month'
)

fig_monthly_treemap.update_layout(template='plotly_dark')
fig_monthly_treemap.show()
