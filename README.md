# Youtube Video ETL Scheduler with Airflow

**Summary**
---
In this project I attempt to create an Extract, Transform, Load(ETL) pipeline using Python and Airflow and its scheduler. The pipeline will retrieve all video-related statistics for all videos or selected amount of videos from a given Youtube channel based on the channel name. The scheduler will run daily so that a time series record is generated for statistics such as view count, comment count, like count.  

**Background Information**
---
The free YouTube Data API V3 grants access to video-related data on youtube. The API key is available at https://console.developers.google.com/. The data obtained from the API is limited in the sense that each call to the API will only return the current count for variables such as view count, comment count, like count. There is no historical count available. Even though the API does not offer the option to retrieve historical record, setting up a scheduler will allow us to generate a time series record in variables such as view count, on an ongoing basis with a starting date set by the scheduler.

There are several ways to access video-level data on the Youtube API. In this project, I use playlist id for a given channel id. All video ids are retrieved from the playlist id.

The input variables are
1. API Key-user specific
2. Channel Name-name as shown on the youtube channel
3. Maximum Video Count-Youtube Data API V3 has a cap of 10,000 units per day. User can set the maximum to avoid making too many API calls when the Channel has too many videos

**Step 1: Data Preparation**
---
