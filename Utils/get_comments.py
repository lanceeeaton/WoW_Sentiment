import praw
import pandas as pd
import time
import datetime
import csv
from api_info import ApiInfo


reddit = praw.Reddit(client_id=ApiInfo.CLIENT_ID,
                     client_secret=ApiInfo.CLIENT_SECRET, password=ApiInfo.PASSWORD,
                     user_agent=ApiInfo.USER_AGENT, username=ApiInfo.USERNAME)

reddit.read_only = True

columns = ['Comment List','Comment Number','Creation Date','Title']

write_csv = 'Data\\wow_comments.csv'
read_csv = 'Data\\urls.csv'

with open(write_csv, 'a') as csvFile: # adding header for easier use later
    writer = csv.writer(csvFile)
    writer.writerow(columns)
csvFile.close()


values = pd.read_csv(read_csv).values

for value_pair in values:
  
    url = value_pair[1]
    time.sleep(0.01)
    
    submission = reddit.submission(url = url)
    submission_dict = {} # Dict to hold a single observation
    submission_dict.update({'Title': submission.title,'Creation Date': int(submission.created)})
    
    print(datetime.datetime.fromtimestamp(int(submission.created)).strftime('%Y-%m-%d %H:%M:%S'))
    
    if len(submission.comments) < 0:
        comment_list = [] # list of all comments we will add to our dict
    else:
        submission.comments.replace_more(limit = 0) # flatten tree
        comments = submission.comments.list() # all comments
        comment_list = [] # list of all comments we will add to our dict
        
        for comment in comments:
            comment_list.append(comment.body)
            
    submission_dict.update({'Comment List': comment_list})
    submission_dict.update({'Comment Number': len(comment_list)})
    row = [submission_dict]
    (pd.DataFrame(row)).to_csv(write_csv,mode='a',header = False, index = False)


    