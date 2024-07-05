import pandas as pd
from googleapiclient.discovery import build
from bs4 import BeautifulSoup
import re

import warnings 
warnings.filterwarnings('ignore')

# YouTube API를 사용하여 댓글 가져오기
def get_video_comments(api_key, video_id):
    comments = []
    api_obj = build('youtube', 'v3', developerKey=api_key)
    response = api_obj.commentThreads().list(part='snippet,replies', videoId=video_id, maxResults=100).execute()

    while response:
        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']
            text_display = comment['textDisplay']
            author_display_name = comment['authorDisplayName']
            published_at = comment['publishedAt']
            like_count = comment['likeCount']
            
            # BeautifulSoup을 사용하여 HTML 태그 제거
            soup = BeautifulSoup(text_display, 'html.parser')
            clean_text = soup.get_text(separator=' ', strip=True)
            
            comments.append([clean_text, author_display_name, published_at, like_count])
     
            if item['snippet']['totalReplyCount'] > 0:
                for reply_item in item['replies']['comments']:
                    reply = reply_item['snippet']
                    reply_text_display = reply['textDisplay']
                    reply_author_display_name = reply['authorDisplayName']
                    reply_published_at = reply['publishedAt']
                    reply_like_count = reply['likeCount']
                    
                    # BeautifulSoup을 사용하여 HTML 태그 제거
                    reply_soup = BeautifulSoup(reply_text_display, 'html.parser')
                    clean_reply_text = reply_soup.get_text(separator=' ', strip=True)
                    
                    comments.append([clean_reply_text, reply_author_display_name, reply_published_at, reply_like_count])
     
        if 'nextPageToken' in response:
            response = api_obj.commentThreads().list(part='snippet,replies', videoId=video_id, pageToken=response['nextPageToken'], maxResults=100).execute()
        else:
            break
    
    return comments

# 여러 개의 video_id를 리스트로 지정
video_ids = ['FhFwr7IGtA8', 'YEs4cQ7yygk', 'ES6OkUJcCQQ', 'FCKk9X1Ox_Y', 's0hK97vhy1w', 'a_fRpuiecuM', 'vjY5sJvwtFY' ,'8qrKPd11GMQ', '_ZOTOyGyu3k', '9Rw48RxyNac', 'LxIcglnahcQ', '8e435zy551E','lyMZ6mdJZaQ', '3So5QdtLG44', 'IKMiZTB-F7I']

# 모든 댓글을 담을 리스트 초기화
all_comments = []

# 각 video_id에 대해 댓글 가져오기
for video_id in video_ids:
    comments = get_video_comments(api_key='AIzaSyCdbV6ufugDFytecdYQ6bD1AENWVJCqAfw', video_id=video_id)     # google api 필요
    all_comments.extend(comments)

# 데이터프레임 생성 및 Excel 파일로 저장
df = pd.DataFrame(all_comments, columns=['comment', 'author', 'date', 'num_likes'])
df.to_excel('youtube_vietnam_15_video.xlsx', index=None)
