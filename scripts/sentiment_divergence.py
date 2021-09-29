import numpy as np
import pandas as pd
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--cut", '-c', help = "How high the sentiment divergence should be to flag for investigation", default = 1.0, type = float)
args = parser.parse_args()

businesses = pd.read_json("../yelp_dataset/yelp_academic_dataset_business.json", lines = True) #Pull businesses with business ID
sentiment = pd.read_csv("../yelp_dataset/sentiment_scores.csv") #Pull calculated sentiments, the outputs of calculate_sentiment.py
aggregateSentiment = sentiment.groupby("business_id").mean() #Assume that overall sentiment is well represented by average of reviews
merged = pd.merge(aggregateSentiment, businesses, on='business_id', how='left') #left join on business_id.
merged['sentimentDivergence'] = merged['stars'] - merged['composite'] #Compute divergence of sentiment from stars.
#Make a cut on sentimentDivergence

cutVal = args.cut
print(f"Cutting on sentiment divergence at: {cutVal}")
merged['forReview'] = merged['sentimentDivergence'].apply(lambda x: abs(x) >= cutVal)

desiredFields = ['name', 'city', 'state', 'sentimentDivergence', 'forReview'] #I believe these are the most useful fields for pivot tabling
df = merged[desiredFields] #Retain only the desired fields
df.to_csv("../outputs/output4.csv", index=False) #Save to hard drive.