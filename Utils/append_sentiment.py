import pandas as pd
import csv
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


read_csv = 'Data\\reddit_data.csv'
write_file = 'Data\\reddit_with_sent.csv'
    
def get_sent(row):
    '''
    Gets the sentiment value for the row given using Vader and returns it
    '''
    
    analyzer = SentimentIntensityAnalyzer()
    comment_sent = [analyzer.polarity_scores(row['Title'])['compound']] # sentiment of each comment, initialized with sentiment of title

    comments = row['Comment List']

    for comment in comments.split():
        sentiment = analyzer.polarity_scores(comment)['compound']
        comment_sent.append(sentiment)
        
    return sum(comment_sent) / len(comment_sent)  # sentiment of entire posts comments + title
    
    
with open(write_file, 'a', newline='') as csvFile: # adding header to file
  writer = csv.writer(csvFile)
  writer.writerow(['Comment List','Comment Number','Title','Created Date','Full Url','Sentiment'])

for chunk in pd.read_csv(read_csv, chunksize = 1000):
    chunk['Sentiment'] = chunk.apply(get_sent, axis = 1)
    chunk.to_csv(write_file, mode='a', header = False, index = False) # don't include index or headings
    print(chunk)
    break




