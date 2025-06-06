import pandas as pd
import plotly.express as px

#Loading merged data
df = pd.read_csv('../data/Merged Data Frame_topic_model/merged_document.csv')

#Keeping only pairs from the same topic
same_topic_df = df[df['topic_1'] == df['topic_2']].copy()

#Calculating average similarity per topic per year
avg_sim = same_topic_df.groupby(['year-1', 'topic_1'])['similarity'].mean().reset_index()

#Renaming columns for clarity
avg_sim.columns = ['Year', 'Topic', 'Average_Similarity']

#Filtering for 2023 and 2024
avg_sim = avg_sim[avg_sim['Year'].isin([2023, 2024])]

#Topic Name Mappings
topic_id_to_name = {
    0: 'bank, west, israeli, palestinian',
    1: 'captives, hamas, release, hostages',
    3: 'hospital, patients, medical, hospitals',
    5: 'gaza, people, killed, younis'
}

#Apply the mapping to create a new 'Topic_Name' column
avg_sim['Topic_Name'] = avg_sim['Topic'].map(topic_id_to_name).fillna(avg_sim['Topic'].astype(str))

#Convert 'Topic' to numeric temporarily for sorting, then back to string for plotting #chat help
avg_sim['Topic_Numeric'] = pd.to_numeric(avg_sim['Topic'])
avg_sim = avg_sim.sort_values(by='Topic_Numeric')
avg_sim = avg_sim[avg_sim['Topic_Numeric'] <= 6]
avg_sim = avg_sim[avg_sim['Topic_Numeric'] <= 6]


#Get unique topic names in the desired numerical order for the x-axis
#This ensures that topics are ordered by their original IDs on the plot
topic_order_for_plot = avg_sim['Topic_Name'].unique().tolist()

#Convert 'Year' to string type to ensure it's treated as a categorical variable for coloring
avg_sim['Year'] = avg_sim['Year'].astype(str)

#Improved Grouped Bar Chart with Topic Names

#Creating grouped bar chart
fig = px.bar(
    avg_sim,
    x='Topic_Name',             
    y='Average_Similarity', 
    color='Year',               
    barmode='group',        
    title='Average Document Similarity within Topics: 2023 vs 2024',
    labels={
        'Topic_Name': 'Topic',  # Label for the x-axis
        'Average_Similarity': 'Average Similarity Score'
    },
    hover_data=['Year', 'Average_Similarity', 'Topic'], # Display Year, Similarity, and original Topic ID on hover
    category_orders={'Topic_Name': topic_order_for_plot} # Ensure topics are ordered correctly on x-axis
)

#Tuning plot layout for better readability #chat
fig.update_layout(
    xaxis_title="Topic", #Updated title for x-axis
    yaxis_title="Average Similarity Score",
    legend_title="Year",
    title_x=0.5, #Center the main title
    margin=dict(l=40, r=40, t=80, b=40), #Adjust margins
    bargap=0.1,  #Gap between bars *within* a group (e.g., 2023 and 2024 bars)
    bargroupgap=0.3 #Increased gap between groups of bars for each Topic
)

#Making x-axis show every topic clearlyy
fig.update_xaxes(
    type='category', #Treat Topic Names as categories
    tickmode='array', #Use 'array' mode to explicitly set tick values
    tickvals=topic_order_for_plot, #Show ticks for all unique topic names
    tickangle=-45 #Rotate labels slightly if they overlap
)

# Saving the plot
# save the plot as HTML
fig.write_html("../data/Outputs/Topic Modelling Visuals/average_similarity_bar_chart_by_topic.html")
#Showing the plot
fig.show()


