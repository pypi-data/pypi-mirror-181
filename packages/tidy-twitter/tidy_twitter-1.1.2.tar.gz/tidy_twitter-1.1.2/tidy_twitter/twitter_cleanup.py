#
# This file contains main logic for deleting old tweets
#
# Copyright (c) 2021-2021 Sven Varkel.
#

import os
import pytz
import asyncio
import twitter
from tqdm import tqdm
from datetime import datetime
from typing import AnyStr, List
from dateutil.parser import parse
from twitter import TwitterError


async def load_tweets(screen_name: AnyStr, offset: int):
    client = get_client()
    if client:
        tweets = client.GetUserTimeline(screen_name=screen_name, count=200, max_id=offset, include_rts=True)
        return tweets


def get_client():
    """
    Return configured Twitter client instance
    :return:
    """
    CONSUMER_KEY = str(os.getenv("TWITTER_CONSUMER_KEY"))
    CONSUMER_SECRET = str(os.getenv("TWITTER_CONSUMER_SECRET"))
    ACCESS_TOKEN = str(os.getenv("TWITTER_ACCESS_TOKEN"))
    ACCESS_TOKEN_SECRET = str(os.getenv("TWITTER_ACCESS_TOKEN_SECRET"))
    client = twitter.Api(consumer_key=CONSUMER_KEY,
                         consumer_secret=CONSUMER_SECRET,
                         access_token_key=ACCESS_TOKEN,
                         access_token_secret=ACCESS_TOKEN_SECRET)
    return client


async def delete_tweets(screen_name: AnyStr, days: int = 30):
    """
    This function gathers tweet id-s recursive that will be deleted
    and after that tries to delete tweets with found id-s
    :return:
    """

    async def _internal(screen_name: AnyStr, days: int, max_id: int, out: List):
        """
        Internal recursion worker
        :param max_id:
        :param out:
        :return:
        """
        items = await load_tweets(screen_name=screen_name, offset=max_id)
        if len(items) < 2:
            return out
        for item in tqdm(items, desc="Loading tweet ID-s"):
            if item.user.id == user.id:
                try:
                    created_at = parse(item.created_at)
                    max_id = item.id
                    _diff_days = (now - created_at).days
                    if _diff_days >= days:
                        out.append(item.id)
                except Exception as ex:
                    print(ex)
        return await _internal(screen_name=screen_name, days=days, max_id=max_id, out=out)

    try:
        client = get_client()
        if client:
            user = client.GetUser(screen_name=screen_name)

            # get most recent tweet
            response = client.GetUserTimeline(screen_name=screen_name, count=1, include_rts=True)
            max_item = response[-1]
            max_id = max_item.id

            now = datetime.utcnow()
            tz = pytz.timezone("UTC")
            now = tz.localize(now)

            # gather all deleting candidate id-s recursively
            ids = await _internal(screen_name=screen_name, days=days, max_id=max_id, out=list())

            # delete all gathered tweet by id-s
            for idx, _id in tqdm(enumerate(ids), desc="Deleting tweets", total=len(ids)):
                try:
                    client.DestroyStatus(_id)
                except Exception as ex:
                    print(ex)
                await asyncio.sleep(delay=0.5)
    except Exception as ex:
        print(ex)
    return
