#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: rajneshbajaj
"""

import pandas as pd
import tweepy
import time
from datetime import datetime
import csv


with open(".csv",'a',newline='',encoding='utf-8') as fd:
    wr = csv.writer(fd, dialect='excel')     
    wr.writerow(["Username","Data Type","Screen Name","Date"])


CONSUMER_KEY = ''
CONSUMER_SECRET= ''
ACCESS_TOKEN = ''
ACCESS_SECRET =''


auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth,wait_on_rate_limit=True)




#username = pd.read_excel('example_data_twitterapi.xlsx')["Links"]
#username = [i.replace("https://twitter.com/","") for i in list(username)]


username = ["KimKardashian"]


for u in username:
    
    followers_count = api.lookup_users(screen_name=u)
    f_count = followers_count[0].followers_count
    print(f_count)
    delay = 5

    if f_count > 50000:
        delay = 10
    if f_count > 75000:
        delay = 60
    if f_count > 100000:
        delay = 75
    if f_count > 130000:
        delay = 100

    ids = []
    
    for page in tweepy.Cursor(api.followers_ids, screen_name=u).pages():
        ids.extend(page)
        print(len(ids))
        time.sleep(100)
        
    names= []
    
    
    today = str(datetime.today()).split(' ')[0]
    
    
    for i in range(0,len(ids),100):
        temp = ids[i+1:i+100]
        print(len(temp))    
        user_objs = api.lookup_users(user_ids = list(temp))
    
        for user in user_objs:
            row = [u,'Followers',user.screen_name,today]
            print(row)
            with open("demo_twitter_followers.csv",'a',newline='',encoding='utf-8') as fd:
                wr = csv.writer(fd, dialect='excel')     
                wr.writerow(row)
        time.sleep(0.3)
            
    
    ids = []
    
    for page in tweepy.Cursor(api.friends_ids, screen_name=u).pages():
        ids.extend(page)
        print(len(set(ids)))
        time.sleep(1)
    today = str(datetime.today()).split(' ')[0]
    
    
    for i in range(0,len(ids),100):
        temp = ids[i+1:i+100]
        print(len(temp))    
        user_objs = api.lookup_users(user_ids = list(temp))
    
        for user in user_objs:
            row = [u,'Following',user.screen_name,today]
            print(row)
            with open("kk_twitter_followers.csv",'a',newline='',encoding='utf-8') as fd:
                wr = csv.writer(fd, dialect='excel')     
                wr.writerow(row)
    
        time.sleep(1)
        


















'''
for user in tweepy.Cursor(api.friends, screen_name="rajnesh_bajaj").items():
    print('friend: ' + user.screen_name)




followers_list = []
for user in tweepy.Cursor(api.followers, screen_name=).items():
    followers_list.append(user.screen_name)
    print(user.screen_name)




followers = api.followers_ids("")

'''






df = pd.DataFrame(columns=['text', 'source', 'url','date'])
msgs = []
msg =[]

for tweet in tweepy.Cursor(api.search, q='#adidas', lang = 'en').items(20):
    msg = [tweet.text, tweet.source, tweet.source_url, tweet.created_at]
    msg = tuple(msg)
    msgs.append(msg)
    
df = pd.DataFrame(msgs)
df.to_csv('adidas2.csv')



