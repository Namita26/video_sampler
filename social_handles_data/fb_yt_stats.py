import requests
import json
import csv
import facebook
import datetime
import os
from social_handles_data.fbstories import get_facebook_stories, get_grand_facebook_stories
from social_handles_data.ytstories import get_youtube_stories, get_grand_youtube_stories, get_youtube_title, get_youtube_uniques, get_youtube_created_time
from social_handles_data.utils.fb_fetch_all_links import get_combined_insights



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
        with open("social_handles_data/" + brand_name + "/latest.json", "r") as f:
            final = json.load(f)
        return json.dumps(final)
    else:
        all_fb = get_facebook_stories(video_ids, start_date, end_date, brand_name)
        yb = get_youtube_stories(video_ids, start_date, end_date, brand_name)
        all_yb = yb[0]
        title_info = yb[1]
        uniques = yb[2]

    sum_total_views = []
    sum_total_likes = []
    sum_total_comments = []
    sum_total_uniques = []
    sum_total_engagement = []
    sum_total_impressions = []
    i = 0

    for i in xrange(0, len(all_fb)):
        each_video = {}
        each_video['facebook'] = {'video_id': all_fb[i][0], 'views':all_fb[i][1], 'likes':all_fb[i][2], 'comments': all_fb[i][3], 'shares': all_fb[i][4], 'video_title': all_fb[i][5], 'video_impressions_unique': all_fb[i][6], "video_engaged_users": all_fb[i][7], 'created_time': all_fb[i][8], 'video_impressions_total': all_fb[i][9], "unique_views": all_fb[i][10]}

        each_video['youtube'] = {
                'video_id': all_yb[i][0],
                'views':all_yb[i][1],
                'likes': all_yb[i][2],
                'comments':all_yb[i][3],
                'video_title': get_youtube_title(title_info, all_yb[i][0]),
                'unique_views': get_youtube_uniques(uniques, all_yb[i][0]),
                'created_time': get_youtube_created_time(title_info, all_yb[i][0])
            }
        each_video['fb_yt'] = {
                'total_views': all_fb[i][1] + all_yb[i][1],
                'total_likes': all_fb[i][2] + all_yb[i][2],
                'total_comments': all_fb[i][3] + all_yb[i][3],
                'total_unique_views': all_fb[i][10] + get_youtube_uniques(uniques, all_yb[i][0]),
                'total_engagement': all_fb[i][11] + get_youtube_uniques(uniques, all_yb[i][0])
            }

        final.append(each_video)

        sum_total_views.append(all_fb[i][1] + all_yb[i][1])
        sum_total_likes.append(all_fb[i][2] + all_yb[i][2])
        sum_total_comments.append(all_fb[i][3] + all_yb[i][3])
        sum_total_uniques.append(all_fb[i][10] + get_youtube_uniques(uniques, all_yb[i][0]))
        sum_total_engagement.append(all_fb[i][11] + get_youtube_uniques(uniques, all_yb[i][0]))
        print "Kechit", get_youtube_uniques(uniques, all_yb[i][0]), all_fb[i][9], get_combined_insights(all_fb[i][0])
        sum_total_impressions.append(get_youtube_uniques(uniques, all_yb[i][0]) + all_fb[i][9]  + get_combined_insights(all_fb[i][0]))

        # i = i + 1
    facebook_grand = get_grand_facebook_stories(all_fb)
    youtube_grand = get_grand_youtube_stories(all_yb, uniques)

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
    final.append(facebook_grand['facebook_grand_total_impressions'])
    final.append(facebook_grand['facebook_grand_unique_views'])
    final.append(youtube_grand['youtube_grand_uniques'])
    final.append(sum(sum_total_uniques))

    final.append(sum(sum_total_engagement))
    final.append(sum(sum_total_impressions))

    with open("social_handles_data/" + brand_name +'/' + end_date + "_fb_yt_final.json", "w") as f:
        json.dump(final, f, indent=4)

    with open("social_handles_data/" + brand_name +"/latest.json", "w") as f:
        json.dump(final, f, indent=4)

    return json.dumps(final)


def chart_details(brand_name):
    with open("social_handles_data/" + brand_name + "/latest.json", "r") as f:
        final = json.load(f)
    return json.dumps(final)


def check_already_fetched(brand_name):
    if os.path.isfile("social_handles_data/" + brand_name + "/latest.json"):
        return True
    else:
        return False


if __name__ == "__main__":
    print fetch_data(video_ids)
