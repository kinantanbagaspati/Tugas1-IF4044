#!/home/bigdata/anaconda3/bin/python

import sys
from datetime import datetime
from json import load, loads
    
#socmed_dict = {}
data_directory = "../raw_json_test"

for line in sys.stdin:
    try:
        data_list = loads(line.strip())
    except:
        continue
    if(type(data_list) is not list):
        continue

    for data_element in data_list:
        # To get the social media type, all json files except from instagram have this crawler target to differentiate
        socmed_type = "instagram"
        if data_element.get("crawler_target"):
            socmed_type = data_element["crawler_target"].get("specific_resource_type")
        print(socmed_type, end="\t")

        if socmed_type == "facebook":
            # Data from facebook have its own comments to a post listed with each own created time
            print(data_element.get("created_time", "-").split("T")[0] + "\t1\t0")
            for comment in data_element.get("comments", {}).get("data", []):
                print(socmed_type + "\t" + comment.get("created_time", "-").split("T")[0] + "\t0\t1")

        elif socmed_type == "twitter":
            # Data from twitter in this case is assumed that status is post, and reply is comments
            date = datetime.strptime(data_element.get('created_at'), "%a %b %d %H:%M:%S %z %Y")
            print(date.strftime('%Y-%m-%d') + "\t1\t" + str(data_element.get("reply_count", 0)))

        elif socmed_type == "youtube":
            # Youtube video can be adressed as post, each comment from youtube_comment files are the comments
            date_str = data_element.get("snippet", {}).get("publishedAt", "-").split("T")[0]
            if(data_element.get("kind") == "youtube#video"):
                print(date_str + "\t1\t0")
            # if not youtube video, then this is youtube comment
            else:
                print(date_str + "\t0\t1")

        else: #socmed_type == "instagram"
            date_str = "-"
            try:
                timestamp = int(data_element.get("created_time"))
                if(timestamp > 0):
                    date_str = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
            except:
                pass
            print(date_str, end="\t")
            if data_element.get("parent"): # This is a comment
                print("0\t1")
            else: # This is a post
                print("1\t0")