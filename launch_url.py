import webbrowser
import pandas as pd
"""
Simple program for opening a random url in your default browser
"""
webbrowser.open(pd.read_csv('G:\\WoW_Sentiment\\url_and_utc.csv').sample(n = 1).values[0][1])
