import pandas as pd
import requests
import json
import time
import csv

def get_pushshift_urls():
    """
    Gets all reddit urls and creation dates from the wow subreddit and writes them to a csv named urls.csv. 

    """
    after_date = 1217611716
    before_date = int(time.time())
    columns = ['Created Date','Full Url']
    write_file = 'Data\\urls.csv'
    
    with open(write_file, 'a', newline='') as csvFile: # adding header to file
      writer = csv.writer(csvFile)
      writer.writerow(columns)
    
    while True:
      url = 'https://api.pushshift.io/reddit/search/submission/?subreddit=wow&sort=asc&sort_type=created_utc&after='+str(after_date)+'&before='+str(before_date)+'&size=1000'
      response = requests.get(url)
      data = json.loads(response.content)['data']
      
      if len(data) != 0: # As long as there is data
        page_df = pd.DataFrame()
        
        for i in range(len(data)): # get info from all posts on page
            created_utc = data[i].get('created_utc')
            full_link = data[i].get('full_link')
            row_df = pd.DataFrame([[created_utc, full_link]],columns = columns) # one url, creation date pair
            page_df = page_df.append(row_df, ignore_index = True) # all pairs on the page
        
        page_df.to_csv(write_file, mode='a', header = False, index = False) # don't include index or headings
        after_date = int(page_df.tail(1)['Created Date'].values) + 1 
        time.sleep(.5) # waiting half second after each request 
      else: # no data
        break

get_pushshift_urls()
