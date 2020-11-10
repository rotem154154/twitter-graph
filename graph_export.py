import work.project_files.ezers as ezers
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
import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()
plt.style.use('dark_background')


version = 4


users_follow = {}

def make_graph():
    for user,user_data in users_follow.items():
        G.add_node(user,layer = user_data['layer'])

    for user,user_data in users_follow.items():
        for folo in user_data['followers']:
            G.add_edge(user,folo)

    #     try:
    #         if 'bot_meter' in user_data and user_data['bot_meter'] > 0:
    #             G.add_node(user,bot_meter = user_data['bot_meter'])
    #     except:
    #         if 'bot_meter' in user_data and user_data['bot_meter']['overall'] > 0:
    #             G.add_node(user,bot_meter = user_data['bot_meter']['overall'])
    # for user in G.nodes:
    #     for follo in users_follow[user]['followers']:
    #         if follo in G.nodes:
    #             G.add_edge(user,follo)

    nx.write_graphml(G, 'graph_version_' + str(version) + '.graphml')


def make_graph_user_data():
    print('1')
    for user,user_data in users_follow.items():
        try:
            if 'join_year' in user_data:
                user_attr = {i: user_data[i] for i in user_data if i != 'followers'}
                G.add_node(user)
                G.nodes[user].update(user_attr)
        except:
            pass
    print('2')
    for user in G.nodes:
        for follo in users_follow[user]['followers']:
            if follo in G.nodes:
                G.add_edge(user,follo)

    print('3')
    nx.write_graphml(G, 'graph_version_' + str(version) + '_user_data.graphml')


def make_graph_all():
    for user,user_data in users_follow.items():
        try:
            if 'bot_meter' in user_data and 'overall' in user_data['bot_meter']:
                user_data['bot_meter'] = user_data['bot_meter']['overall']
        except:
            pass

        # try:
        # if 'bot_meter' in user_data and user_data['bot_meter'] > 0 and 'join_year' in user_data:
        #     user_attr = {i: user_data[i] for i in user_data if i != 'followers'}
        #     G.add_node(user)
        #     G.nodes[user].update(user_attr)
        G.add_node(user)

        # except:
        #     print(user_data['bot_meter'])
        #     if ('bot_meter' in user_data) and\
        #         (user_data['bot_meter']['overall'] > 0) and\
        #         ('join_year' in user_data):
        #         user_data['bot_meter'] = user_data['bot_meter']['overall']
        #         user_attr = {i: user_data[i] for i in user_data if i != 'followers'}
        #         G.add_node(user, user_attr)


    for user in G.nodes:
        for follo in users_follow[user]['followers']:
            if follo in G.nodes:
                G.add_edge(user,follo)
    print(len(G.nodes))
    nx.write_graphml(G, 'graph_version_' + str(version) + '_all.graphml')

def load_graph(file):
    print('kk')
    graph = nx.read_graphml(file)
    print(graph.number_of_edges())
    print(graph.number_of_nodes())

def main():
    # load_vars()
    #
    make_graph()
    # graph = load_graph('graph_version_4.graphml')


def load_vars():
    global users_follow
    # users_follow = ezers.load_obj('/Users/rotemisraeli/Documents/python/work/project_files/vars/t_uf/81356.pkl')
    users_follow = ezers.load_obj('/Users/rotemisraeli/Documents/python/work/project_files/vars2/uf2/12-10-16-07-24.pkl')


if __name__ == "__main__":
    t1 = time.time()

    main()

    print(time.time()-t1)

