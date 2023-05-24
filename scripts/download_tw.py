import os
import pandas as pd
import time

import tweepy
import tqdm
import wget



def main():
    consumer_key = 'GjW4VkYPX7CFD2EsPEXUDQa4b'
    consumer_secret = 'wctPXRgg9916yNYWdLQs3TlulA82lQOIi1Gichhxg6uIMHaaOQ'

    access_token = '1071616827648819200-x086b6Aaf92TI0524idqLbhDRrmLdK'
    access_token_secret = 'MTaopOiPeNPlSLipmNZnAV8GAiVNeeKGJ22QWjiAVVDxm'

    bearer_token = 'AAAAAAAAAAAAAAAAAAAAABzgYQEAAAAANljwGa2S8%2BbjULK6vwapWQOoZIw%3Dd1iMfwR9RODhGHZyHbuFSVjOiJ4tX0H3Xha82kpVd1Vre6XRdZ'

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth, wait_on_rate_limit=True)

    client = tweepy.Client(bearer_token=bearer_token, consumer_key=consumer_key, consumer_secret=consumer_secret,
                           access_token=access_token, access_token_secret=access_token_secret, wait_on_rate_limit=True)

    tw_names = pd.read_excel('../data/Lyst_index.xlsx')

    os.chdir('../data/tw')

    for name in tqdm.tqdm(tw_names['tw account'][0:1]):
        if not os.path.exists(name):
            os.makedirs(name)

        #query = 'from:'+name+' -is:retweet -is:reply'
        query = 'from:'+name+' has:media'
        start_time = '2020-10-02T00:00:00Z'
        end_time = '2020-10-03T00:00:00Z'

        # get
        for tweet in tweepy.Paginator(client.search_all_tweets, query=query, start_time=start_time, end_time=end_time,
                                      tweet_fields=['created_at', 'conversation_id'], max_results=100).flatten():
            date = str(tweet.created_at).replace(' ', '_').replace(':', '-')
            text = tweet.text
            status = api.get_status(tweet.id, tweet_mode="extended")
            time.sleep(2)
            
            # save text
            try:
                text_path = name+'/'+date+'.txt'
                with open(text_path, 'a') as f:
                    f.write(text)
                print('write text: ', text_path)
            except:
                pass
                

            # save videos and photos
            try:
                # check if any media, extended_entities is here
                media_lists = status.extended_entities['media']  # try
                if media_lists is not None:
                    for m in media_lists:
                        v_idx = 0  # in case multiple videos and photos in single tweet
                        p_idx = 0
                        g_idx = 0

                        if m['type'] == 'video':
                            # find max birate variant
                            if m['video_info']['variants'][-1]['content_type'] == 'video/mp4':
                                video_url = m['video_info']['variants'][-1]['url']
                            else:
                                video_url = m['video_info']['variants'][-2]['url']
                            video_path = name+'/'+date+str(v_idx)+'.mp4'
                            v_idx += 1
                            if not os.path.exists(video_path):
                                wget.download(
                                    url=video_url, out=video_path, bar=None)
                                print('write video: ', video_path)

                        if m['type'] == 'photo':
                            photo_url = m['media_url']
                            photo_path = name+'/'+date+str(p_idx)+'.jpg'
                            p_idx += 1
                            if not os.path.exists(photo_path):
                                wget.download(
                                    url=photo_url, out=photo_path, bar=None)
                                print('write photo: ', photo_path)

                        if m['type'] == 'animated_gif':
                            # find max birate variant
                            if m['video_info']['variants'][-1]['content_type'] == 'video/mp4':
                                gif_url = m['video_info']['variants'][-1]['url']
                            else:
                                gif_url = m['video_info']['variants'][-2]['url']
                            gif_path = name+'/'+date+str(g_idx)+'_gif.mp4'
                            g_idx += 1
                            if not os.path.exists(gif_path):
                                wget.download(
                                    url=gif_url, out=gif_path, bar=None)
                                print('write GIF: ', gif_path)
            except:
                pass
            time.sleep(2)


if __name__ == '__main__':
    main()
