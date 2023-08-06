import re
import sys
import pandas as pd
from copy import deepcopy
from datetime import timedelta
from bru_analysis.common import general_utils, metric_transformation

ERR_SYS = "\nSystem error: "


def get_name(pid, dict_page_id_to_name):
    try:
        out_name = dict_page_id_to_name[pid]
    except Exception:
        out_name = "no_name"
    return out_name


class EngagementRateFB:
    def __init__(self, df_posts, df_pages):
        """
        This method computes the DataFrame 'df_posts_full' with the columns
        'group' and 'fan_count' which is a count of the fans in the day the post was made.

        Parameters
        ----------
        df_posts:
            type: DataFrame
            this Pandas DataFrame must have columns
            'created_time' and 'page_id'.
        df_pages:
            type: DataFrame
            this Pandas DataFrame must have columns
            'fan_count', 'page_id' and 'created_at'.
        """

        METHOD_NAME = "__init__"

        PAGES_COLUMNS = ["fan_count", "page_id", "created_at"]
        POSTS_COLUMNS = [
            "page_id",
            "created_time",
            "post_id",
            "likes",
            "reactions_love",
            "reactions_wow",
            "reactions_haha",
            "reactions_sad",
            "reactions_angry",
            "reactions_thankful",
            "shares",
            "comments",
            "message",
            "permalink_url",
            "type",
            "message_tags",
        ]
        OUTPUT_COLUMNS = [
            "fan_count",
            "page_id",
            "page_name",
            "date",
            "group",
            "created_time",
            "post_id",
            "likes",
            "reactions_love",
            "reactions_wow",
            "reactions_haha",
            "reactions_sad",
            "reactions_angry",
            "reactions_thankful",
            "shares",
            "comments",
            "message",
            "permalink_url",
            "type",
            "message_tags",
        ]

        if len(df_posts) > 0 and len(df_pages) > 0:
            try:
                df_fan_count = (
                    df_pages[PAGES_COLUMNS]
                    .groupby(["page_id", "created_at"])
                    .last()
                    .reset_index()
                )

                df_fan_count["created_at"] = pd.to_datetime(
                    df_fan_count["created_at"], format="%Y-%m-%dT%H:%M:%S"
                )
                df_fan_count["created_at"] = pd.to_datetime(
                    df_fan_count["created_at"]
                ) - timedelta(hours=5)
                df_fan_count["date"] = df_fan_count["created_at"].dt.date
                df_fan_count = df_fan_count.drop(columns=["created_at"])

                df_posts_full = deepcopy(df_posts[POSTS_COLUMNS])

                page_id_name_fb = {}
                for idd, row in df_pages.iterrows():
                    page_id_name_fb[row.page_id] = row["name"]
                df_posts_full["page_name"] = df_posts_full.page_id.apply(
                    lambda pid: get_name(pid, page_id_name_fb)
                )

                df_posts_full["created_time"] = pd.to_datetime(
                    df_posts_full["created_time"]
                ) - timedelta(hours=5)
                df_posts_full["date"] = df_posts_full["created_time"].dt.date
                df_posts_full = pd.merge(
                    df_posts_full, df_fan_count, on=["page_id"], how="left"
                )
                df_posts_full = df_posts_full.rename(
                    columns={"date_x":"date"}
                )
                df_posts_full = df_posts_full.drop(columns=["date_y"])
                
                df_posts_full["fan_count"] = df_posts_full.sort_values(
                    ["page_id", "date"]
                )["fan_count"].fillna(method="bfill")

                df_posts_full = df_posts_full.sort_values("date").drop_duplicates(
                    subset=["post_id"], keep="last"
                )

                self.df_posts_full = df_posts_full

            except Exception as e:
                exception_type = sys.exc_info()[0]
                print(ERR_SYS + str(exception_type))
                print(e)
                print(f"Class: {self.__str__()}\nMethod: {METHOD_NAME}\n")
                self.df_posts_full = pd.DataFrame(columns=OUTPUT_COLUMNS, dtype=object)

        else:
            print("Warning: One of the DataFrames is empty. It cannot be computed.")
            self.df_posts_full = pd.DataFrame(columns=OUTPUT_COLUMNS, dtype=object)

    def by_post(self):
        """
        This method computes the engagement rate for every post based on the
        number of followers of the account. It stores it on the column
        'engagement_rate_by_post' on the input Pandas DataFrame 'df_posts_full'.

        Returns
        -------
        DataFrame
        """

        METHOD_NAME = "by_post"

        df_posts_full = self.df_posts_full
        try:
            df_posts_full["engagement_rate_by_post"] = df_posts_full.apply(
                lambda row: 100
                * (
                    row.likes
                    + row.reactions_love
                    + row.reactions_wow
                    + row.reactions_haha
                    + row.reactions_sad
                    + row.reactions_angry
                    + row.reactions_thankful
                    + row.shares
                    + row.comments
                )
                / row.fan_count,
                axis=1,
            )

            METRIC = "engagement_rate_by_post"
            ITEM_COLUMN = "page_id"
            df_posts_full = df_posts_full.sort_values(by=["created_time"])
            df_posts_full = metric_transformation.MetricCategorization(
                df_posts_full, METRIC, ITEM_COLUMN
            ).categorize()

            return df_posts_full.dropna(subset=["engagement_rate_by_post"])

        except Exception as e:
            exception_type = sys.exc_info()[0]
            print(ERR_SYS + str(exception_type))
            print(e)
            print(f"Class: {self.__str__()}\nMethod: {METHOD_NAME}\n")
            return pd.DataFrame(
                columns=list(df_posts_full.columns)
                + ["engagement_rate_by_post", "boundary", "rel_engagement_rate_by_post"]
            )


