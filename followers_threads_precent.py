import os
import json
import threading

import botometer
import pandas
import requests
import tweepy
import time
from subprocess import call
from tqdm import tqdm
from hyperdash import Experiment
import subprocess
import pickle
import rotem_helpers
import _thread
from time import gmtime, strftime

import more_itertools as mit


exp = Experiment("follow_threads")
uf_file = '9-10-02-10-17.pkl'
vars_dir = '/Users/rotemisraeli/Documents/python/work/parts/vars/'

# followers_per_user = 10000
followers_precent = 0.25
version = 9

n_t = 24
nums = 10000

q = []
users_follow = {}

def main():
    setup_hyperdash()
    # new_q(['BDSmovement'])
    load_vars()
    # print(q)
    # user_friends('BDSmovement','followers')
    # s = old_follow()

    qs = chunks(q,n_t)

    treads = []
    print(len(users_follow),'gggggg')
    for thread_num in range(n_t):
        x = threading.Thread(target=new_follow, args=(thread_num,qs[thread_num],))
        treads.append(x)
        x.start()

    for t in treads:
        t.join()

    exp.end()


def chunks(l, n):
    return [list(c) for c in mit.divide(n, l)]

def get_num_followers(user):
    site = 'https://cdn.syndication.twimg.com/widgets/followbutton/info.json?screen_names='
    r = requests.get(site + user)
    return int(r.text.split('followers_count":')[1].split(',')[0])


def load_vars():
    global q, users_follow
    q = rotem_helpers.load_obj('/Users/rotemisraeli/Documents/python/work/parts/vars/q/save2.pkl')
    users_follow = rotem_helpers.load_obj('/Users/rotemisraeli/Documents/python/work/parts/vars/uf/'+uf_file)


def user_friends(username, followers_or_following):
    num_followers = float(get_num_followers(username))

    output = subprocess.check_output(
        "twint -u " + username + " --" + followers_or_following + " --limit " + str(int(num_followers*followers_precent)), shell=True)
    followed = output.decode('utf8').split('\n')[:-1]
    return followed

def users_from_file(file_path):
    df = pandas.read_csv(file_path)
    account_list = df["acount_name"].tolist()
    return account_list


def setup_hyperdash():
    exp.param("followers_precent", followers_precent)
    exp.param('number of threads',n_t)
    # exp.param("follow per user", followers_per_user)



def new_follow(thread_num,thread_q):
    global users_follow
    print(len(thread_q),len(users_follow))
    i = 0
    pop_first = True
    count_first = 0
    if thread_num == 0:
        while True:
            time.sleep(60*20)
            exp.metric('laptop_battery', rotem_helpers.get_battery())
            users_follow2 = users_follow.copy()
            exp.metric('num_users', len(users_follow2))
            file_name = str(version) + '-' + strftime("%m-%d-%H-%M", gmtime()) + '.pkl'
            rotem_helpers.save_obj(users_follow2, vars_dir + 'uf/' + file_name)

    while i < nums:
        try:
            current_user = thread_q.pop(0)
            if current_user in users_follow:
                if pop_first:
                    count_first = 0
            else:
                if pop_first:
                    count_first+=1
                    if count_first > 5:
                        thread_q.pop(0)
                        pop_first = False

                else:
                    exp.metric(str(thread_num), float(i))

                    i+=1
                    try:
                        followers = user_friends(current_user, 'followers')
                        users_follow[current_user] = {'followers': followers}
                    except:
                        print('******************** ' + current_user)
                        pass
                # if time.time() - last_time > 10*60:
                #     last_time = time.time()
                    # file_name = str(version)+'-'+str(thread_num)+'-'+strftime("%m-%d-%H-%M", gmtime()) + '.pkl'
                    # rotem_helpers.save_obj(thread_q, vars_dir+'q/' + file_name)
        except:
            i+=1
            thread_q.pop(0)


if __name__ == "__main__":
    main()

#
# def old_follow():
#     users = users_from_file('../week2/' + real_or_bot + '_users2.csv')[:3]
#     csv = []
#     s = []
#     lens = len(users)
#     count = 0
#     print('gets followers from ', lens, 'users')
#     for index, user in enumerate(users):
#         exp.metric('get followers', float(count) / float(lens))
#         count += 1
#         try:
#             followers = user_friends(user, 'followers')
#             csv.append({'user': user, 'followers': followers})
#             s.append(user)
#             s.extend(followers)
#         except:
#             pass
#
#     s = list(dict.fromkeys(s))
#     return s
