# Import libraries
import pandas as pd
import plotly.express as px

# Load and prepare the data
data_path = "/Users/mac/Downloads/FASDH25-portfolio3/data/dataframes/n-grams/2-gram/2-gram-year-month.csv"
df = pd.read_csv(data_path)

# Standardise column names
df.columns = df.columns.str.lower().str.strip()
df['2-gram'] = df['2-gram'].str.lower()

# Define 2-gram categories
destruction = ['israeli forces', 'military operations', 'the killing']
harmony = ['united nations', 'diplomatic efforts', 'peace talks']
selected_2grams = destruction + harmony

# Filter dataset
df_filtered = df[df['2-gram'].isin(selected_2grams)].copy()
df_filtered['year-month'] = pd.to_datetime(df_filtered[['year', 'month']].assign(day=1))

# Filter time range: Feb 2023 to Mar 2024
start_date = pd.to_datetime('2023-02-01')
end_date = pd.to_datetime('2024-03-31')
df_filtered = df_filtered[(df_filtered['year-month'] >= start_date) & (df_filtered['year-month'] <= end_date)]

# Categorize 2-grams
def categorize(row):
    if row['2-gram'] in destruction:
        return 'Destruction'
    elif row['2-gram'] in harmony:
        return 'Harmony'
    else:
        return 'Other'

df_filtered['category'] = df_filtered.apply(categorize, axis=1)

# Group and summarize
df_grouped = df_filtered.groupby(['year-month', 'category'])['count-sum'].sum().reset_index()
df_grouped['month_label'] = df_grouped['year-month'].dt.strftime('%b %Y')
df_grouped = df_grouped.sort_values('year-month')

# Plot grouped bar chart
fig = px.bar(
    df_grouped,
    x='month_label',
    y='count-sum',
    color='category',
    barmode='group',
    title='Destruction vs Harmony (Aggregated 2-Gram Trends: Feb 2023 – Mar 2024)',
    labels={
        'month_label': 'Month',
        'count-sum': 'Total Frequency',
        'category': 'Category'
    }
)

# Customize layout
fig.update_layout(
    xaxis=dict(tickangle=45),
    yaxis_title='Total Frequency',
    plot_bgcolor='#f9f9f9',
    title_font_size=18,
    legend_title_text='2-Gram Category'
)
# Show plot
fig.show()

# Save as HTML
fig.write_html("destruction_vs_harmony.html")

