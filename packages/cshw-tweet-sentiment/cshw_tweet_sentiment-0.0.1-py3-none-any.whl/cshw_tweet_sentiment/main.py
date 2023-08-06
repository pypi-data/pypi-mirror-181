import pandas as pd
import re
from textblob import TextBlob

def clean_tweet(tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

def get_tweet_sentiment(tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(clean_tweet(tweet))
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'
 

def gen_sentiment(df: pd.DataFrame):
    sentiments = []
    for tweet in df["text"]:
        sentiments.append(get_tweet_sentiment(tweet))

    df["sentiment"] = sentiments
    return df


def display_sentiment(df: pd.DataFrame):
    # Display the first 30 rows
    print(df.head(30))

    values = df["sentiment"].value_counts()
    total = len(df)
    positive_per = (values["positive"] / total) * 100
    neutral_per = (values["neutral"] / total) * 100
    negative_per = (values["negative"] / total) * 100

    print('\n   Positive Tweets: {}\nNeutral Tweets: {}\nNegative Tweets: {}\n'.format(positive_per, neutral_per, negative_per))
