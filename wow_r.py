import praw
import pandas as pd
from api_info import ApiInfo

reddit = praw.Reddit(client_id=ApiInfo.CLIENT_ID,
                     client_secret=ApiInfo.CLIENT_SECRET, password=ApiInfo.PASSWORD,
                     user_agent=ApiInfo.USER_AGENT, username=ApiInfo.USERNAME)
reddit.read_only = True

r_wow = reddit.subreddit('wow').hot(limit = 1)


rows_list = [] # list of all rows we will add to our DF

for submission in r_wow:
    submission_dict = {} # Dict to hold a single observation
    submission_dict.update({'Title': submission.title,'Date': submission.created_utc})
    
    if len(submission.comments) <= 0:
        comment_list = [] # list of all comments we will add to our dict
    else:
        submission.comments.replace_more(limit = 0) # flatten tree
        comments = submission.comments.list() # all comments
        comment_list = []
        
        for comment in comments:
            comment_list.append(comment.body)
            
    submission_dict.update({'Comment List': comment_list})
    submission_dict.update({'Comment Number': len(comment_list)})
    rows_list.append(submission_dict)

post = pd.DataFrame(rows_list)
