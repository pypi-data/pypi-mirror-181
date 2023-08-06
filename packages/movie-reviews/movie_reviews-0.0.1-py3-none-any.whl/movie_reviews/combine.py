"""Module providing Function to combine data"""
import os.path
import random
import pandas as pd


# open file
my_path = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(my_path, "./data/combined_movie_reviews.csv")
with open(path, encoding="UTF-8") as f:

    # read it using pandas
    data = pd.read_csv(f)

# function to generate mini data sets
def combine_reviews(size: int):
    """generate a sample dataset using a random source)"""
    if (size < 1 )| (size > data.shape[0]):
        raise Exception(f"Sample size must be less/greater than {size}")

    source_list = ["imdb", "rotten_tomatoes"]
    source = random.choice(source_list)
    tmp = data[(data["source"] == source)]
    reviews = tmp.sample(size).reset_index()[["text", "label"]]
    return reviews