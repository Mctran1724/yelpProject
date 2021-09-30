# Welcome to my brief yelp dataset project. 
The goal of this is to perform some data analyses with the online yelp dataset found at https://www.yelp.com/dataset.

#### In the scripts folder, you will find the programs/tools I created for this so far:  
1. filtering_database.py
1. tabulate_attributes.py
1. calculate_sentiment.py
1. sentiment_scores.py

## A short description for each one
**filtering_database.py** 
* Uses command line arguments via argparse.
* Currently gives csv of business_id, name, address, city, state, rating, review_count and business attributes
* These can be changed by changing the "desiredFields" variable.

**tabulate_attributes.py**
* Uses command line arguments the same way as filtering_database.py to query the data
* Then creates columns out of the attributes for use in a pivot table
* Gives back only the name, city, and attributes. 
* The attributes dictionaries are unpacked to generate purely tabular data.
* Python truthiness is used to convert the True/False into 1/0. 

**calculate_sentiment.py**
* Pulls the reviews dataset. This is too large for my RAM so I pull items in batches.
* Assigns a sentiment score to every single review in the dataset.
* For the sentiment analysis, I use both VADER and textblob. 
* Data cleaning is lowercasing, punctuation removal, and stopword removal. 
* Note: there could be some value to not cleaning the text that I have not extensively tested. On whole VADER performs well with punctuation and emojis. In addition, some textblob sentiment calculations seemed more accurate by eye test when no cleaning was done.
* The scores from vader and textblob are combined by averaging.
* In order to compare to the standard yelp 5 stars rating, the average is normalized to be on the interval [0,5] to give a composite rating score. 
* Note: I also did not decide to take into account subjectivity score from textblob or other aspects of the review (such as the review stars and reactions). 
* Future additions include taking these extra factors into account. The subjectivity could be used to weight the combination of VADER and textblob. 

**sentiment_divergence.py**
* Takes the composite sentiment and groups by business_id, and computes an aggregate business sentiment across all reviews by taking a simple average.
* Note: The review stars and reactions could be used to weight the contribution of each individual review to hte aggregate sentiment.
* Joins the business data from the business dataset with the aggregate sentiment on the business_id and outputs the sentiment divergence, the difference between the actual star rating and the star-rating-normalized aggregate sentiment. 
* One might imagine then making a cut on absolute divergence to determine which businesses need further review. 