class EngagementRateIG:
    def __init__(self, df_posts, df_pages, mode="status"):
        """
        This method computes the DataFrame 'df_posts_full' with the columns
        'group' and 'followers' which is a count of the fans in the day the post was made.

        Parameters
        ----------
        df_posts:
            type: DataFrame
            this Pandas DataFrame muts have columns
            'owner_id' and 'date_utc'.
        df_pages:
            type: DataFrame
            this Pandas DataFrame muts have columns
            'followers', 'userid' and 'date'.
        """

        METHOD_NAME = "__init__"

        self.mode = mode

        if self.mode == "status":
            PAGES_COLUMNS = ["followers", "userid", "date"]

            POSTS_COLUMNS = [
                "owner_id",
                "owner_username",
                "date_utc",
                "shortcode",
                "likes_count",
                "comment_count",
                "caption_hashtags",
                "typename",
                "caption",
                "mediaid",
            ]
            OUTPUT_COLUMNS = [
                "followers",
                "owner_id",
                "owner_username",
                "group",
                "created_at",
                "shortcode",
                "likes_count",
                "comment_count",
                "caption_hashtags",
                "typename",
                "caption",
            ]

            if len(df_posts) > 0 and len(df_pages) > 0:
                try:
                    df_fan_count = deepcopy(df_pages[PAGES_COLUMNS])
                    df_fan_count["userid"] = df_fan_count["userid"].apply(
                        lambda uid: str(uid)
                    )

                    df_fan_count["date"] = pd.to_datetime(
                        df_fan_count["date"], format="%Y-%m-%dT%H:%M:%S"
                    )
                    df_fan_count["date"] = pd.to_datetime(
                        df_fan_count["date"]
                    ) - timedelta(hours=5)
                    df_fan_count["date"] = df_fan_count["date"].dt.date
                    df_fan_count = (
                        df_fan_count.groupby(["userid", "date"]).last().reset_index()
                    )

                    df_fan_count = df_fan_count.rename(columns={"userid": "owner_id"})

                    df_posts_full = deepcopy(df_posts[POSTS_COLUMNS])
                    df_posts_full["owner_id"] = df_posts_full["owner_id"].apply(
                        lambda uid: str(uid)
                    )

                    df_posts_full["date"] = pd.to_datetime(
                        df_posts_full["date_utc"], format="%Y-%m-%dT%H:%M:%S"
                    )
                    df_posts_full["created_at"] = pd.to_datetime(
                        df_posts_full["date"]
                    ) - timedelta(hours=5)
                    df_posts_full["date"] = pd.to_datetime(
                        df_posts_full["date"]
                    ) - timedelta(hours=5)
                    df_posts_full["date"] = df_posts_full["date"].dt.date
                    df_posts_full = pd.merge(
                        df_posts_full, df_fan_count, on=["owner_id"], how="left"
                    )
                    df_posts_full = df_posts_full.rename(
                        columns={"date_x":"date"}
                    )
                    df_posts_full = df_posts_full.drop(columns=["date_y"])
                    
                    df_posts_full["followers"] = df_posts_full.sort_values(
                        ["owner_id", "date"]
                    )["followers"].fillna(method="bfill")

                    df_posts_full = df_posts_full.sort_values("date").drop_duplicates(
                        subset=["shortcode"], keep="last"
                    )

                    self.df_posts_full = df_posts_full

                except Exception as e:
                    exception_type = sys.exc_info()[0]
                    print(ERR_SYS + str(exception_type))
                    print(e)
                    print(f"Class: {self.__str__()}\nMethod: {METHOD_NAME}\n")
                    self.df_posts_full = pd.DataFrame(columns=OUTPUT_COLUMNS)

            else:
                print("Warning: One of the DataFrames is empty. It cannot be computed.")
                self.df_posts_full = pd.DataFrame(columns=OUTPUT_COLUMNS)
        elif self.mode == "hashtags":
            HASHTAG_COLUMNS = [
                "caption",
                "comments_count",
                "like_count",
                "media_type",
                "timestamp",
            ]
            OUTPUT_COLUMNS = [
                "followers",
                "group",
                "created_at",
                "likes_count",
                "comment_count",
                "typename",
                "caption",
            ]
            try:
                df_hashtag_full = deepcopy(
                    df_posts[HASHTAG_COLUMNS]
                )  # df_hashtag camuflado
                df_hashtag_full = df_hashtag_full.rename(
                    columns={
                        "comments_count": "comment_count",
                        "like_count": "likes_count",
                        "media_type": "typename",
                        "timestamp": "date_utc",
                    }
                )

                df_hashtag_full = df_hashtag_full.drop_duplicates()
                df_hashtag_full["followers"] = 1
                df_hashtag_full["group"] = "hashtags"
                df_hashtag_full["date"] = pd.to_datetime(
                    df_hashtag_full["date_utc"], format="%Y-%m-%dT%H:%M:%S"
                )
                df_hashtag_full["created_at"] = pd.to_datetime(
                    df_hashtag_full["date"]
                ) - timedelta(hours=5)
                self.df_posts_full = df_hashtag_full[OUTPUT_COLUMNS]
            except Exception as e:
                exception_type = sys.exc_info()[0]
                print(ERR_SYS + str(exception_type))
                print(e)
                print(f"Class: {self.__str__()}\nMethod: {METHOD_NAME}\n")
        else:
            OUTPUT_COLUMNS = [
                "followers",
                "group",
                "created_at",
                "likes_count",
                "comment_count",
                "typename",
                "caption",
            ]
            self.df_posts_full = pd.DataFrame(columns=OUTPUT_COLUMNS)

    def by_post(self):
        """
        This method computes the engagement rate for every post based on the
        number of followers of the account. It stores it on the column
        'engagement_rate_by_post' on the input Pandas DataFrame 'df_posts_full'.

        Returns
        -------
        DataFrame
        """

        METHOD_NAME = "by_reach"

        df_posts_full = self.df_posts_full
        try:
            df_posts_full["engagement_rate_by_post"] = df_posts_full.apply(
                lambda row: 100 * (row.likes_count + row.comment_count) / row.followers,
                axis=1,
            )

            METRIC = "engagement_rate_by_post"
            ITEM_COLUMN = "owner_id"
            df_posts_full = df_posts_full.sort_values(by=["created_at"])
            df_posts_full = metric_transformation.MetricCategorization(
                df_posts_full, METRIC, ITEM_COLUMN
            ).categorize()

            return df_posts_full.dropna(subset=["engagement_rate_by_post"])

        except Exception as e:
            exception_type = sys.exc_info()[0]
            print(ERR_SYS + str(exception_type))
            print(e)
            print(f"Class: {self.__str__()}\nMethod: {METHOD_NAME}\n")
            return pd.DataFrame(
                columns=list(df_posts_full.columns)
                + ["engagement_rate_by_post", "boundary", "rel_engagement_rate_by_post"]
            )

