import argparse
import pandas as pd
import numpy as np


parser = argparse.ArgumentParser(description = "Include Filter Criteria")
parser.add_argument("--city", '-c', nargs = "+", help = "list desired cities in format of city names delimited by spaces")
parser.add_argument("--state", '-s', nargs = "+", help = "list desired states in format of state abbreviations delimited by spaces")
parser.add_argument("--postal_code", '-p', nargs = "+", help = "list desired postal codes delimited by spaces")
parser.add_argument("--star_range", '-r', nargs = "+", help = "input desired rating range as: 'min_stars max_stars'", default = [0.0, 5.0], type = float)
args = parser.parse_args()


desiredFields= ["name", "city", "attributes"]
df = pd.read_json("../yelp_dataset/yelp_academic_dataset_business.json", lines = True)

#Vars takes the __dict__ attribute of the Namespace object, allowing me to iterate through.
for arg in vars(args):
	vals = getattr(args, arg) #returns value of named attributes of args, which are in our case the values that we want to filter by
	#Filter sequentially. 
	if arg == "star_range": #The filtering is different for star_range because we only want to take rows within the given star range. Keep only columns from the desiredFields.
		print(f"Filtering by rating. Allowing vals between {vals[0]} and {vals[1]}")
		df = df.loc[(vals[0] <= df.stars) & (df.stars <= vals[1]), desiredFields]
	elif vals: #Take only those items that are in the allowed values. Keep only columns from the desiredFields.
		print(f"Filtering by {arg}. Allowing {vals}")
		df = df.loc[df[arg].isin(vals)]


#Fill missing attribute dictionaries with this placeholder
filler = [{"NoAttributeListed": True}]
df.fillna(True, inplace = True) #Hacky thing here. I don't know why it doesn't work without this. Filling na without this has to effect
df.loc[df['attributes'] == True, ['attributes']] = filler #Fill all the NaN values with placeholder dictionaries
aList = (d for _, d in df['attributes'].iteritems()) #Create a generator comprehension for memory efficiency
attributeDF = pd.DataFrame(aList, index = df.index) #DataFrame to append
for col in attributeDF: #Need the dictionary to provide evaluation key for unknown objects
    attributeDF[col] = attributeDF[col].apply(lambda x: eval(str(x), {"nan": False, True: True, False: False}))

#Now to tackle the dictionaries of dictionaries...
toDrop = set() #Use a set to avoid redundancies since there may be more than one dictionary in a given column

for col in attributeDF:
    for row, entry in attributeDF[col].iteritems():
        if isinstance(entry, dict):
            for key, value in entry.items():
                attributeDF.loc[row, key] = value #Place the appropriate value
            toDrop.add(col) #Drop all the columns

attributeDF.drop(list(toDrop), axis=1, inplace = True) #Remove the redundant columns
attributeDF.fillna(False, inplace = True) #Fill all NaNs created from the unpacking with False.

df = pd.concat([df, attributeDF], axis = 1) #Concatenate the huge DF of attributes to the name and city.
df.drop("attributes", axis = 1, inplace = True) #Remove the now redundant attributes column

df.to_csv("../outputs/output2.csv", index = False)

