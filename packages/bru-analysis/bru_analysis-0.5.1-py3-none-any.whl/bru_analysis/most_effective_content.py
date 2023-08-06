import re
import sys
import ast
import json
import warnings
import pandas as pd
from copy import deepcopy
from bru_analysis.common.nlp_utils import CleanText, Features
from bru_analysis.common.identify_social_network import identify_social_network_posts
from bru_analysis.engagement_rate import EngagementRateFB, EngagementRateIG, EngagementRateTW

warnings.filterwarnings("ignore", "This pattern has match groups")
warnings.filterwarnings("ignore", category=DeprecationWarning)

ERR_SYS = "\nSystem error: "


class MostEffectiveContent:
    """
    This class computes the different atributes of the posts with
    higher engagement rate.
    """

    def __init__(self, df_posts, df_pages):
        """
        This method computes the DataFrame 'df_posts_full'
        which contains all the information of the posts, including columns
        'page_name'.

        Parameters
        ----------
        df_posts:
            type: DataFrame
            Information of the posts.
            This Pandas DataFrame must have columns 'page_id',
            'page_name', 'message' and 'engagement_rate_by_post'.
        df_pages:
            type: DataFrame
            Information of the pages.
            This Pandas DataFrame must have columns 'page_id' and 'name.
            It is used just to set the page name in the DataFrame 'df_posts'.
        """

        self.df_pages = df_pages
        self.s_net = identify_social_network_posts(df_posts)
        if self.s_net == 'fb':

            self.df_posts = EngagementRateFB(df_posts, df_pages).by_post()
            self.page_id = "page_id"
            self.page_name = "page_name"
            self.post_id = "post_id"
            self.message = "message"
            # self.permalink_url = "permalink_url"
            self.hashtags = "hashtags"
            self.type = "type"
            self.message_tags = "message_tags"
            self.userid = "page_id"
            self.fan_count = "fan_count"
            self.created_time = "created_time"

        elif self.s_net == 'ig':

            self.df_posts = EngagementRateIG(df_posts, df_pages).by_post()
            self.page_id = "owner_id"
            self.page_name = "owner_username"
            self.post_id = "shortcode"
            self.message = "caption"
            self.type = "typename"
            self.hashtags = "caption_hashtags"
            self.message_tags = "caption_mentions"
            self.userid = "userid"
            self.fan_count = "followers"
            self.created_time = "date"

        elif self.s_net == 'tw':

            self.df_posts = EngagementRateTW(df_posts, df_pages).by_post()
            self.page_id = "twitter_id"
            self.page_name = "screen_name"
            self.post_id = "tweet_id"
            self.message = "text"
            self.type = "media_entities"
            self.hashtags = "hashtags"
            self.message_tags = "user_mentions"
            self.userid = "twitter_id"
            self.fan_count = "ac_followers_count"
            self.created_time = "created_at"

        else:
            print(f'{self.s_net} social network not valid')

        method_name = "__init__"

        self.posts_columns = [
            self.page_id,
            self.page_name,
            self.post_id,
            self.message,
            # self.permalink_url,
            self.type,
            self.message_tags,
            self.created_time,
            "engagement_rate_by_post",
            "rel_engagement_rate_by_post"
        ]

        self.output_columns = [
            self.page_id,
            self.page_name,
            self.post_id,
            self.message,
            # self.permalink_url,
            self.type,
            self.message_tags,
            self.created_time,
            "engagement_rate_by_post",
            "rel_engagement_rate_by_post"
        ]

        if self.s_net != 'fb':
            self.posts_columns = self.posts_columns + [self.hashtags]

        self.features = None

        if len(self.df_posts) > 0 and len(self.df_pages) > 0:
            try:
                df_posts_full = deepcopy(self.df_posts[self.posts_columns])

                self.df_posts_full = df_posts_full
                self.len_posts_full = len(self.df_posts_full)

            except Exception as e:
                exception_type = sys.exc_info()[0]
                print(ERR_SYS + str(exception_type))
                print(e)
                print(f"Class: {self.__str__()}\nMethod: {method_name}\n")
                self.df_posts_full = pd.DataFrame(columns=self.output_columns)
                self.len_posts_full = len(self.df_posts_full)
        else:
            print("Warning: One of the DataFrames is empty. It cannot be computed.")
            self.df_posts_full = pd.DataFrame(columns=self.output_columns)
            self.len_posts_full = len(self.df_posts_full)

    def posts(self, n_most_eff=5, engagement_rate="engagement_rate_by_post", **kwargs):
        """
        This function computes the DataFrame 'df_most_eff_posts'
        which contains the posts with higher engagement rate for the accounts selected.

        Parameters
        ----------
        n_most_eff:
            type: int
            Number of posts to show, default=5.
        engagement_rate:
            type: str
            Determines the column of engagement rate for the computations,
            default='engagement_rate_by_post'
        **kwargs:
            account_ids:
                type: list
                Ids of the accounts to look for.
                If [] takes all the posts in the DataFrame posts.
            account_names:
                type: list
                Name of the accounts to look for.
                If [] takes all the posts in the DataFrame posts.

        Returns
        -------
        DataFrame
        """

        method_name = "posts"

        df_most_eff_posts = self.df_posts_full

        if "account_ids" in kwargs.keys() and kwargs["account_ids"]:
            account_ids = kwargs["account_ids"]
            df_most_eff_posts = df_most_eff_posts[
                df_most_eff_posts[self.page_id].isin(account_ids)
            ][
                [
                    self.page_id,
                    self.page_name,
                    self.post_id,
                    self.message,
                    engagement_rate,
                    "rel_" + engagement_rate,
                    # "permalink_url",
                ]
            ]
        elif "account_names" in kwargs.keys() and kwargs["account_names"]:
            account_names = kwargs["account_names"]
            df_most_eff_posts = df_most_eff_posts[
                df_most_eff_posts.page_name.isin(account_names)
            ][
                [
                    self.page_id,
                    self.page_name,
                    self.post_id,
                    self.message,
                    engagement_rate,
                    "rel_" + engagement_rate,
                    # "permalink_url",
                ]
            ]
        else:
            df_most_eff_posts = deepcopy(
                df_most_eff_posts[
                    [
                        self.page_id,
                        self.page_name,
                        self.post_id,
                        self.message,
                        engagement_rate,
                        "rel_" + engagement_rate,
                        # "permalink_url",
                    ]
                ]
            )

        if "search_word" in kwargs.keys() and kwargs["search_word"]:
            search_word = kwargs["search_word"]
            search_word_regex = '|'.join(search_word)
            df_most_eff_posts = df_most_eff_posts.dropna(subset=[self.message])
            df_most_eff_posts = df_most_eff_posts[
                df_most_eff_posts[self.message].str.lower().str.contains(
                    search_word_regex,
                    regex=True)
            ][
                [
                    self.page_id,
                    self.page_name,
                    self.post_id,
                    self.message,
                    engagement_rate,
                    "rel_" + engagement_rate,
                    # "permalink_url",
                ]
            ]
        try:
            df_most_eff_posts = df_most_eff_posts.sort_values(
                engagement_rate, ascending=False
            ).head(n_most_eff)

            return df_most_eff_posts

        except Exception as e:
            exception_type = sys.exc_info()[0]
            print(ERR_SYS + str(exception_type))
            print(e)
            print(f"Class: {self.__str__()}\nMethod: {method_name}\n")
            return pd.DataFrame(
                columns=[
                    self.page_id,
                    self.page_name,
                    self.post_id,
                    self.message,
                    engagement_rate,
                    "rel_" + engagement_rate,
                    # "permalink_url",
                ]
            )

    def posts_type(
        self,
        from_n_most_eff=None,
        engagement_rate="engagement_rate_by_post",
        grouped=False,
        **kwargs,
    ):
        """
        This function computes the DataFrame 'df_most_eff_posts_type_tw'
        which contains for each media type its proportion to the whole number of posts
        and its average engagement rate.

        Parameters
        ----------
        from_n_most_eff:
            type: int
            Number of posts to compute the ratios from, default=None means
            the computations is against all posts.
        engagement_rate:
            type: str
            Determines the column of engagement rate for the computations,
            default='engagement_rate_by_post'
        grouped:
            type: bool
            Determines if the output is returned grouped by group or account,
            default=True.
        **kwargs:
            account_ids:
                type: list
                Ids of the accounts to look for.
                If [] takes all the posts in the DataFrame posts.
            account_names:
                type: list
                Name of the accounts to look for.
                If [] takes all the posts in the DataFrame posts.

        Returns
        -------
        DataFrame
        """

        method_name = "posts_type"

        if not from_n_most_eff:
            from_n_most_eff = self.len_posts_full

        PAGE_COLUMNS = []
        if not grouped:
            PAGE_COLUMNS = [self.page_id, self.page_name]

        df_most_eff_posts_type = self.df_posts_full

        if "account_ids" in kwargs.keys() and kwargs["account_ids"]:
            account_ids = kwargs["account_ids"]
            df_most_eff_posts_type = df_most_eff_posts_type[
                df_most_eff_posts_type[self.page_id].isin(account_ids)
            ][
                PAGE_COLUMNS
                + [self.type, self.message, engagement_rate, "rel_" + engagement_rate]
            ]
        elif "account_names" in kwargs.keys() and kwargs["account_names"]:
            account_names = kwargs["account_names"]
            df_most_eff_posts_type = df_most_eff_posts_type[
                df_most_eff_posts_type.page_name.isin(account_names)
            ][
                PAGE_COLUMNS
                + [self.type, self.message, engagement_rate, "rel_" + engagement_rate]
            ]
        else:
            df_most_eff_posts_type = deepcopy(
                df_most_eff_posts_type[
                    PAGE_COLUMNS
                    + [self.type, self.message, engagement_rate, "rel_" + engagement_rate]
                ]
            )

        if "search_word" in kwargs.keys() and kwargs["search_word"]:
            search_word = kwargs["search_word"]
            search_word_regex = '|'.join(search_word)
            df_most_eff_posts_type = df_most_eff_posts_type.dropna(subset=[self.message])
            df_most_eff_posts_type = df_most_eff_posts_type[
                df_most_eff_posts_type[self.message].str.lower().str.contains(
                    search_word_regex,
                    regex=True)
            ][
                PAGE_COLUMNS
                + [self.type, self.message, engagement_rate, "rel_" + engagement_rate]
            ]

        try:
            df_most_eff_posts_type = df_most_eff_posts_type.sort_values(
                engagement_rate, ascending=False
            ).head(from_n_most_eff)

            df_most_eff_posts_type["message_count"] = 1
            df_most_eff_posts_type = (
                df_most_eff_posts_type[
                    PAGE_COLUMNS
                    + [
                        self.type,
                        "message_count",
                        engagement_rate,
                        "rel_" + engagement_rate,
                    ]
                ]
                .groupby(PAGE_COLUMNS + [self.type])
                .agg(
                    {
                        "message_count": "count",
                        engagement_rate: "mean",
                        "rel_" + engagement_rate: "mean",
                    }
                )
            )
            df_most_eff_posts_type = df_most_eff_posts_type.rename(
                columns={
                    "message_count": "counts",
                    engagement_rate: "avg_engagement_rate",
                    "rel_" + engagement_rate: "avg_rel_engagement_rate",
                }
            )
            if PAGE_COLUMNS:
                df_most_eff_posts_type["percentage"] = (
                    df_most_eff_posts_type["counts"]
                    .groupby(level=0)
                    .apply(lambda c: 100.0 * c / float(c.sum()))
                    .round(2)
                )
                df_most_eff_posts_type = (
                    df_most_eff_posts_type.reset_index().rename(
                        columns={
                            PAGE_COLUMNS[0]: "_object_id",
                            PAGE_COLUMNS[1]: "_object_name",
                        }
                    )
                )
                PAGE_COLUMNS = ["_object_id", "_object_name"]
            else:
                df_most_eff_posts_type["percentage"] = (
                    100.0
                    * df_most_eff_posts_type["counts"]
                    / df_most_eff_posts_type["counts"].sum()
                ).round(2)
                df_most_eff_posts_type = df_most_eff_posts_type.reset_index()

            return df_most_eff_posts_type.sort_values(
                PAGE_COLUMNS + ["avg_engagement_rate"], ascending=False
            )

        except Exception as e:
            exception_type = sys.exc_info()[0]
            print(ERR_SYS + str(exception_type))
            print(e)
            print(f"Class: {self.__str__()}\nMethod: {method_name}\n")
            if PAGE_COLUMNS:
                PAGE_COLUMNS = ["_object_id", "_object_name"]
            return pd.DataFrame(
                columns=[
                    "type",
                    "counts",
                    "avg_engagement_rate",
                    "avg_rel_engagement_rate",
                    "percentage",
                ]
            )

    def construct_most_eff_objects(
        self,
        df_most_eff_objects,
        objs,
        engagement_rate="engagement_rate_by_post",
        grouped=False,
        sort_column="engagement_rate_by_post",
    ):
        """
        This function computes the output DataFrame for words, hashtags or mentions
        with their respective count and engagement rate.

        Parameters
        ----------
        df_most_eff_objects:
            type: DataFrame
            DataFrame with objects (hashtags or mentions) to extract.
        objs:
            type: str
            Objects (hashtags or mentions) to compute the DataFrame.
        engagement_rate:
            type: str
            Determines the column of engagement rate for the computations,
            default='engagement_rate_by_post'.
        grouped:
            type: bool
            Determines if the output is returned grouped by group or account,
            default=True.
        sort_column:
            Column to sort the output DataFrame,
            default='engagement_rate_by_post'.

        Returns
        -------
        DataFrames
        """

        method_name = "construct_most_eff_objects"

        PAGE_COLUMNS = []
        if not grouped:
            PAGE_COLUMNS = [self.page_id, self.page_name]

        try:
            objs_list = []
            objs_eff = []
            objs_rel_eff = []
            if PAGE_COLUMNS:
                objs_ids = []
                objs_names = []
            objs_counts = []

            for _, row in df_most_eff_objects.iterrows():
                if self.s_net == 'ig':
                    caption_ = "caption_"
                else:
                    caption_ = ""

                objs_list = objs_list + row[caption_ + objs]
                objs_eff = objs_eff + [row[engagement_rate]] * len(
                    row[caption_ + objs]
                )
                objs_rel_eff = objs_rel_eff + [
                    row["rel_" + engagement_rate]
                ] * len(row[caption_ + objs])

                if PAGE_COLUMNS:
                    objs_ids = objs_ids + [row[PAGE_COLUMNS[0]]] * len(
                        row[caption_ + objs]
                    )
                    objs_names = objs_names + [row[PAGE_COLUMNS[1]]] * len(
                        row[caption_ + objs]
                    )

                objs_counts = objs_counts + [1] * len(row[caption_ + objs])

            if self.s_net == 'tw':
                objs = objs[:-1].split("_")[-1]
                most_eff_objs = pd.DataFrame(
                    {
                        objs: objs_list,
                        engagement_rate: objs_eff,
                        "rel_" + engagement_rate: objs_rel_eff,
                        f"{objs}_count": objs_counts,
                    }
                )
            else:
                most_eff_objs = pd.DataFrame(
                    {
                        objs[:-1]: objs_list,
                        engagement_rate: objs_eff,
                        "rel_" + engagement_rate: objs_rel_eff,
                        f"{objs[:-1]}_count": objs_counts,
                    }
                )

            if PAGE_COLUMNS:
                most_eff_objs[PAGE_COLUMNS[0]] = objs_ids
                most_eff_objs[PAGE_COLUMNS[1]] = objs_names

            if self.s_net == 'tw':
                most_eff_objs = (
                    most_eff_objs.groupby(PAGE_COLUMNS + [objs])
                        .agg(
                        {
                            engagement_rate: "mean",
                            "rel_" + engagement_rate: "mean",
                            f"{objs}_count": "sum",
                        }
                    )
                        .sort_values(PAGE_COLUMNS + [sort_column], ascending=False)
                        .reset_index()
                )
            else:
                most_eff_objs = (
                    most_eff_objs.groupby(PAGE_COLUMNS + [objs[:-1]])
                    .agg(
                        {
                            engagement_rate: "mean",
                            "rel_" + engagement_rate: "mean",
                            f"{objs[:-1]}_count": "sum",
                        }
                    )
                    .sort_values(PAGE_COLUMNS + [sort_column], ascending=False)
                    .reset_index()
                )

            return most_eff_objs

        except Exception as e:
            exception_type = sys.exc_info()[0]
            print(ERR_SYS + str(exception_type))
            print(e)
            print(f"Class: {self.__str__()}\nMethod: {method_name}\n")
            most_eff_objs = pd.DataFrame(
                columns=PAGE_COLUMNS
                + [
                    objs[:-1],
                    engagement_rate,
                    "rel_" + engagement_rate,
                    f"{objs[:-1]}_count",
                ]
            )

            return most_eff_objs

    def hashtags_mentions(
        self,
        from_n_most_eff=None,
        engagement_rate="engagement_rate_by_post",
        grouped=False,
        **kwargs,
    ):
        """
        This function computes the following DataFrames:
          - 'most_eff_hashtags' and 'most_eff_mentions'
            which contains the hastags and mentions with higher associated
            engagement rate for the accounts selected.

          - 'compare_hashtags' and 'compare_mentions'
            which contains the most used hastags and mentions for the account
            to compare with.

        Parameters
        ----------
        compare_group:
            type: str
            Name of the group to compare with. default='brand'.
        from_n_most_eff:
            type: int
            Number of posts to compute the ratios from, default=None means
            the computations is against all posts.
        engagement_rate:
            type: str
            Determines the column of engagement rate for the computations,
            default='engagement_rate_by_post'.
        grouped:
            type: bool
            Determines if the output is returned grouped by group or account,
            default=True.
        **kwargs:
            account_ids:
                type: list
                Ids of the accounts to look for.
                If [] takes all the posts in the DataFrame posts.
            account_names:
                type: list
                Name of the accounts to look for.
                If [] takes all the posts in the DataFrame posts.

        Returns
        -------
        Tuple of DataFrames
        """

        method_name = "hashtags_mentions"

        if not from_n_most_eff:
            from_n_most_eff = self.len_posts_full

        PAGE_COLUMNS = []
        if not grouped:
            PAGE_COLUMNS = [self.page_id, self.page_name]

        df_most_eff_hashtags_mentions = self.df_posts_full

        if "search_word" in kwargs.keys() and kwargs["search_word"]:
            search_word = kwargs["search_word"]
            search_word_regex = '|'.join(search_word)
            df_most_eff_hashtags_mentions = df_most_eff_hashtags_mentions.dropna(subset=[self.message])
            df_most_eff_hashtags_mentions = df_most_eff_hashtags_mentions[
                df_most_eff_hashtags_mentions[self.message].str.lower().str.contains(
                    search_word_regex,
                    regex=True)
            ]

        if "account_ids" in kwargs.keys() and kwargs["account_ids"]:
            if self.s_net == 'fb':
                account_ids = kwargs["account_ids"]
                df_most_eff_hashtags_mentions = df_most_eff_hashtags_mentions[
                    df_most_eff_hashtags_mentions[self.page_id].isin(account_ids)
                ][
                    PAGE_COLUMNS
                    + [self.message_tags,
                       engagement_rate,
                       "rel_" + engagement_rate]
                ]
            else:
                account_ids = kwargs["account_ids"]
                df_most_eff_hashtags_mentions = df_most_eff_hashtags_mentions[
                    df_most_eff_hashtags_mentions[self.page_id].isin(account_ids)
                ][
                    PAGE_COLUMNS
                    + [self.hashtags,
                       self.message_tags,
                       engagement_rate,
                       "rel_" + engagement_rate]
                    ]
        elif "account_names" in kwargs.keys() and kwargs["account_names"]:
            account_names = kwargs["account_names"]
            df_most_eff_hashtags_mentions = df_most_eff_hashtags_mentions[
                df_most_eff_hashtags_mentions[self.page_id].isin(account_names)
            ][
                PAGE_COLUMNS
                + [self.message_tags, engagement_rate, "rel_" + engagement_rate]
            ]
        else:
            if self.s_net != 'fb':
                df_most_eff_hashtags_mentions = deepcopy(
                    df_most_eff_hashtags_mentions[
                        PAGE_COLUMNS
                        + [
                            self.hashtags,
                            self.message_tags,
                            engagement_rate,
                            "rel_" + engagement_rate,
                        ]
                    ]
                )
            else:
                df_most_eff_hashtags_mentions = deepcopy(
                    df_most_eff_hashtags_mentions[
                        PAGE_COLUMNS
                        + [
                            self.message_tags,
                            engagement_rate,
                            "rel_" + engagement_rate,
                        ]
                    ]
                )

        if self.s_net == 'fb':
            df_compare_hashtags_mentions = df_most_eff_hashtags_mentions[
                PAGE_COLUMNS
                + [self.message_tags,
                   engagement_rate,
                   "rel_" + engagement_rate]
            ]
        else:
            df_compare_hashtags_mentions = df_most_eff_hashtags_mentions[
                PAGE_COLUMNS
                + [self.hashtags,
                   self.message_tags,
                   engagement_rate,
                   "rel_" + engagement_rate]
                ]

        try:
            if self.s_net == 'fb':
                df_most_eff_hashtags_mentions = df_most_eff_hashtags_mentions[
                    ~df_most_eff_hashtags_mentions[self.message_tags].isna()
                ]

                df_most_eff_hashtags_mentions = df_most_eff_hashtags_mentions[
                    (
                            (df_most_eff_hashtags_mentions[self.message_tags] != "None")
                            & (df_most_eff_hashtags_mentions[self.message_tags] != "[]")
                    )
                ]
                df_most_eff_hashtags_mentions[self.message_tags] = (
                    df_most_eff_hashtags_mentions[self.message_tags].apply(
                        lambda _json: ast.literal_eval(_json)
                    )
                )

                df_most_eff_hashtags_mentions[
                    "mentions"
                ] = df_most_eff_hashtags_mentions[self.message_tags].apply(
                    lambda tags: [
                        tag["name"] for tag in tags if not re.search(r"^#.*", tag["name"])
                    ]
                )
                df_most_eff_hashtags_mentions[
                    "mentions"
                ] = df_most_eff_hashtags_mentions["mentions"].apply(
                    lambda ments: ments if ments else None
                )

                df_most_eff_hashtags_mentions[
                    "hashtags"
                ] = df_most_eff_hashtags_mentions[self.message_tags].apply(
                    lambda tags: [
                        tag["name"] for tag in tags if re.search(r"^#.*", tag["name"])
                    ]
                )
                df_most_eff_hashtags_mentions[
                    "hashtags"
                ] = df_most_eff_hashtags_mentions["hashtags"].apply(
                    lambda hashs: hashs if hashs else None
                )

                df_compare_hashtags_mentions = df_compare_hashtags_mentions[
                    ~df_compare_hashtags_mentions[self.message_tags].isna()
                ]
                df_compare_hashtags_mentions = df_compare_hashtags_mentions[
                    (
                            (df_compare_hashtags_mentions[self.message_tags] != "None")
                            & (df_compare_hashtags_mentions[self.message_tags] != "[]")
                    )
                ]
                df_compare_hashtags_mentions[self.message_tags] = (
                    df_compare_hashtags_mentions[self.message_tags].apply(
                        lambda _json: ast.literal_eval(_json)
                    )
                )

                df_compare_hashtags_mentions[
                    "mentions"
                ] = df_compare_hashtags_mentions[self.message_tags].apply(
                    lambda tags: [
                        tag["name"] for tag in tags if not re.search(r"^#.*", tag["name"])
                    ]
                )
                df_compare_hashtags_mentions[
                    "mentions"
                ] = df_compare_hashtags_mentions["mentions"].apply(
                    lambda ments: ments if ments else None
                )

                df_compare_hashtags_mentions[
                    "hashtags"
                ] = df_compare_hashtags_mentions[self.message_tags].apply(
                    lambda tags: [
                        tag["name"] for tag in tags if re.search(r"^#.*", tag["name"])
                    ]
                )
                df_compare_hashtags_mentions[
                    "hashtags"
                ] = df_compare_hashtags_mentions["hashtags"].apply(
                    lambda hashs: hashs if hashs else None
                )
            elif self.s_net == 'ig':

                df_most_eff_hashtags_mentions[
                    "caption_hashtags"
                ] = df_most_eff_hashtags_mentions["caption_hashtags"].apply(
                    lambda hashtags: json.loads(hashtags)
                )
                df_most_eff_hashtags_mentions[
                    "caption_hashtags"
                ] = df_most_eff_hashtags_mentions["caption_hashtags"].apply(
                    lambda hashtags: hashtags if hashtags else None
                )

                df_most_eff_hashtags_mentions[
                    "caption_mentions"
                ] = df_most_eff_hashtags_mentions["caption_mentions"].apply(
                    lambda mentions: json.loads(mentions)
                )
                df_most_eff_hashtags_mentions[
                    "caption_mentions"
                ] = df_most_eff_hashtags_mentions["caption_mentions"].apply(
                    lambda mentions: mentions if mentions else None
                )

                df_compare_hashtags_mentions[
                    "caption_hashtags"
                ] = df_compare_hashtags_mentions["caption_hashtags"].apply(
                    lambda hashtags: json.loads(hashtags)
                )
                df_compare_hashtags_mentions[
                    "caption_hashtags"
                ] = df_compare_hashtags_mentions["caption_hashtags"].apply(
                    lambda hashtags: hashtags if hashtags else None
                )

                df_compare_hashtags_mentions[
                    "caption_mentions"
                ] = df_compare_hashtags_mentions["caption_mentions"].apply(
                    lambda mentions: json.loads(mentions)
                )
                df_compare_hashtags_mentions[
                    "caption_mentions"
                ] = df_compare_hashtags_mentions["caption_mentions"].apply(
                    lambda mentions: mentions if mentions else None
                )

                df_most_eff_hashtags_mentions = (
                    df_most_eff_hashtags_mentions.sort_values(
                        engagement_rate, ascending=False
                    ).head(from_n_most_eff)
                )
                df_compare_hashtags_mentions = (
                    df_compare_hashtags_mentions.sort_values(
                        engagement_rate, ascending=False
                    ).head(from_n_most_eff)
                )

            elif self.s_net == 'tw':

                df_most_eff_hashtags_mentions[
                    "hashtags"
                ] = df_most_eff_hashtags_mentions["hashtags"].fillna('')
                df_most_eff_hashtags_mentions[
                    "user_mentions"
                ] = df_most_eff_hashtags_mentions["user_mentions"].fillna('')

                df_compare_hashtags_mentions[
                    "hashtags"
                ] = df_compare_hashtags_mentions["hashtags"].fillna('')
                df_compare_hashtags_mentions[
                    "user_mentions"
                ] = df_compare_hashtags_mentions["user_mentions"].fillna('')

                df_most_eff_hashtags_mentions[
                    "hashtags"
                ] = df_most_eff_hashtags_mentions["hashtags"].apply(
                    lambda hashtags: hashtags.split(",") if hashtags else None
                )
                df_most_eff_hashtags_mentions[
                    "user_mentions"
                ] = df_most_eff_hashtags_mentions["user_mentions"].apply(
                    lambda mentions: mentions.split(",") if mentions else None
                )
                df_compare_hashtags_mentions[
                    "hashtags"
                ] = df_compare_hashtags_mentions["hashtags"].apply(
                    lambda hashtags: hashtags.split(",") if hashtags else None
                )
                df_compare_hashtags_mentions[
                    "user_mentions"
                ] = df_compare_hashtags_mentions["user_mentions"].apply(
                    lambda mentions: mentions.split(",") if mentions else None
                )

                df_most_eff_hashtags_mentions = (
                    df_most_eff_hashtags_mentions.sort_values(
                        engagement_rate, ascending=False
                    ).head(from_n_most_eff)
                )

                df_compare_hashtags_mentions = (
                    df_compare_hashtags_mentions.sort_values(
                        engagement_rate, ascending=False
                    ).head(from_n_most_eff)
                )

            else:
                print(f'{self.s_net} social network not valid')
            df_most_eff_hashtags_mentions = (
                df_most_eff_hashtags_mentions.sort_values(
                    engagement_rate, ascending=False
                ).head(from_n_most_eff)
            )
            df_compare_hashtags_mentions = (
                df_compare_hashtags_mentions.sort_values(
                    engagement_rate, ascending=False
                ).head(from_n_most_eff)
            )
            # Hashtags
            df_most_eff_hashtags = df_most_eff_hashtags_mentions[
                ~df_most_eff_hashtags_mentions[self.hashtags].isna()
            ]
            most_eff_hashtags = self.construct_most_eff_objects(
                df_most_eff_hashtags, objs="hashtags", grouped=grouped
            )

            # Group to compare with
            df_compare_hashtags = df_compare_hashtags_mentions[
                ~df_compare_hashtags_mentions[self.hashtags].isna()
            ]
            compare_hashtags = self.construct_most_eff_objects(
                df_compare_hashtags,
                objs="hashtags",
                grouped=grouped,
                sort_column="hashtag_count",
            )

            # Mentions
            if self.s_net == 'fb':
                df_most_eff_mentions = df_most_eff_hashtags_mentions[
                    ~df_most_eff_hashtags_mentions["mentions"].isna()
                ]
            else:
                df_most_eff_mentions = df_most_eff_hashtags_mentions[
                    ~df_most_eff_hashtags_mentions[self.message_tags].isna()
                ]
            if self.s_net == 'tw':
                mentions_ = "user_mentions"
            else:
                mentions_ = "mentions"

            most_eff_mentions = self.construct_most_eff_objects(
                df_most_eff_mentions, objs=mentions_, grouped=grouped
            )

            # Group to compare with
            if self.s_net == "fb":
                df_compare_mentions = df_compare_hashtags_mentions[
                    ~df_compare_hashtags_mentions[mentions_].isna()
                ]
            else:
                df_compare_mentions = df_compare_hashtags_mentions[
                    ~df_compare_hashtags_mentions[self.message_tags].isna()
                ]
            compare_mentions = self.construct_most_eff_objects(
                df_compare_mentions,
                objs=mentions_,
                grouped=grouped,
                sort_column="mention_count",
            )

            if PAGE_COLUMNS:
                most_eff_hashtags = most_eff_hashtags.rename(
                    columns={
                        PAGE_COLUMNS[0]: "_object_id",
                        PAGE_COLUMNS[1]: "_object_name",
                    }
                )
                compare_hashtags = compare_hashtags.rename(
                    columns={
                        PAGE_COLUMNS[0]: "_object_id",
                        PAGE_COLUMNS[1]: "_object_name",
                    }
                )
                most_eff_mentions = most_eff_mentions.rename(
                    columns={
                        PAGE_COLUMNS[0]: "_object_id",
                        PAGE_COLUMNS[1]: "_object_name",
                    }
                )
                compare_mentions = compare_mentions.rename(
                    columns={
                        PAGE_COLUMNS[0]: "_object_id",
                        PAGE_COLUMNS[1]: "_object_name",
                    }
                )
                PAGE_COLUMNS = ["_object_id", "_object_name"]

            return (
                most_eff_hashtags,
                compare_hashtags,
                most_eff_mentions,
                compare_mentions,
            )

        except Exception as e:
            exception_type = sys.exc_info()[0]
            print(ERR_SYS + str(exception_type))
            print(e)
            print(f"Class: {self.__str__()}\nMethod: {method_name}\n")
            if PAGE_COLUMNS:
                PAGE_COLUMNS = ["_object_id", "_object_name"]
            most_eff_hashtags = pd.DataFrame(
                columns=[
                    "hashtag",
                    engagement_rate,
                    "rel_" + engagement_rate,
                    "hashtag_count",
                ]
            )
            compare_hashtags = pd.DataFrame(
                columns=[
                    "hashtag",
                    engagement_rate,
                    "rel_" + engagement_rate,
                    "hashtag_count",
                ]
            )
            most_eff_mentions = pd.DataFrame(
                columns=[
                    "mention",
                    engagement_rate,
                    "rel_" + engagement_rate,
                    "mention_count",
                ]
            )
            compare_mentions = pd.DataFrame(
                columns=[
                    "mention",
                    engagement_rate,
                    "rel_" + engagement_rate,
                    "mention_count",
                ]
            )
            return (
                most_eff_hashtags,
                compare_hashtags,
                most_eff_mentions,
                compare_mentions,
            )

    def construct_most_eff_words(
        self,
        df_most_eff_words,
        lemmatize=False,
        engagement_rate="engagement_rate_by_post",
        grouped=False,
        min_count=2,
    ):
        """
        This function computes the output DataFrame for words, hashtags or mentions
        with their respective count and engagement rate.

        Parameters
        ----------
        df_most_eff_objects:
            type: DataFrame
            DataFrame with words to extract.
        lemmatize:
            type: bool
            True if the lemmas are desired instead of words. default=False.
        engagement_rate:
            type: str
            Determines the column of engagement rate for the computations,
            default='engagement_rate_by_post'.
        grouped:
            type: bool
            Determines if the output is returned grouped by group or account,
            default=True.
        min_count:
            type: int
            Minimum number of counts on the word to consider in the analysis.

        Returns
        -------
        DataFrames
        """

        method_name = "construct_most_eff_words"

        PAGE_COLUMNS = []
        if not grouped:
            PAGE_COLUMNS = [self.page_id, self.page_name]

        try:
            words = []
            lemmas = []
            pos_tags = []
            words_counts = []
            words_eff = []
            words_rel_eff = []
            if PAGE_COLUMNS:
                words_ids = []
                words_names = []
            for _, row in df_most_eff_words.iterrows():
                words = words + row.words
                lemmas = lemmas + row.lemmas
                pos_tags = pos_tags + row.pos_tags
                words_counts = words_counts + [1] * len(row.words)
                words_eff = words_eff + [row[engagement_rate]] * len(row.words)
                words_rel_eff = words_rel_eff + [
                    row["rel_" + engagement_rate]
                ] * len(row.words)
                if PAGE_COLUMNS:
                    words_ids = words_ids + [row[PAGE_COLUMNS[0]]] * len(
                        row.words
                    )
                    words_names = words_names + [row[PAGE_COLUMNS[1]]] * len(
                        row.words
                    )

            most_eff_words = pd.DataFrame(
                {
                    "word": words,
                    "lemma": lemmas,
                    "pos_tag": pos_tags,
                    "word_count": words_counts,
                    engagement_rate: words_eff,
                    "rel_" + engagement_rate: words_rel_eff,
                }
            )

            if PAGE_COLUMNS:
                most_eff_words[PAGE_COLUMNS[0]] = words_ids
                most_eff_words[PAGE_COLUMNS[1]] = words_names

            if lemmatize:
                word_column = "lemma"
            else:
                word_column = "word"
            most_eff_words = (
                most_eff_words[
                    PAGE_COLUMNS
                    + [
                        "pos_tag",
                        word_column,
                        "word_count",
                        engagement_rate,
                        "rel_" + engagement_rate,
                    ]
                ]
                .groupby(PAGE_COLUMNS + ["pos_tag", word_column])
                .agg(
                    {
                        engagement_rate: "mean",
                        "rel_" + engagement_rate: "mean",
                        "word_count": "sum",
                    }
                )
            )
            most_eff_words = most_eff_words[
                most_eff_words["word_count"] >= min_count
            ]

            most_eff_words = most_eff_words.sort_values(
                PAGE_COLUMNS + ["pos_tag", engagement_rate], ascending=False
            ).reset_index()

            most_eff_nouns = most_eff_words[
                most_eff_words["pos_tag"] == "NOUN"
            ]
            most_eff_verbs = most_eff_words[
                most_eff_words["pos_tag"] == "VERB"
            ]
            most_eff_adjs = most_eff_words[most_eff_words["pos_tag"] == "ADJ"]

            return (
                most_eff_words,
                most_eff_nouns,
                most_eff_verbs,
                most_eff_adjs,
            )

        except Exception as e:
            exception_type = sys.exc_info()[0]
            print(ERR_SYS + str(exception_type))
            print(e)
            print(f"Class: {self.__str__()}\nMethod: {method_name}\n")
            if lemmatize:
                word_column = "lemma"
            else:
                word_column = "word"
            most_eff_words = pd.DataFrame(
                columns=PAGE_COLUMNS
                + [
                    "pos_tag",
                    word_column,
                    "word_count",
                    engagement_rate,
                    "rel_" + engagement_rate,
                ]
            )
            show_columns = PAGE_COLUMNS + [
                "word",
                engagement_rate,
                "rel_" + engagement_rate,
                "word_count",
            ]
            most_eff_nouns = pd.DataFrame(columns=show_columns)
            most_eff_verbs = pd.DataFrame(columns=show_columns)
            most_eff_adjs = pd.DataFrame(columns=show_columns)
            return (
                most_eff_words,
                most_eff_nouns,
                most_eff_verbs,
                most_eff_adjs,
            )

    def words(
        self,
        lemmatize=False,
        from_n_most_eff=None,
        min_count=2,
        engagement_rate="engagement_rate_by_post",
        grouped=False,
        **kwargs,
    ):
        """
        This function computes the following DataFrames:
          - 'most_eff_words'
            which contains the words with higher associated
            engagement rate for the accounts selected, it is tagged with
            the part of speech tag of the word.

          - most_eff_nouns, most_eff_verbs and most_eff_adjs
            which contains the nouns, verbs and adjectives with higher associated
            engagement rate for the accounts selected, it is tagged with
            the part of speech tag of the word.

        Parameters
        ----------
        lemmatize:
            type: bool
            True if the lemmas are desired instead of words. default=False.
        from_n_most_eff:
            type: int
            Number of posts to compute the ratios from, default=None means
            the computations is against all posts.
        min_count:
            type: int
            Minimum number of counts on the word to consider in the analysis.
        engagement_rate:
            type: str
            Determines the column of engagement rate for the computations,
            default='engagement_rate_by_post'.
        grouped:
            type: bool
            Determines if the output is returned grouped by group or account,
            default=True.
        **kwargs:
            account_ids:
                type: list
                Ids of the accounts to look for.
                If [] takes all the posts in the DataFrame posts.
            account_names:
                type: list
                Name of the accounts to look for.
                If [] takes all the posts in the DataFrame posts.

        Returns
        -------
        Tuple of DataFrames
        """

        method_name = "words"

        if not self.features:
            self.features = Features()

        if not from_n_most_eff:
            from_n_most_eff = self.len_posts_full

        PAGE_COLUMNS = []
        if not grouped:
            PAGE_COLUMNS = [self.page_id, self.page_name]

        if "account_ids" in kwargs.keys() and kwargs["account_ids"]:
            account_ids = kwargs["account_ids"]
            df_most_eff_words = self.df_posts_full[
                self.df_posts_full.page_id.isin(account_ids)
            ][
                PAGE_COLUMNS
                + [self.message, engagement_rate, "rel_" + engagement_rate]
            ]
        elif "account_names" in kwargs.keys() and kwargs["account_names"]:
            account_names = kwargs["account_names"]
            df_most_eff_words = self.df_posts_full[
                self.df_posts_full.page_name.isin(account_names)
            ][
                PAGE_COLUMNS
                + [self.message, engagement_rate, "rel_" + engagement_rate]
            ]
        else:
            df_most_eff_words = deepcopy(
                self.df_posts_full[
                    PAGE_COLUMNS
                    + [self.message, engagement_rate, "rel_" + engagement_rate]
                ]
            )

        try:
            df_most_eff_words = df_most_eff_words.sort_values(
                engagement_rate, ascending=False
            ).head(from_n_most_eff)

            if "processed_text" not in df_most_eff_words.keys():
                df_most_eff_words[
                    "processed_text"
                ] = df_most_eff_words[self.message].apply(
                    lambda msg: CleanText(msg).process_text(
                        mentions=True, hashtags=True, links=True, spec_chars=True
                    )
                )
            df_most_eff_words["processed_text"] = df_most_eff_words[
                "processed_text"
            ].apply(lambda txt: self.features.pos_tags(txt))

            df_most_eff_words["words"] = df_most_eff_words[
                "processed_text"
            ].apply(lambda pt: pt["words"])
            df_most_eff_words["lemmas"] = df_most_eff_words[
                "processed_text"
            ].apply(lambda pt: pt["lemmas"])
            df_most_eff_words["pos_tags"] = df_most_eff_words[
                "processed_text"
            ].apply(lambda pt: pt["pos_tags"])

            df_most_eff_words = df_most_eff_words[
                ~df_most_eff_words["processed_text"].isna()
            ]

            (
                most_eff_words,
                most_eff_nouns,
                most_eff_verbs,
                most_eff_adjs,
            ) = self.construct_most_eff_words(
                df_most_eff_words,
                lemmatize=lemmatize,
                engagement_rate=engagement_rate,
                grouped=grouped,
                min_count=min_count,
            )

            if PAGE_COLUMNS:
                most_eff_words = most_eff_words.rename(
                    columns={
                        PAGE_COLUMNS[0]: "_object_id",
                        PAGE_COLUMNS[1]: "_object_name",
                    }
                )
                most_eff_nouns = most_eff_nouns.rename(
                    columns={
                        PAGE_COLUMNS[0]: "_object_id",
                        PAGE_COLUMNS[1]: "_object_name",
                    }
                )
                most_eff_verbs = most_eff_verbs.rename(
                    columns={
                        PAGE_COLUMNS[0]: "_object_id",
                        PAGE_COLUMNS[1]: "_object_name",
                    }
                )
                most_eff_adjs = most_eff_adjs.rename(
                    columns={
                        PAGE_COLUMNS[0]: "_object_id",
                        PAGE_COLUMNS[1]: "_object_name",
                    }
                )
                PAGE_COLUMNS = ["_object_id", "_object_name"]

            show_columns = PAGE_COLUMNS + [
                "word",
                engagement_rate,
                "rel_" + engagement_rate,
                "word_count",
            ]

            return (
                most_eff_words,
                most_eff_nouns[show_columns],
                most_eff_verbs[show_columns],
                most_eff_adjs[show_columns],
            )

        except Exception as e:
            exception_type = sys.exc_info()[0]
            print(ERR_SYS + str(exception_type))
            print(e)
            print(f"Class: {self.__str__()}\nMethod: {method_name}\n")
            if PAGE_COLUMNS:
                PAGE_COLUMNS = ["_object_id", "_object_name"]
            most_eff_words = pd.DataFrame(
                columns=PAGE_COLUMNS
                + [
                    "pos_tag",
                    "word",
                    "word_count",
                    engagement_rate,
                    "rel_" + engagement_rate,
                ]
            )
            show_columns = PAGE_COLUMNS + [
                "word",
                engagement_rate,
                "rel_" + engagement_rate,
                "word_count",
            ]
            most_eff_nouns = pd.DataFrame(columns=show_columns)
            most_eff_verbs = pd.DataFrame(columns=show_columns)
            most_eff_adjs = pd.DataFrame(columns=show_columns)
            return (
                most_eff_words,
                most_eff_nouns,
                most_eff_verbs,
                most_eff_adjs,
            )
