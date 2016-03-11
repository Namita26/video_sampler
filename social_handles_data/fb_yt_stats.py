import requests
import json
import csv
import facebook
import datetime
import os
from social_handles_data.fbstories import get_facebook_stories, get_grand_facebook_stories
from social_handles_data.ytstories import get_youtube_stories, get_grand_youtube_stories, get_youtube_title


start_date = '2011-01-01'

def get_end_date():
    return datetime.datetime.today().strftime('%Y-%m-%d')


def fetch_data(video_ids, brand_name):
    """
    Fetch views, likes, comments and shares for YouTube and Facebook videos
    :Input video ids should be given in following format.
    [
        {
            'fb': 932669140143902,
            'yt': 'pFrUnz-NO7A'
        },
    ]
    """
    final = []

    is_fetched = check_already_fetched(brand_name)
    end_date = get_end_date()
    if is_fetched:
        with open("social_handles_data/" + brand_name + '/' + end_date  +"_fb_yt_final.json", "r") as f:
            final = json.load(f)
        return json.dumps(final)
    else:
        all_fb = get_facebook_stories(video_ids, start_date, end_date, brand_name)
        yb = get_youtube_stories(video_ids, start_date, end_date, brand_name)
        all_yb = yb[0]
        title_info = yb[1]

    sum_total_views = []
    sum_total_likes = []
    sum_total_comments = []
    i = 0

    for i in xrange(0, len(all_fb)):
        each_video = {}
        each_video['facebook'] = {'video_id': all_fb[i][0], 'views':all_fb[i][1], 'likes':all_fb[i][2], 'comments': all_fb[i][3], 'shares': all_fb[i][4], 'video_title': all_fb[i][5], 'video_impressions_unique': all_fb[i][6], "video_engaged_users": all_fb[i][7]}

        each_video['youtube'] = {
                'video_id': all_yb[i][0],
                'views':all_yb[i][1],
                'likes': all_yb[i][2],
                'comments':all_yb[i][3],
                'video_title': get_youtube_title(title_info, all_yb[i][0])
            }
        each_video['fb_yt'] = {
                'total_views': all_fb[i][1] + all_yb[i][1],
                'total_likes': all_fb[i][2] + all_yb[i][2],
                'total_comments': all_fb[i][3] + all_yb[i][3]
            }
        final.append(each_video)

        sum_total_views.append(all_fb[i][1] + all_yb[i][1])
        sum_total_likes.append(all_fb[i][2] + all_yb[i][2])
        sum_total_comments.append(all_fb[i][3] + all_yb[i][3])

        # i = i + 1
    facebook_grand = get_grand_facebook_stories(all_fb)
    youtube_grand = get_grand_youtube_stories(all_yb)

    final.append(facebook_grand['facebook_grand_views'])
    final.append(youtube_grand['youtube_grand_views'])
    final.append(sum(sum_total_views))
    final.append(facebook_grand['facebook_grand_likes'])
    final.append(youtube_grand['youtube_grand_likes'])
    final.append(sum(sum_total_likes))
    final.append(facebook_grand['facebook_grand_comments'])
    final.append(youtube_grand['youtube_grand_comments'])
    final.append(sum(sum_total_comments))
    final.append(facebook_grand['facebook_grand_shares'])
    final.append(facebook_grand['facebook_grand_unique_impressions'])
    final.append(facebook_grand['facebook_grand_engaged_users'])

    with open("social_handles_data/" + brand_name +'/' + end_date + "_fb_yt_final.json", "w") as f:
        json.dump(final, f, indent=4)

    return json.dumps(final)


def chart_details(brand_name):
    with open("social_handles_data/" + brand_name + '/' + get_end_date()  +"_fb_yt_final.json", "r") as f:
        final = json.load(f)
    return json.dumps(final)


def check_already_fetched(brand_name):
    if os.path.isfile('social_handles_data/' + brand_name + '/'+ get_end_date() +'_fb_yt_final.json'):
        return True
    else:
        return False


if __name__ == "__main__":
    print fetch_data(video_ids)
