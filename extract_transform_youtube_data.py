import numpy as np
import pandas as pd
import requests
import matplotlib.pyplot as plt
from datetime import date
import os
from datetime import datetime
import pickle

#Please replace the api_key with your unique api key
api_key="-------"
#Please enter the name of a youtube channel that has all videos in a playlist
channel_name="-------"
#Please select the maximum number of videos to store in the dataframe
max_vid_count=12

def get_youtube_data(api_key, channel_name, max_vid_count):
    url="https://www.googleapis.com/youtube/v3/"
    #Get channel id based on channel name and store the result in a list
    channel_id=requests.get(url+"channels?key="+api_key+"&forUsername="+channel_name+"&part=id").json()["items"][0]["id"]
    #Get data in a dataframe
    #The steps to retrieve youtube data is the following
    #(1)Retrieve the playlist id based on channel id
    #(2)Use the playlist id to retrive video id
    #(3)Locate all video ids from each channel(Note: each page shows a max of 50 videos, thus nextPageToken is required to
    #load the next page, the process continues until there is no more nextPageToken on the current page.)
    #(4)For each video id located, retrieve all relevant information such as publish time, view count, like count, etc...
    df=pd.DataFrame()
    response_upload=requests.get(url+"channels?id="+channel_id+"&key="+api_key+"&part=contentDetails").json()
    playlist_id=response_upload["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
    response_video=requests.get(url+"playlistItems?playlistId="+playlist_id+"&order=date&key="+api_key+"&part=snippet&maxResults=50").json()
    while ("nextPageToken" in response_video.keys()):
        next_page_token=response_video["nextPageToken"]
        for video in response_video["items"]:
            if video["snippet"]["resourceId"]["kind"]=="youtube#video":
                video_id=video["snippet"]["resourceId"]["videoId"]
                publish_time=video["snippet"]["publishedAt"].split("T")[0]
                video_title=video["snippet"]["title"]
                video_description=video["snippet"]["description"]
                response_stats=requests.get(url+"videos?part=statistics&id="+video_id+"&key="+api_key).json()
                view_count=response_stats["items"][0]["statistics"]["viewCount"]
                like_count=response_stats["items"][0]["statistics"]["likeCount"]
                note=""
                try:
                    comment_count=response_stats["items"][0]["statistics"]["commentCount"]
                except:
                    comment_count=0
                    note="Comments are disabled"
                df=df.append({"Video_Id":video_id, "Upload_Date":publish_time, "Video_Title": video_title,
                                "Video_Description":video_description, "View_Count":view_count, "Like_Count":like_count,
                                "Comment_Count":comment_count, 
                                "Channel":channel_name, "Note": note},  ignore_index=True)
                if df.shape[0]==max_vid_count:
                    break
        if df.shape[0]==max_vid_count:
            break
        response_video=requests.get(url+"playlistItems?pageToken="+next_page_token+"&playlistId="+playlist_id+"&order=date&key="+api_key+"&part=snippet&maxResults=50").json()
    file_name=str(datetime.now().date())+'yt_data.pkl'
    full_file_name=os.path.join(os.path.dirname(__file__), file_name)
    df.to_pickle(full_file_name)

if __name__=="__main__":
    get_youtube_data(api_key, channel_name, max_vid_count)


