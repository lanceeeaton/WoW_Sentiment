import praw
import pandas as pd
import requests
import json
from datetime import datetime
from api_info import ApiInfo

def get_pushshift_urls(after, before):
    """
    Gets all reddit urls from the wow subreddit starting from the after date until the before date.

    Arguments:
    after -- the date in UNIX Epoch time to start getting urls from
    before -- the date in UNIX Epoch time from which urls will not be gathered past

    """
    
    url_and_utc = {}
    url = 'https://api.pushshift.io/reddit/search/submission/?subreddit=wow&sort=asc&sort_type=created_utc&after='+str(after)+'&before='+str(before)+'&size=4'
    response = requests.get(url)
    data = json.loads(response.content)['data']
    print(len(data))
    for i in range(len(data)):
        created_utc = data[i].get('created_utc')
        full_link = data[i].get('full_link')
        url_and_utc.update({str(full_link): created_utc})
    return url_and_utc
       


 
urls = get_pushshift_urls(1217611716,1557952704)

print(urls)


'''reddit = praw.Reddit(client_id='ApiInfo.CLIENT_ID',
                     client_secret='ApiInfo.CLIENT_SECRET', password='ApiInfo.PASSWORD',
                     user_agent='ApiInfo.USER_AGENT', username='ApiInfo.USERNAME')

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

post = pd.DataFrame(rows_list)'''