class EngagementRateTW:
    def __init__(self, df_tweets, df_replies, mode="status", remove_rt=True):
        """
        This method computes the DataFrame 'df_tweets_full' with the column 'reply_count_no_api'
        which is a count of the replies for every post.

        Parameters
        ----------
        df_tweets:
            type: DataFrame
            this Pandas DataFrame muts have columns
            'tweet_id'.
        df_replies:
            type: DataFrame
            this Pandas DataFrame muts have columns
            'text', 'in_reply_to_status_id'.
        mode:
            type: str
            Selects the module to compute the engagement rates for.
            default = 'status'
            If set to 'terms' df_replies and groups are no used.
        """

        METHOD_NAME = "__init__"

        REPLIES_COLUMNS = ["text", "in_reply_to_status_id"]
        TWEETS_COLUMNS = [
            "twitter_id",
            "screen_name",
            "created_at",
            "tweet_id",
            "favorite_count",
            "retweet_count",
            "ac_followers_count",
            "in_reply_to_status_id",
            "media_entities",
            "user_mentions",
            "hashtags",
            "text",
            "profile_image",
        ]
        OUTPUT_COLUMNS = [
            "reply_count_no_api",
            "twitter_id",
            "screen_name",
            "group",
            "created_at",
            "tweet_id",
            "ac_followers_count",
            "favorite_count",
            "retweet_count",
            "in_reply_to_status_id",
            "media_entities",
            "user_mentions",
            "hashtags",
            "text",
            "profile_image",
        ]
        self.remove_rt = remove_rt
        self.mode = mode

        if mode == "status":
            if len(df_tweets) > 0 and len(df_replies) > 0:
                try:
                    df_tweets_full = deepcopy(
                        df_tweets[df_tweets["in_reply_to_status_id"].isna()][
                            TWEETS_COLUMNS
                        ]
                    )
                    df_tweets_full = df_tweets_full.drop_duplicates(
                        subset=[
                            "screen_name",
                            "created_at",
                            "user_mentions",
                            "hashtags",
                            "text",
                        ],
                        keep=False,
                    )
                    df_replies_count = (
                        df_replies[REPLIES_COLUMNS]
                        .groupby("in_reply_to_status_id")
                        .count()
                        .reset_index()
                    )
                    df_replies_count = df_replies_count.rename(
                        columns={
                            "in_reply_to_status_id": "tweet_id",
                            "text": "reply_count_no_api",
                        }
                    )
                    df_tweets_full = pd.merge(
                        df_tweets_full, df_replies_count, on=["tweet_id"], how="left"
                    )
                    df_tweets_full["reply_count_no_api"] = df_tweets_full[
                        "reply_count_no_api"
                    ].fillna(0)

                    df_tweets_full["created_at"] = pd.to_datetime(
                        df_tweets_full["created_at"]
                    ) - timedelta(hours=5)
                    self.df_tweets_full = df_tweets_full

                except Exception as e:
                    exception_type = sys.exc_info()[0]
                    print(ERR_SYS + str(exception_type))
                    print(e)
                    print(f"Class: {self.__str__()}\nMethod: {METHOD_NAME}\n")
                    self.df_tweets_full = pd.DataFrame(
                        columns=OUTPUT_COLUMNS, dtype=object
                    )

            else:
                print("Warning: One of the DataFrames is empty. It cannot be computed.")
                self.df_tweets_full = pd.DataFrame(columns=OUTPUT_COLUMNS, dtype=object)

        elif mode == "terms":
            try:
                df_tweets_full = deepcopy(df_tweets[TWEETS_COLUMNS])
                df_tweets_full = df_tweets_full.drop_duplicates(
                    subset=[
                        "screen_name",
                        "created_at",
                        "user_mentions",
                        "hashtags",
                        "text",
                        "media_entities",
                    ],
                    keep=False,
                )
                df_tweets_full[
                    "reply_count_no_api"
                ] = 0  # set replies to zero, temporary until official API
                df_tweets_full["group"] = "terms"  # set group to 'terms'
                df_tweets_full = df_tweets_full[
                    df_tweets_full["ac_followers_count"] != 0
                ]  # Avoiding division by zero for users with zero followes.
                df_tweets_full["created_at"] = pd.to_datetime(
                    df_tweets_full["created_at"]
                ) - timedelta(hours=5)
                if remove_rt:
                    rt_flag_list, unique_text_list, author_name_list = [], [], []
                    rt_pattern = re.compile(r"^(?:RT|rt) \@[a-zA-Z0-9\-\_]+\:\s")
                    for index, row in df_tweets_full.iterrows():
                        findings = re.findall(rt_pattern, row["text"])
                        rt_flag = 0
                        unique_text, author_name = row["text"], row["screen_name"]
                        if len(findings) > 0:
                            rt_flag = 1
                            unique_text = re.sub(rt_pattern, "", row["text"])
                            author_name = re.sub(
                                re.compile(r"^(?:RT|rt) \@"), "", findings[0]
                            ).replace(": ", "")
                        rt_flag_list.append(rt_flag)
                        unique_text_list.append(unique_text.lower())
                        author_name_list.append(author_name)
                    df_tweets_full["rt_flag"] = rt_flag_list
                    df_tweets_full["unique_text"] = unique_text_list
                    df_tweets_full["author_name"] = author_name_list
                self.df_tweets_full = df_tweets_full

            except Exception as e:
                exception_type = sys.exc_info()[0]
                print(ERR_SYS + str(exception_type))
                print(e)
                print(f"Class: {self.__str__()}\nMethod: {METHOD_NAME}\n")
                self.df_tweets_full = pd.DataFrame(columns=OUTPUT_COLUMNS, dtype=object)

        else:
            raise RuntimeError(
                f'Mode {mode} is not available. Modes available: "status" and "terms".'
            )

    def by_post(self):
        """
        This method computes the engagement rate for every post based on the
        number of followers of the account. It stores it on the column
        'engagement_rate_by_post' on the input Pandas DataFrame 'df_tweets_full'.

        Returns
        -------
        DataFrame
        """

        METHOD_NAME = "by_post"

        df_tweets_full = self.df_tweets_full
        try:
            if self.mode == "terms":
                df_tweets_full["engagement_rate_by_post"] = df_tweets_full.apply(
                    lambda row: row.favorite_count
                                + row.retweet_count
                                + row.reply_count_no_api,
                    axis=1,
                )

                if self.remove_rt:
                    df_tweets_max_er = df_tweets_full[
                        ["screen_name", "unique_text", "engagement_rate_by_post"]
                    ]
                    df_tweets_max_er = (
                        df_tweets_max_er.groupby(["screen_name", "unique_text"])
                            .max()
                            .reset_index()
                    )
                    df_tweets_full = df_tweets_full.merge(
                        df_tweets_max_er,
                        left_on=[
                            "author_name",
                            "unique_text",
                            "engagement_rate_by_post",
                        ],
                        right_on=[
                            "screen_name",
                            "unique_text",
                            "engagement_rate_by_post",
                        ],
                        how="inner",
                    )
                    df_tweets_full = df_tweets_full.drop(
                        ["rt_flag", "unique_text", "author_name", "screen_name_y"],
                        axis=1,
                    )
                    df_tweets_full = df_tweets_full.rename(
                        columns={"screen_name_x": "screen_name"}
                    )

            else:
                df_tweets_full["engagement_rate_by_post"] = df_tweets_full.apply(
                    lambda row: 100
                                * (row.favorite_count + row.retweet_count + row.reply_count_no_api)
                                / row.ac_followers_count,
                    axis=1,
                )

            METRIC = "engagement_rate_by_post"
            ITEM_COLUMN = "twitter_id"
            df_tweets_full = df_tweets_full.sort_values(by=["created_at"])
            df_tweets_full = metric_transformation.MetricCategorization(
                df_tweets_full, METRIC, ITEM_COLUMN
            ).categorize()

            return df_tweets_full.dropna(subset=["engagement_rate_by_post"])

        except Exception as e:
            exception_type = sys.exc_info()[0]
            print(ERR_SYS + str(exception_type))
            print(e)
            print(f"Class: {self.__str__()}\nMethod: {METHOD_NAME}\n")
            return pd.DataFrame(
                columns=list(df_tweets_full.columns)
                        + ["engagement_rate_by_post", "boundary", "rel_engagement_rate_by_post"]
            )
