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





from bs4 import BeautifulSoup as soup

import requests
import csv


for page in range(0,23000,20):
    print(page)
    url = "https://www.celebritytalent.net/sampletalent/index.php?next="+str(page)

    r = requests.get(url).text
    bsobj = soup(r,'lxml')
    
    all_entry = bsobj.find_all('div',{"class":"entry"})
    names = [i.find('a').text for i in all_entry]
    
    
    with open('/Users/rajneshbajaj/Desktop/names.csv','a',newline='',errors='ignore') as fd:
        wr = csv.writer(fd, dialect='excel')
        for name in names:
            wr.writerow([name])
    








from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import csv
import datetime
import pandas as pd
from bs4 import BeautifulSoup as soup
from datetime import datetime
import requests
import docx


driver= webdriver.Chrome(executable_path='/Users/rajneshbajaj/Downloads/chromedriver 5')

texts_blob = pd.read_csv('/Users/rajneshbajaj/Desktop/Task - PDF File Log - magzine (1).csv')

links = texts_blob['URL']
indexs = texts_blob['Index']

compelete_dataframe = list(pd.read_excel('/Users/rajneshbajaj/Desktop/magzine.xlsx')[0])

remaining = list(set(indexs) - set(compelete_dataframe))

    
for i in remaining[306:]:
    driver.get(links[i])
    bsobj  = soup(driver.page_source,'lxml')

    index = indexs[i]
    all_p = bsobj.find_all('p')
    print(len(all_p))
    mydoc = docx.Document()
    
    for i in all_p:
        if "coalition" in i.text or "ouvriers" in i.text:  
            mydoc.add_paragraph(i.text)
            
    path = "/Users/rajneshbajaj/Desktop/untitled folder/"+str(index)+".docx"
    mydoc.save(path)










log_cred = pd.read_csv("/Users/rajneshbajaj/Downloads/login_credentials.csv - Sheet1.csv")
consumer_key = log_cred.iloc[0, 1]
consumer_secret = log_cred.iloc[1, 1]
access_token = log_cred.iloc[2, 1]
access_token_secret = log_cred.iloc[3, 1]








name = '0xferg'
tweet_id = '1572662065189515264'

replies=[]
for tweet in tweepy.Cursor(api.search,q='to:'+name, timeout=999999).items(1000):
    if hasattr(tweet, 'in_reply_to_status_id_str'):
        if (tweet.in_reply_to_status_id_str==tweet_id):
            replies.append(tweet)

with open('replies_clean1.csv', 'w') as f:
    csv_writer = csv.DictWriter(f, fieldnames=('screen_handle','name' ,'text','created_at'))
    csv_writer.writeheader()
    for tweet in replies:
        row = {'screen_handle': tweet.user.screen_name,'name':tweet.user.name ,'text': tweet.text.replace('\n', ' '),'created_at':str(tweet.created_at)}
        csv_writer.writerow(row)





import pandas as pd
import tweepy
import time
from datetime import datetime
import csv
import random

#create list of APIS keys
keys=[{"CONSUMER_KEY":'1doTsKylDwPodNvVMx17TBn1I',
     "CONSUMER_SECRET":'enqNCUFmUrTafmTkrncnW7hBT7BNIWIKD2iWwqw8M2hdjKiE1h',
     "ACCESS_TOKEN":'3349806612-3Ogblycok439LQaxS5EOx35pP2Aw5kmlGzBejyU',
     "ACCESS_SECRET":'gNDuMtyqklS3joWbz3LrZHQuK5fdo2NWs66wB0LFiqolE'
     },
     {"CONSUMER_KEY":'1doTsKylDwPodNvVMx17TBn1I',
     "CONSUMER_SECRET":'enqNCUFmUrTafmTkrncnW7hBT7BNIWIKD2iWwqw8M2hdjKiE1h',
     "ACCESS_TOKEN":'3349806612-3Ogblycok439LQaxS5EOx35pP2Aw5kmlGzBejyU',
     "ACCESS_SECRET":'gNDuMtyqklS3joWbz3LrZHQuK5fdo2NWs66wB0LFiqolE'
     }]


#Random Generating Index 



username = ["KimKardashian","cz_binance"]

for u in username:
    random_index = random.randint(0,len(keys)-1)

    auth = tweepy.OAuthHandler(keys[random_index]["CONSUMER_KEY"], keys[random_index]["CONSUMER_SECRET"])
    auth.set_access_token(keys[random_index]["ACCESS_TOKEN"], keys[random_index]["ACCESS_SECRET"])
    api = tweepy.API(auth,wait_on_rate_limit=True)

    followers_count = api.lookup_users(screen_name=u)
    





