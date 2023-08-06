import os
import pandas as pd
from bru_analysis.most_effective_content import MostEffectiveContent
from bru_analysis.engagement_rate import EngagementRateFB, EngagementRateIG, EngagementRateTW

FOLDER_DATA = '/home/oscar/Labs'

groups = {}
words = ['hamburguesa', 'pedido', 'corral', 'mcdonald']
# words = ['hdhjsgdfhg']
account_ids_fb = [160665307320292, 335653391129]

df_pages_fb = pd.read_csv(f'{FOLDER_DATA}/bru_analysis/bru_analysis/ft_test/data/Facebook/facebook_lib_facebook_pages.csv')
df_posts_fb = pd.read_csv(f'{FOLDER_DATA}/bru_analysis/bru_analysis/ft_test/data/Facebook/facebook_lib_facebook_posts.csv')
df_enga_fb = EngagementRateFB(df_posts_fb, df_pages_fb).by_post()
mec_fb = MostEffectiveContent(df_posts_fb, df_pages_fb)
mec_post_fb = mec_fb.posts(account_ids=account_ids_fb, search_word=words)
mec_post_type_fb = mec_fb.posts_type(account_ids=account_ids_fb, search_word=words)
most_eff_hashtags_fb, compare_hashtags_fb, most_eff_mentions_fb, compare_mentions_fb = mec_fb.hashtags_mentions(compare_group="no_group",
                                                                                                                account_ids=account_ids_fb)
most_eff_words_fb, most_eff_nouns_fb, most_eff_verbs_fb, most_eff_adjs_fb = mec_fb.words()


df_pages_tw = pd.read_csv(f'{FOLDER_DATA}/bru_analysis/bru_analysis/ft_test/data/Twitter/twitter_lib_tweetreply.csv')
df_posts_tw = pd.read_csv(f'{FOLDER_DATA}/bru_analysis/bru_analysis/ft_test/data/Twitter/twitter_lib_tweet.csv')
account_ids_tw = ['2838220979', '1584148458']
df_enga_tw = EngagementRateTW(df_posts_tw, df_pages_tw).by_post()
mec_tw = MostEffectiveContent(df_posts_tw, df_pages_tw)
mec_post_tw = mec_tw.posts(account_ids=account_ids_tw, search_word=words)
mec_post_type_tw = mec_tw.posts_type(account_ids=account_ids_tw, search_word=words)
most_eff_hashtags_tw, compare_hashtags_tw, most_eff_mentions_tw, compare_mentions_tw = mec_tw.hashtags_mentions(compare_group="no_group",
                                                                                                                account_ids=account_ids_tw,
                                                                                                                search_word=words)
most_eff_words_tw, most_eff_nouns_tw, most_eff_verbs_tw, most_eff_adjs_tw = mec_tw.words(search_word=words)

account_ids_ig = ['4652205892', '2044002384']
df_pages_ig = pd.read_csv(f'{FOLDER_DATA}/bru_analysis/bru_analysis/ft_test/data/Instagram/instagram_lib_profile.csv')
df_posts_ig = pd.read_csv(f'{FOLDER_DATA}/bru_analysis/bru_analysis/ft_test/data/Instagram/instagram_lib_posts.csv')
df_enga_ig = EngagementRateIG(df_posts_ig, df_pages_ig).by_post()
mec_ig = MostEffectiveContent(df_posts_ig, df_pages_ig)
mec_post_ig = mec_ig.posts(account_ids=account_ids_ig, search_word=words)
mec_post_type_ig = mec_ig.posts_type(account_ids=account_ids_ig, search_word=words)
most_eff_hashtags_ig, compare_hashtags_ig, most_eff_mentions_ig, compare_mentions_ig = mec_ig.hashtags_mentions(compare_group="no_group",
                                                                                                                account_ids=account_ids_ig,
                                                                                                                search_word=words)
most_eff_words_ig, most_eff_nouns_ig, most_eff_verbs_ig, most_eff_adjs_ig = mec_ig.words(search_word=words)
