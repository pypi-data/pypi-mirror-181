#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 17:50:42 2021

@author: oscar
"""
import random
import unittest
import pandas as pd
from copy import deepcopy
from most_effective_content import MostEffectiveContent

pd.options.mode.chained_assignment = None


s_net = 'fb'
FOLDER = '/home/oscar/Labs/Informes_010321/Facebook/'

if s_net == 'fb':
    page_id = "page_id"
    pages = 'facebook_lib_facebook_pages.csv'
    posts = 'facebook_lib_facebook_posts.csv'
elif s_net == 'ig':
    page_id = "owner_id"
    pages = 'instagram_lib_profile.csv'
    posts = 'instagram_lib_posts.csv'
elif s_net == 'tw':
    page_id = "twitter_id"
    pages = 'twitter_lib_tweetreply.csv'
    posts = 'twitter_lib_tweet.csv'

words = ['hamburguesa', 'pedido', 'corral', 'mcdonald']

df_pages = pd.read_csv(pages, index_col=0, low_memory=False)
df_posts = pd.read_csv(posts, index_col=0, low_memory=False)

print('ut_effec_content_fb.py')
print('post = ' + str(len(df_posts)))
print('brands = ' + str(len(df_posts[page_id].unique())))
print('================================================')


class Test(unittest.TestCase):

    def setUp(self):
        '''
        Variables to use in tests

        Returns
        -------
        None.

        '''
        print("SETUP...")
        df_ef_post = df_posts#.sample(300, random_state=1)
        self.df_ef_post = df_ef_post
        self.df_pages_empty = pd.DataFrame(columns=df_pages.columns)
        self.df_posts_empty = pd.DataFrame(columns=df_posts.columns)

        mec = MostEffectiveContent(df_posts, df_pages)
        self.df_posts_mef = mec.posts()
        self.df_posts_mef_type = mec.posts_type()
        self.df_hashtags_mentions = mec.hashtags_mentions(compare_group="no_group")
        self.df_words = mec.words()

        print("END SETUP")
        print('================================================')

    def test_data_normal(self):
        """
        This test with data ok

        Returns
        -------
        None.

        """
        print("TEST_DATA_NORMAL...")
        df_hashtags_mentions = self.df_hashtags_mentions
        df_hashtags_mentions1 = df_hashtags_mentions[0]
        df_hashtags_mentions2 = df_hashtags_mentions[1]
        df_hashtags_mentions3 = df_hashtags_mentions[2]
        df_hashtags_mentions4 = df_hashtags_mentions[3]

        df_words = self.df_words
        df_words1 = df_words[0]
        df_words2 = df_words[1]
        df_words3 = df_words[2]
        df_words4 = df_words[3]

        self.assertGreater(len(self.df_posts_mef), 0)
        self.assertGreater(len(self.df_posts_mef_type), 0)

        self.assertGreater(len(df_hashtags_mentions1), 0)
        self.assertIsNotNone(len(df_hashtags_mentions2), 0)
        self.assertGreater(len(df_hashtags_mentions3), 0)
        self.assertIsNotNone(len(df_hashtags_mentions4), 0)

        self.assertGreater(len(df_words1), 0)
        self.assertGreater(len(df_words2), 0)
        self.assertGreater(len(df_words3), 0)
        self.assertGreater(len(df_words4), 0)

        print("END TEST_DATA_NORMAL")
        print('================================================')

    def test_account_id(self):
        """
        This test with data ok

        Returns
        -------
        None.

        """
        print("TEST_ACCOUNT_ID...")


        account_ids_fb = [160665307320292, 335653391129]

        mec = MostEffectiveContent(df_posts, df_pages)
        df_posts_mef = mec.posts(account_ids=account_ids_fb)
        df_posts_mef_type = mec.posts_type(account_ids=account_ids_fb)
        df_hashtags_mentions = mec.hashtags_mentions(compare_group="no_group", account_ids=account_ids_fb)

        df_hashtags_mentions1 = df_hashtags_mentions[0]
        df_hashtags_mentions2 = df_hashtags_mentions[1]
        df_hashtags_mentions3 = df_hashtags_mentions[2]
        df_hashtags_mentions4 = df_hashtags_mentions[3]

        self.assertGreaterEqual(len(df_posts_mef), 0)
        self.assertGreaterEqual(len(df_posts_mef_type), 0)

        self.assertGreaterEqual(len(df_hashtags_mentions1), 0)
        self.assertGreaterEqual(len(df_hashtags_mentions2), 0)
        self.assertGreaterEqual(len(df_hashtags_mentions3), 0)
        self.assertGreaterEqual(len(df_hashtags_mentions4), 0)

        print("END TEST_ACCOUNT_ID")
        print('================================================')

    def test_words(self):
        """
        This test with data ok

        Returns
        -------
        None.

        """
        print("TEST_WORDS...")


        mec = MostEffectiveContent(df_posts, df_pages)
        df_posts_mef = mec.posts(search_word=words)
        df_posts_mef_type = mec.posts_type(search_word=words)
        df_hashtags_mentions = mec.hashtags_mentions(compare_group="no_group", search_word=words)

        df_hashtags_mentions1 = df_hashtags_mentions[0]
        df_hashtags_mentions2 = df_hashtags_mentions[1]
        df_hashtags_mentions3 = df_hashtags_mentions[2]
        df_hashtags_mentions4 = df_hashtags_mentions[3]

        self.assertGreaterEqual(len(df_posts_mef), 0)
        self.assertGreaterEqual(len(df_posts_mef_type), 0)

        self.assertGreaterEqual(len(df_hashtags_mentions1), 0)
        self.assertGreaterEqual(len(df_hashtags_mentions2), 0)
        self.assertGreaterEqual(len(df_hashtags_mentions3), 0)
        self.assertGreaterEqual(len(df_hashtags_mentions4), 0)

        print("END TEST_WORDS")
        print('================================================')

    def test_data_empty(self):
        '''
        This test with data empty

        Returns
        -------
        None.

        '''
        print("TEST_DATA_EMPTY...")

        mec_empty = MostEffectiveContent(df_posts=self.df_posts_empty,
                                              df_pages=self.df_pages_empty)
        df_posts_mef = mec_empty.posts()
        df_posts_mef_type = mec_empty.posts_type()
        df_hashtags_mentions = mec_empty.hashtags_mentions(compare_group="no_group")
        df_words = mec_empty.words()

        df_hashtags_mentions1 = df_hashtags_mentions[0]
        df_hashtags_mentions2 = df_hashtags_mentions[1]
        df_hashtags_mentions3 = df_hashtags_mentions[2]
        df_hashtags_mentions4 = df_hashtags_mentions[3]

        df_words1 = df_words[0]
        df_words2 = df_words[1]
        df_words3 = df_words[2]
        df_words4 = df_words[3]

        self.assertAlmostEqual(len(df_posts_mef), 0)
        self.assertAlmostEqual(len(df_posts_mef_type), 0)

        self.assertAlmostEqual(len(df_hashtags_mentions1), 0)
        self.assertAlmostEqual(len(df_hashtags_mentions2), 0)
        self.assertAlmostEqual(len(df_hashtags_mentions3), 0)
        self.assertAlmostEqual(len(df_hashtags_mentions4), 0)

        self.assertAlmostEqual(len(df_words1), 0)
        self.assertAlmostEqual(len(df_words2), 0)
        self.assertAlmostEqual(len(df_words3), 0)
        self.assertAlmostEqual(len(df_words4), 0)

        print("END TEST_DATA_EMPTY")
        print('================================================')


if __name__ == "__main__":
    unittest.main()
