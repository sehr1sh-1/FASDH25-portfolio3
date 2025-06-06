# Importing necessary libraries
import pandas as pd
import plotly.express as px

# Setting path to the data
data_path = "/Users/mac/Downloads/FASDH25-portfolio3/data/dataframes/n-grams/2-gram/2-gram-year-month.csv"

# Loading the CSV file
df = pd.read_csv(data_path)

# Standardise column names
df.columns = df.columns.str.lower().str.strip()

# Define the selected 2-grams for analysis
selected_2grams = ['israeli forces', 'united nations', 'the killing']

# Filter for the selected 2-grams and avoid SettingWithCopyWarning
filtered_df = df[df['2-gram'].isin(selected_2grams)].copy()

# Create a datetime column from year and month
filtered_df['year-month'] = pd.to_datetime(filtered_df[['year', 'month']].assign(day=1))

# Create a readable month label (e.g., "Jan 2023")
filtered_df['month_label'] = filtered_df['year-month'].dt.strftime('%b %Y')

# Sort the dataframe by date to maintain correct order
filtered_df = filtered_df.sort_values('year-month')

# Pivoting the data to have months as rows and 2-grams as columns
pivot_df = filtered_df.pivot_table(
    index='month_label',
    columns='2-gram',
    values='count-sum',
    aggfunc='sum',
    fill_value=0
).reset_index()

# Melt the pivoted DataFrame for use in Plotly
melted_df = pivot_df.melt(
    id_vars='month_label',
    var_name='2-gram',
    value_name='count'
)

# Create the grouped bar chart using Plotly
fig = px.bar(
    melted_df,
    x='month_label',
    y='count',
    color='2-gram',
    barmode='group',
    title='Usage Trends of Selected 2-Grams Over Time (by Month)',
    labels={'month_label': 'Month', 'count': 'Total Frequency', '2-gram': '2-Gram'}
)

# Enhancing chart layout for readability
fig.update_layout(
    xaxis=dict(tickangle=45),
    yaxis_title='Total Count (Sum)',
    plot_bgcolor='#f9f9f9',
    title_font_size=18,
    legend_title_text='2-Gram'
)

# Display the chart
fig.show()

# Optionally save the chart as an HTML file
fig.write_html("selected_2gram_monthly_trends.html")
