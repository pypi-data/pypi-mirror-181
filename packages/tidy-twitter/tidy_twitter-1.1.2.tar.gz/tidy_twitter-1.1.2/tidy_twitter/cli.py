#
# This script deletes Twitter tweets.
# It requires Twitter API OAuth keys for
# the account that the tweets will be deleted for.
# It takes some arguments like number of days and user handle
# to delete tweets for.
# It's configured to act easy on Twitter API to not overload it. That's why
# there's a delay between delete requests
#
# Copyright (c) 2021 Sven Varkel.
#

import click
import asyncio
import pkg_resources
from typing import AnyStr
from tidy_twitter.twitter_cleanup import delete_tweets

__version__ = pkg_resources.get_distribution("tidy-twitter").version


@click.command(name="cleanup",
               help="This command deletes all tweets for user handle older than given number of days.\n\n"
                    "It requires following Twitter OAuth keys to be exported to the environment before use:\n\n"
                    "TWITTER_CONSUMER_KEY\n\nTWITTER_CONSUMER_SECRET\n\nTWITTER_ACCESS_TOKEN\n\nTWITTER_ACCESS_TOKEN_SECRET")
@click.option("--screen_name", "-s", help="Twitter screen name (@username).", type=click.STRING, required=True)
@click.option("--days", "-d", help="Number of days, defaults to 30 days.", default=30, type=click.INT, required=False)
@click.version_option(__version__)
def cli(screen_name: AnyStr, days: int = 30, ):
    """
    Main entry point for the command line interface
    :param user_handle:
    :param days:
    :return:
    """
    asyncio.run(delete_tweets(screen_name=screen_name, days=days))
    return


if __name__ == "__main__":
    cli()
