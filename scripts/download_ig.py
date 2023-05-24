import os
import pandas as pd
import numpy as np
import random
import time

from datetime import datetime
from itertools import dropwhile, takewhile
from itertools import islice
from math import ceil

import instaloader
import tqdm


ig_names = pd.read_excel('../data/Lyst_index.xlsx')

if not os.path.exists('../data/ig'):
    os.makedirs('../data/ig')

username = 'vince.wx'
password = '.xiewen.1230.'

def main():
    class MyRateController(instaloader.RateController):

        def sleep(self, secs):
            wait_time = random.uniform(5, 30)
            time.sleep(secs)
            time.sleep(wait_time)

        def count_per_sliding_window(self, query_type):
            return 30 if query_type == 'other' else 40

    #L = instaloader.Instaloader(quiet=False)
    L = instaloader.Instaloader(quiet=False, rate_controller=lambda ctx: MyRateController(
        ctx), max_connection_attempts=5,fatal_status_codes=[302,400,429])

    L.login(username, password)
    os.chdir('../data/ig')

    #5:8 , 5, 6,7, 18:19, 18,
    for name in tqdm.tqdm(ig_names['ig account'][34:35]):
        if name is not None:
            # change directory to current product
            if not os.path.exists(name):
                os.makedirs(name)
            # os.chdir(name)

            posts = instaloader.Profile.from_username(
                L.context, name).get_posts()

            START_ = datetime(2019, 5, 26)
            END_ = datetime(2020, 2, 26)

            # download by dates
            for post in takewhile(lambda p: p.date >= START_, dropwhile(lambda p: p.date > END_, posts)):
                #print(post.date,  post.typename, post.likes, post.comments)
                L.download_post(post, name)
                '''
                with open('likes_comments_videoviews.txt','a+') as f:
                    f.write(name+' '+str(post.date).replace(' ','_').replace(':','-')+' '+str(post.likes)+' '+str(post.comments)+' '+str(post.video_view_count))
                    f.write('\n')
                '''

            # download by top k
            # likes and comments  // dates
            #posts_sorted_by_likes = sorted(posts,key=lambda p: p.likes + p.comments,reverse=True)
            #posts_sorted_by_date = sorted(posts, key=lambda p: p.date, reverse=True)

        # os.chdir('..')


if __name__ == '__main__':
    # print(instaloader.__version__)
    main()
