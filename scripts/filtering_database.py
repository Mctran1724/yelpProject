import argparse
import pandas as pd
import json

#Use argparse to make a nice console interface that takes cities, states, postal codes, and star range.
parser = argparse.ArgumentParser(description = "Include Filter Criteria")
parser.add_argument("--city", '-c', nargs = "+", help = "list desired cities in format of city names delimited by spaces")
parser.add_argument("--state", '-s', nargs = "+", help = "list desired states in format of state abbreviations delimited by spaces")
parser.add_argument("--postal_code", '-p', nargs = "+", help = "list desired postal codes delimited by spaces")
parser.add_argument("--star_range", '-r', nargs = "+", help = "input desired rating range as: 'min_stars max_stars'", default = [0.0, 5.0], type = float)
args = parser.parse_args()

desiredFields= ["business_id", "name", "address", "city", "state", "stars", "review_count", "attributes"]

'''dataDicts = [json.loads(f) for f in open("../yelp_dataset/yelp_academic_dataset_business.json", 'r')]
df = pd.DataFrame(dataDicts)
'''

df = pd.read_json("../yelp_dataset/yelp_academic_dataset_business.json", lines = True)

#Vars takes the __dict__ attribute of the Namespace object, allowing me to iterate through.
for arg in vars(args): #Returns __dict__ attribute, aligning the command line keyword with the arguments.
	vals = getattr(args, arg) #returns value of named attributes of args, which are in our case the values that we want to filter by
	#Filter sequentially. 
	if arg == "star_range": #The filtering is different for star_range because we only want to take rows within the given star range. Keep only columns from the desiredFields.
		print(f"Filtering by rating. Allowing vals between {vals[0]} and {vals[1]}")
		df = df.loc[(vals[0] <= df.stars) & (df.stars <= vals[1]), desiredFields]
	elif vals: #Take only those items that are in the allowed values. Keep only columns from the desiredFields.
		print(f"Filtering by {arg}. Allowing {vals}")
		df = df.loc[df[arg].isin(vals), desiredFields]

df.to_csv("../outputs/output1.csv", index = False) 