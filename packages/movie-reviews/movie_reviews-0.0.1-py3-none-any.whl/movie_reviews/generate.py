"""Module providing Function to generate data"""
import os.path
import pandas as pd

# open file
my_path = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(my_path, "./data/combined_movie_reviews.csv")

with open(path, encoding="UTF-8") as f:

    # read it using pandas
    data = pd.read_csv(f)

# function to generate mini data sets
def generate_reviews(source: str, size: int):
    """
    generate a sample dataset using generate(source, sample size):
    source can be imdb or rt for rotten tomatoes - string
    sample size can be any number between 1 and max rows of the dataset
    default sample size is 30 records #not set yet
    returns a pandas object as dataframe
    """
    source = str(source)
    if size < 1 | size > data.shape[0]:
        raise Exception(f"Sample size must be less/greater than {size}")

    tmp = data[(data["source"] == source)]
    reviews = tmp.sample(size)[["text", "label"]]
    return reviews


def generate_class(source: str, size: int, pos: float):
    """
    generate a sample dataset with portions of postive and negative:
    source can be imdb or rt for rotten tomatoes - string
    sample size can be any number between 1 and max rows of the dataset
    default sample size is 30 records #not set yet
    returns a pandas object as dataframe
    """
    source = str(source)
    # check possible sample size
    if (size < 1) | (size > data.shape[0]):
        raise Exception(f"Sample size must be less/greater than {size}")

    if (pos < 0 )| (pos > 1):
        raise Exception(f"Portion size must be less/greater than {pos}")

    # set pos, neg ratio
    positive = int(size * pos)
    negative = size - positive

    sample_pos = data[(data["source"] == source) & (data["label"] == 1)].sample(
        positive
    )
    sample_neg = data[(data["source"] == source) & (data["label"] == 0)].sample(
        negative
    )
    frames = [sample_pos, sample_neg]
    tmp = pd.concat(frames)
    reviews = tmp.sample(frac=1).reset_index()[["text", "label"]]

    if negative == 0:
        tmp = data[(data["source"] == source)].sample(positive)
        reviews = tmp.sample(frac=1).reset_index()[["text", "label"]]
    elif positive == 0:
        tmp = data[(data["source"] == source)].sample(negative)
        reviews = tmp.sample(frac=1).reset_index()[["text", "label"]]
    else:
        sample_pos = data[(data["source"] == source) & (data["label"] == 1)].sample(
            positive
        )
        sample_neg = data[(data["source"] == source) & (data["label"] == 0)].sample(
            negative
        )
        frames = [sample_pos, sample_neg]
        tmp = pd.concat(frames)
        reviews = tmp.sample(frac=1).reset_index()[["text", "label"]]

    return reviews
