import os
import feedparser
from source import source_list
import datetime
import time
import requests

new_message_token = os.environ['NEW_MESSAGE_TOKEN']
epoch = datetime.datetime.utcfromtimestamp(0)


def unix_time_millis(dt):
    return (dt - epoch).total_seconds() * 1000.0


now = unix_time_millis(datetime.datetime.now())

for feed_source in source_list:
    feed = feedparser.parse(feed_source)
    for post in feed['entries']:
        tmp = unix_time_millis(datetime.datetime.fromtimestamp(time.mktime(post.updated_parsed)))
        if tmp + 1_000 * 60 * 60 > now:
            print("New post!")
            requests.post("https://life-ustc.tiankaima.cn/api/newMessage",
                          params={"token": new_message_token,
                                  "topic": post.title,
                                  "content": post.description})