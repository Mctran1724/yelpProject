import numpy as np
import pandas as pd

businesses = pd.read_json("yelp_dataset/yelp_academic_dataset_business.json", lines = True) #Pull businesses with business ID
sentiment = pd.read_csv("yelp_dataset/sentiment_scores.csv") #Pull calculated sentiments, the outputs of calculate_sentiment.py
aggregateSentiment = sentiment.groupby("business_id").mean() #Assume that overall sentiment is well represented by average of reviews
merged = pd.merge(aggregateSentiment, businesses, on='business_id', how='left') #left join on business_id.
merged['sentimentDivergence'] = merged['stars'] - merged['composite'] #Compute divergence of sentiment from stars.

desiredFields = ['city', 'state', 'stars', 'composite', 'sentimentDivergence'] #I believe these are the most useful fields for pivot tabling
df = merged[desiredFields] #Retain only the desired fields
df.to_csv("output4.csv", index=False) #Save to hard drive.