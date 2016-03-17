import requests
import json
from social_handles_data.utils.yt import post_insights_object_combined, get_youtube_video_ids
from social_handles_data.utils.file_util import FileUtil


def get_youtube_title(title_info, video_id):
    for i in title_info:
        if i['id'] == video_id:
            title = i['title']
    return title


def get_youtube_created_time(title_info, video_id):
    for i in title_info:
        if i['id'] == video_id:
            ctime = i['created_time']
    return ctime


def get_youtube_uniques(uniques, video_id):
    for i in uniques:
        if i['id'] == video_id:
            uniques = i['uniques']
    return uniques

def get_youtube_stories(video_ids, start_date, end_date, brand_name):
    youtube_video_ids = get_youtube_video_ids(video_ids)
    insights_file = FileUtil.readJson('social_handles_data/' +brand_name+ '/'+ end_date +'yt_stats.json')

    flag = False
    insight_ids = insights_file.keys()
    for key in youtube_video_ids:
        if str(key) in insight_ids:
            flag = True
    if flag:
        return [insights_file['all_yb'], insights_file['title_info']]
    else:
        return post_insights_object_combined(",".join(youtube_video_ids), brand_name)


def get_grand_youtube_stories(all_yb, uniques):
    # all_yb = get_youtube_stories()[0]
    grand = {
        "youtube_grand_likes": 0,
        "youtube_grand_views": 0,
        "youtube_grand_comments": 0,
        "youtube_grand_uniques": 0
    }
    for y_video in all_yb:
        grand['youtube_grand_likes'] += y_video[2]
        grand['youtube_grand_views'] += y_video[1]
        grand['youtube_grand_comments'] += y_video[3]
        grand['youtube_grand_uniques'] = sum([unique['uniques'] for unique in uniques])
    return grand

