# -*- coding:utf-8 -*-
import json, config
from requests_oauthlib import OAuth1Session
from pymongo import MongoClient
import datetime
import time

CK = config.CONSUMER_KEY	
CS = config.CONSUMER_SECRET
AT = config.ACCESS_TOKEN
ATS = config.ACCESS_TOKEN_SECRET
twitter = OAuth1Session(CK, CS, AT, ATS)

url = "https://api.twitter.com/1.1/trends/place.json"

# MongoDBクライアントの作成
client = MongoClient('localhost', 27017)
db = client.twitter
collection = db.trends

woeid = '23424856'
params = {'id':woeid}

while True:
	date = datetime.datetime.now()
	req = twitter.get(url, params = params)
	i = 1
	if req.status_code == 200:
		search_trends = json.loads(req.text)
		print('--------------------------')
		print(date)
		print('--------------------------')
		for trend in search_trends[0]['trends']:
			trend_data = {\
				'name': trend['name'],\
				'woeid': woeid,\
				'url': trend['url'],\
				'query': trend['query'],\
				'tweet_volume': trend['tweet_volume'],\
				"rank": i, "date": date}
			print(trend['name'])
			result = collection.insert_one(trend_data)
			i += 1
		print('--------------------------')

	else:
	    print("ERROR: %d" % req.status_code)

	time.sleep(600)