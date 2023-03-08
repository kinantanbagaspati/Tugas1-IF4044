#!/home/bigdata/anaconda3/bin/python

import os
from datetime import datetime
from json import load
    
#socmed_dict = {}
data_directory = "../raw_json"

f = open(data_directory + ".txt", "w")

files_count = len(os.listdir(data_directory))
files_scanned = 0

for filename in os.listdir(data_directory):
    if ".json.json" not in filename:
        fileinfo = filename.split("_")
        # socmed_types.add((fileinfo[0], fileinfo[1]))
        try:
            data_list = load(open(data_directory + "/" + filename, encoding="cp437", errors='ignore'))
        except:
            continue
        if(type(data_list) is not list):
            continue

        for data_element in data_list:
            # To get the social media type, all json files except from instagram have this crawler target to differentiate
            socmed_type = "instagram"
            if data_element.get("crawler_target"):
                socmed_type = data_element["crawler_target"].get("specific_resource_type")
            # print(socmed_type, end="\t")

            if socmed_type == "facebook":
                # Data from facebook have its own comments to a post listed with each own created time
                f.write(socmed_type + "\t" + data_element.get("created_time", "-").split("T")[0] + "\t1\t0\n")
                # print(data_element.get("created_time", "-").split("T")[0] + "\t1\t0")
                for comment in data_element.get("comments", {}).get("data", []):
                    f.write(socmed_type + "\t" + comment.get("created_time", "-").split("T")[0] + "\t0\t1\n")
                    # print(socmed_type + "\t" + comment.get("created_time", "-").split("T")[0] + "\t0\t1")

            elif socmed_type == "twitter":
                # Data from twitter in this case is assumed that status is post, and reply is comments
                date = datetime.strptime(data_element.get('created_at'), "%a %b %d %H:%M:%S %z %Y")
                f.write(socmed_type + "\t" + date.strftime('%Y-%m-%d') + "\t1\t" + str(data_element.get("reply_count", 0)) + "\n")
                # print(date.strftime('%Y-%m-%d') + "\t1\t" + str(data_element.get("reply_count", 0)))

            elif socmed_type == "youtube":
                # Youtube video can be adressed as post, each comment from youtube_comment files are the comments
                date_str = data_element.get("snippet", {}).get("publishedAt", "-").split("T")[0]
                if(data_element.get("kind") == "youtube#video"):
                    f.write(socmed_type + "\t" + date_str + "\t1\t0\n")
                    # print(date_str + "\t1\t0")
                # if not youtube video, then this is youtube comment
                else:
                    f.write(socmed_type + "\t" + date_str + "\t0\t1\n")
                    # print(date_str + "\t0\t1")

            else: #socmed_type == "instagram"
                date_str = "-"
                try:
                    timestamp = int(data_element.get("created_time"))
                    if(timestamp > 0):
                        date_str = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
                except:
                    pass
                # print(date_str, end="\t")
                if data_element.get("parent"): # This is a comment
                    f.write(socmed_type + "\t" + date_str + "\t0\t1\n")
                    # print("0\t1")
                else: # This is a post
                    f.write(socmed_type + "\t" + date_str + "\t1\t0\n")
                    # print("1\t0")
    files_scanned += 1
    if(files_scanned %10 == 0):
        print(str(files_scanned) + "/" + str(files_count) + " files scanned")

f.close()