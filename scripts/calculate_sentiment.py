#Imports
import pandas as pd 
import numpy as np
import json
from tqdm import tqdm
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


#Use a generator-like object to load the reviews (which are too big to load normally into RAM)
dfGenerator = pd.read_json("../yelp_dataset/yelp_academic_dataset_review.json", lines = True, chunksize=4096)
analyzer = SentimentIntensityAnalyzer()


#For cleaning review text. 
import string
from nltk.corpus import stopwords

sw = set(stopwords.words('english'))


def removeStopwords(text):
    words = []
    for word in text.split():
        word = word.strip()
        if word not in sw:
            words.append(word)
    return " ".join(words)
            

def cleanText(text):
    text = text.lower() #Lowercase everything
    text = text.replace(string.punctuation, "") #Remove punctuation
    text = removeStopwords(text) #Remove stopwords from text
    return text


#add sentiment score
def sentimentScore(df):
    df['text'] = df['text'].apply(lambda x: cleanText(x)) #Clean the text. Evaluations may be more accurate without this.
    df['polarity'] = df['text'].apply(lambda x: TextBlob(x).sentiment[0]) #Calculate the sentiment with textblob
    df['subjectivity'] = df['text'].apply(lambda x: TextBlob(x).sentiment[1]) #Calculate the subjectivity with textblob
    df['vader'] = df['text'].apply(lambda x: analyzer.polarity_scores(x)['compound']) #Calculate sentiment with vader
    df['composite'] = ((df['polarity'] + df['vader'])/2 + 1)*5/2 #Averaging the scores from textblob and vader, then normalizing to 5
    return df



with open("sentiment_scores.csv", "a") as f:
    for chunk in tqdm(dfGenerator):
        #It may be useful to retain other information, but for sake of time, I will keep things sparse.
        sentimentScore(chunk)[['business_id','composite']].to_csv(f, header = f.tell()==0)
        #f.tell gives the pointer location in the file. Hence if it is as the start, add a header.
        #intent is to compute average score across reviews.


