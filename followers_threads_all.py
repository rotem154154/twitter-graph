import os
import json
import threading
from random import shuffle

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
import sys
from work.parts import ezers

exp = Experiment("follow_threads2.1")
uf_file = '12-10-15-18-44.pkl'
q_file = '12-10-15-03-11.pkl'
vars_dir = '/Users/rotemisraeli/Documents/python/work/parts/vars2/'

# if in uf layer = 1 dont change it

# followers_per_user = 10000
version = 12 # will be append to file
n_t = 128 # number of threads
nums = 100000

q_in_use = False
q = []
all_qs = []
users_follow = {}

def main():
    global all_qs
    setup_hyperdash()
    # new_q([['BDSmovement',0]])
    load_vars()
    # print(q)
    # user_friends('BDSmovement','followers')
    # s = old_follow()
    shuffle(q)
    all_qs = chunks(q,n_t)

    treads = []
    print(len(users_follow),'gggggg')


    for thread_num in range(n_t):
        x = threading.Thread(target=new_follow, args=(thread_num,all_qs[thread_num],))
        treads.append(x)
        x.start()

    for t in treads:
        t.join()

    exp.end()


def new_q(q):
    file_name = str(version) + '-' + strftime("%m-%d-%H-%M", gmtime()) + '.pkl'
    rotem_helpers.save_obj(q, vars_dir + 'q2/' + file_name)


def chunks(l, n):
    return [list(c) for c in mit.divide(n, l)]

def get_num_followers(user):
    site = 'https://cdn.syndication.twimg.com/widgets/followbutton/info.json?screen_names='
    r = requests.get(site + user)
    return int(r.text.split('followers_count":')[1].split(',')[0])


def load_vars():
    global q, users_follow
    q = rotem_helpers.load_obj('vars2/q2/'+q_file)
    # q = [['BDSmovement',0]]
    users_follow = rotem_helpers.load_obj('vars2/uf2/'+uf_file)


def user_friends(username, followers_or_following):
    # num_followers = float(get_num_followers(username))

    output = subprocess.check_output(
        "twint -u " + username + " --" + followers_or_following, shell=True)
    followed = output.decode('utf8').split('\n')[:-1]
    return followed

def users_from_file(file_path):
    df = pandas.read_csv(file_path)
    account_list = df["acount_name"].tolist()
    return account_list


def setup_hyperdash():
    # exp.param("followers_precent", followers_precent)
    exp.param('number of threads',n_t)
    # exp.param("follow per user", followers_per_user)

lock = threading.Lock()
last_time = time.time()


def new_follow(thread_num,thread_q):
    global users_follow, q_in_use, lock, last_time
    # print(len(thread_q),len(users_follow))
    i = 0
    pop_first = True
    count = 0
    qs_ezer = []
    for qs in thread_q:
        qs_ezer.append(qs[0])
    while i < nums:
        while q_in_use:
            time.sleep(10)
        try:
            current_user,dist = thread_q.pop(0)
            # print(current_user,dist)
            i += 1
            if dist == 1:
                if True or not current_user in users_follow:
                    exp.metric(str(thread_num),count)
                    count+=1
                    followers = user_friends(current_user, 'followers')
                    followers2 = []
                    for folo in followers:
                        while q_in_use:
                            time.sleep(10)
                        if folo in users_follow:
                            users_follow[folo]['followers'].append(current_user)
                        else:
                            # followers2.append([folo,dist+1])
                            users_follow[folo] = {'followers':[],'layer':dist+1}
                    # thread_q.extend(followers2)
                    users_follow[current_user] = {'followers':followers,'layer':dist}
                    # file_name = 'final' + str(version) + '-' + strftime("%m-%d-%H-%M", gmtime()) + '.pkl'
                    # rotem_helpers.save_obj(q, vars_dir + 'q/' + file_name)
                    while q_in_use:
                        time.sleep(10)
                    # if thread_num == 0:
                    #     print(time.time()-last_time)
                    if time.time() - last_time > 15 * 60:
                        with lock:
                            q_in_use = True
                            worked = False
                            file_name = str(version) + '-' + strftime("%m-%d-%H-%M", gmtime()) + '.pkl'
                            while not worked:
                                try:
                                    last_time = time.time()
                                    # q_to_save = []
                                    # qs_ezer = []
                                    # q_in_use = True
                                    # for qs_mini in all_qs:
                                    #     qs_ezer.append(qs_mini.copy())
                                    # q_in_use = False
                                    # for qs_mini in qs_ezer:
                                    #     q_to_save.extend(qs_mini)
                                    #
                                    # rotem_helpers.save_obj(q_to_save, vars_dir + 'q2/' + file_name)
                                    rotem_helpers.save_obj(users_follow, vars_dir + 'uf2/' + file_name)
                                    q_in_use = False
                                    worked = True
                                except:
                                    time.sleep(5)
        except Exception as e:
            if str(e) == 'pop from empty list':
                print('fffffffffff')
                rotem_helpers.save_obj(q, vars_dir + 'q2/' + str(len(q)) + '.pkl')
                rotem_helpers.save_obj(users_follow, vars_dir + 'uf2/' + str(len(users_follow)) + '.pkl')
                sys.exit(0)
            time.sleep(10)
            print('ooo',thread_num,e)

            # print(thread_q)
            # if dist == 0:
            #     if current_user in users_follow:
            #         if pop_first:
            #             count_first = 0
            #     else:
            #         if False and pop_first:
            #             count_first+=1
            #             if count_first > 5:
            #                 thread_q.pop(0)
            #                 pop_first = False
            #
            #         else:
            #             exp.metric(str(thread_num), float(i))



        # except:
        #     i+=1
            # thread_q.pop(0)


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
