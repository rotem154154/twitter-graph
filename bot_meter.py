import work.parts.ezers as ezers
import os
import json
import botometer
import pandas
import tweepy
import time
from subprocess import call
from tqdm import tqdm
from hyperdash import Experiment
import subprocess
import pickle
import copy
import sys
import rotem_helpers

exp = Experiment("bot_meter")

version = 3

users_follow = {}

# rapidapi_key = "OyTByfzOA2mshbg7TNfI9gxuqleyp1Ne1RXjsni94N9JOht0ZB" # now it's called rapidapi key
rapidapi_key = '8a8d64e8b5msh34c092335ddc0b0p125cb8jsne6b7f9d11cea'
twitter_app_auth = {
    'consumer_key': 'XZqb7nIARNbh3x4KxaInQ',
    'consumer_secret': 'MHYtjLH6CqekMxR8sQtH6trnEXfdNCMvd75Dv5akWo',
    'access_token': '245305900-NTgpfmVo4XK39SCwhBZ10SuWEnj1MRu0ymv2h6CJ',
    'access_token_secret': 'XYyP5fG4tQL3chz6p7x71pjTi883CJA59g72Bran1bC2P',
  }
bom = botometer.Botometer(wait_on_ratelimit=True,
                          rapidapi_key=rapidapi_key,
                          **twitter_app_auth)



def bot_meter_users():
    count = 0
    count2 = 0
    copy_user_follow = copy.deepcopy(users_follow)
    for user,user_data in copy_user_follow.items():
        count+=1
        if count2 == 1900:
            exp.end()
            sys.exit()
        if not 'bot_meter' in user_data:
            try:
                for screen_name, result in bom.check_accounts_in([user]):
                    try:
                        # print(result.get("display_scores").get("english"))
                        users_follow[screen_name]['bot_meter'] = result.get("display_scores").get("english")
                        count2+=1
                    except Exception as e:
                        print(e)
                        # users_follow.pop(screen_name, None)
                    ezers.save_obj(users_follow, 'follow-users_follow' + str(version))
                    exp.metric('users', float(count) / float(len(users_follow)))
                    exp.metric('count2', count2)
                    exp.metric('battery', rotem_helpers.get_battery())
            except:
                print('error ' + user)



def main():
    load_vars()
    setup_hyperdash()

    bot_meter_users()

    exp.end()


def load_vars():
    global users_follow
    users_follow = ezers.load_obj('follow-users_follow' + str(version))


def setup_hyperdash():
    exp.param("users", len(users_follow))



if __name__ == "__main__":
    main()
