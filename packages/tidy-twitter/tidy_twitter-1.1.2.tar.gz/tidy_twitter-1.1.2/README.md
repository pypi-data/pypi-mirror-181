# Welcome to tidy-twitter

tidy-twitter is a small program that is intended for those who want to clean up their Twitter history. A working Python3
environment and Twitter OAuth keys are required to run this program.

# Installation and quickstart

It's recommended to install tidy-twitter with [pipx](https://pypa.github.io/pipx/installation/). Install pipx first.

After pipx is installed run:

      pipx install tidy-twitter
      tidy_twitter --help

### Twitter OAuth keys

Twitter OAuth keys can be obtained from https://developer.twitter.com/

Export the following keys before running this program:

- TWITTER_CONSUMER_KEY
- TWITTER_CONSUMER_SECRET
- TWITTER_ACCESS_TOKEN
- TWITTER_ACCESS_TOKEN_SECRET

# Developer quick start

This program requires exporting Twitter OAuth keys to environment before use.

Use of virtual env is strongly recommended to not mess up your other / default Python environments.

1. Clone this repo
2. Install Python 3.9 with pyenv
3. Run the following to install all required dependencies and the program:

         poetry install

4. Run:

         poetry run tidy_twitter --help

# Usage

For help run

        $ tidy-twitter --help
        Usage: tidy-twitter [OPTIONS]
        
          This program deletes all tweets for user handle older than given number of
          days.
        
          It requires following Twitter OAuth keys to be exported to the environment
          before use:
        
          TWITTER_CONSUMER_KEY
        
          TWITTER_CONSUMER_SECRET
        
          TWITTER_ACCESS_TOKEN
        
          TWITTER_ACCESS_TOKEN_SECRET
        
        Options:
          -s, --screen_name TEXT  Twitter screen name (@username).  [required]
          -d, --days INTEGER      Number of days, defaults to 30 days.
          --version               Show the version and exit.
          --help                  Show this message and exit.

This program takes a few command line arguments in addition to fore-mentioned Twitter OAuth keys (as environment
variables):

* *--screen_name / -s* - Twitter user handle (@username) that tweets will be deleted for. Write it here **without an @**.
* *--days / -d* - All tweets older than this number of days will be deleted. Default is 30 (days).
* *--version* - displays program version
* *--help* - displays help message

# License

This software is released under MIT License. See LICENSE.txt for details.

# Bugs, issues, feature requests

Feel free to use this repo's Issue Tracker If you have any bugs to report or any requests / issues.

Thanks,

Sven