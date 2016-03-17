import requests
import json
import facebook
from social_handles_data.utils.fb import post_insights_object, facebook_graph_object, post_meta_info, get_insights


def get_facebook_video_ids(video_ids):
    facebook_video_ids = []
    for each_dict in video_ids:
        facebook_video_ids.append(each_dict['fb'])
    return facebook_video_ids


def get_facebook_stories(video_ids, start_date, end_date, brand_name):
    facebook_video_ids = get_facebook_video_ids(video_ids)
    return get_only_facebook_stories(facebook_video_ids, start_date, end_date, brand_name)

def get_only_facebook_stories(facebook_video_ids, start_date, end_date, brand_name):
    with open("social_handles_data/" + brand_name + '/' + end_date +"_fb_insights.json", "r") as f:
        insights_file = json.load(f)
    all_fb = []
    flag = 'False'
    insight_ids = insights_file.keys()
    for key in facebook_video_ids:
        if str(key) in insight_ids:
            flag = 'True'
    if flag:

        for video_id in facebook_video_ids:
            insights = insights_file[str(video_id)]['insights']
            fb_title = insights_file[str(video_id)]['meta_info']['video_title']

            created_time = insights_file[str(video_id)]['meta_info']['created_date']

            post_video_views = insights['data'][25]['values'][0]['value']

            post_video_views_unique = insights['data'][26]['values'][0]['value']

            post_video_stories = insights['data'][57]['values'][0]['value']
            post_engaged_users = insights['data'][55]['values'][0]['value']
            post_impressions_unique = insights['data'][4]['values'][0]['value']

            post_impressions_total = insights['data'][5]['values'][0]['value']

            autoplay = insights['data'][45]['values'][0]['value']['video play']

            engagement = post_engaged_users + (post_video_views_unique - autoplay)

            all_fb.append([video_id, post_video_views, post_video_stories['like'], post_video_stories['comment'], post_video_stories['share'], fb_title, post_impressions_unique, post_engaged_users, created_time, post_impressions_total, post_video_views_unique, engagement])
    else:
        get_insights(",".join(facebook_video_ids))
        graph = facebook_graph_object()
        for video_id in facebook_video_ids:
            insights = post_insights_object(video_id)
            fb_title = post_meta_info(video_id)['video_title']
            created_time = insights_file[str(video_id)]['meta_info']['created_date']
            post_video_views = insights['data'][25]['values'][0]['value']

            post_video_views_unique = insights['data'][26]['values'][0]['value']

            post_video_stories = insights['data'][57]['values'][0]['value']
            post_engaged_users = insights['data'][55]['values'][0]['value']
            post_impressions_unique = insights['data'][4]['values'][0]['value']

            post_impressions_total = insights['data'][5]['values'][0]['value']
            autoplay = insights['data'][45]['values'][0]['value']['video play']

            engagement = post_engaged_users + (post_video_views_unique - autoplay)

            all_fb.append([video_id, post_video_views, post_video_stories['like'], post_video_stories['comment'], post_video_stories['share'], fb_title, post_impressions_unique, post_engaged_users, created_time, post_impressions_total, post_video_views_unique, engagement])

    return all_fb


def get_grand_facebook_stories(all_fb):
    # all_fb = get_facebook_stories()
    grand = {
        "facebook_grand_likes": 0,
        "facebook_grand_views": 0,
        "facebook_grand_comments": 0,
        "facebook_grand_shares": 0,
        "facebook_grand_unique_impressions": 0,
        "facebook_grand_engaged_users": 0,
        "facebook_grand_unique_views": 0,
        "facebook_grand_total_impressions": 0
    }
    for f_video in all_fb:
        grand['facebook_grand_likes'] += f_video[2]
        grand['facebook_grand_views'] += f_video[1]
        grand['facebook_grand_comments'] += f_video[3]
        grand['facebook_grand_shares'] += f_video[4]
        grand['facebook_grand_unique_impressions'] += f_video[6]
        grand['facebook_grand_engaged_users'] += f_video[7]

        grand['facebook_grand_unique_views'] += f_video[10]
        grand['facebook_grand_total_impressions'] += f_video[9]
    return grand
