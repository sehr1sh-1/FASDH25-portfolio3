import pandas as pd

tfidf_df = pd.read_csv('../data/dataframes/tfidf/tfidf-over-0.3.csv')
topics_df = pd.read_csv('../data/dataframes/topic-model/topic-model.csv').rename(columns={'Topic': 'topic'})

print("TF-IDF DataFrame (first 5 rows):")
print(tfidf_df.head())

print("TF-IDF DataFrame columns:")
print(tfidf_df.columns.tolist())

print("Topic Model DataFrame (first 5 rows):")
print(topics_df.head())

print("Unique topics in topic model:", sorted(topics_df['topic'].unique()))

# Merge topic info for filename-1 #Chatgbt help code 1
merged_df = tfidf_df.merge(
    topics_df[['file', 'topic']].rename(columns={'file': 'filename-1', 'topic': 'topic_1'}),
    on='filename-1', how='left'
)

# Merge topic info for filename-2
merged_df = merged_df.merge(
    topics_df[['file', 'topic']].rename(columns={'file': 'filename-2', 'topic': 'topic_2'}),
    on='filename-2', how='left'
)

print("After merging topics, shape:", merged_df.shape)

# Remove unassigned topics (-1) chatgbt help 2
merged_df = merged_df[(merged_df['topic_1'] != -1) & (merged_df['topic_2'] != -1)].copy()
print("Filtered rows with assigned topics only:", merged_df.shape) #took chat help df.shape 

# Filter for years 2023 and 2024
merged_df = merged_df[merged_df['year-1'].isin([2023, 2024])].copy()
print("Filtered for years 2023 and 2024:", merged_df.shape)

print("Sample of merged and filtered data:")
print(merged_df.head())

print("Final DataFrame columns:")
print(merged_df.columns.tolist())

print("Years in final dataset:", sorted(merged_df['year-1'].unique()))

# Save to file
merged_df.to_csv('../data/Merged Data Frame_topic_model/merged_document.csv', index=False)
print("Merged data saved to 'merged_document_similarity_with_topics.csv'.")


