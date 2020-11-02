import os
import json
import botometer
import pandas
import tweepy
import time
from subprocess import call
from tqdm import tqdm
from hyperdash import Experiment
import numpy as np
import subprocess
import pickle
import work.parts.ezers as ezers
import math
import rotem_helpers
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
import copy
import sys
from torch.autograd import Variable
import torch.optim as optim

import torch.nn as nn
import torch
import torch.nn.functional as F
import matplotlib.pyplot as plt

# os.environ["CUDA_VISIBLE_DEVICES"] = ""

exp = Experiment("classifier1")

version = 3
sub_version = '_19-9'
nums = 100
epochs = 40
batch_size = 500
learning_rate = 0.05

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class Network(nn.Module):
    def __init__(self, input_size,hidden_size1,hidden_size2,output_size):
        super(Network, self).__init__()
        self.l1 = nn.Linear(input_size, hidden_size1)
        self.relu1 = nn.ReLU()
        self.l2 = nn.Linear(hidden_size1, hidden_size2)
        self.relu2 = nn.ReLU()
        self.l3 = nn.Linear(hidden_size2, output_size)

    def forward(self, x):
        x = self.l1(x)
        x = self.relu1(x)
        x = self.l2(x)
        x = self.relu2(x)
        x = self.l3(x)
        return F.log_softmax(x)

net = Network(11,1280,1280,14).to(device)  # define the network
users_follow = {}
dataset = np.empty(1,np.float32)
dataset_y = np.empty(1,np.float32)


def main():
    setup_hyperdash()
    load_vars()
    setup_data()

    # print(dataset[0])
    classific()


    exp.end()


def setup_data():
    global dataset,dataset_y
    dataset_list = []
    dataset_y_list = []
    for user,user_data in users_follow.items():
        try:
            if 'join_year' in user_data:
                dataset_list.append([
                    # (float(user_data['join_year'])-2006)/14,
                    math.log(float(user_data['tweets'])) / 19,
                    math.log(float(user_data['following']))/14,
                    math.log(float(user_data['followers_ratio'])) / 18,
                    math.log(float(user_data['listed'])) / 13,
                    math.sqrt(float(user_data['replies'])),
                    float(user_data['tweets_with_@mentions']),
                    math.sqrt(float(user_data['tweets_with_#hashtags'])),
                    math.sqrt(float(user_data['tweets_with_#hashtags'])),
                    float(user_data['retweets']),
                    float(user_data['tweets_with_links']),
                    float(user_data['tweets_with_links'])
                ])
                year = (int(user_data['join_year']) - 2006)-1
                dataset_y_list.append(year)
        except:
            pass
            # print(user_data['join_year'])
    dataset = np.asarray(dataset_list,dtype=np.float32)
    dataset_y = np.asarray(dataset_y_list,dtype=np.float32)



def classific():
    x_train = dataset[:12000]
    y_train = dataset_y[:12000]
    x_test = dataset[12000:]
    y_test = dataset_y[12000:]



    print(len(x_train),len(y_train),len(x_test),len(y_test))
    x_train,y_train,x_test,y_test = torch.from_numpy(x_train).to(device),torch.from_numpy(y_train).to(device),torch.from_numpy(x_test).to(device),torch.from_numpy(y_test).to(device)
    x_train, y_train, x_test, y_test =  x_train.to(device),y_train.to(device),x_test.to(device),y_test.to(device)
    test_net(x_test, y_test)

    loss_log = []
    optimizer = optim.SGD(net.parameters(), lr=learning_rate, momentum=0.9)
    loss_func = nn.CrossEntropyLoss()
    cn = 0
    error = 0
    for e in tqdm(range(epochs)):
        for i in range(0, x_train.shape[0], batch_size):
            # print(e)
            x_mini = x_train[i:i + batch_size]
            y_mini = y_train[i:i + batch_size]

            x_var = Variable(x_mini)
            y_var = Variable(y_mini)

            optimizer.zero_grad()
            net_out = net(x_var)


            # sys.exit()

            try:
                cn +=1
                loss = loss_func(net_out, y_var.type(torch.LongTensor))
                loss.backward()
                print(loss)
                optimizer.step()
            except:
                error +=1

            # if i % 100 == 0:
            #     loss_log.append(loss.data[0])

        # print('Epoch: {} - Loss: {:.6f}'.format(e, loss.data[0]))

    test_net(x_test,y_test)

    # print(int(net.forward(x_test[co])),int(y_test[co]))

def test_net(x_test,y_test):
    print(x_test.shape)
    output = torch.argmax(net(x_test), dim=1)
    correct = 0.0
    for i in range(len(x_test)):
        if output[i] == y_test[i]:
            correct+=1
    print(correct/len(x_test))

def calc_accuracy(x,y_real):
    y_pred = net(x)
    sum_acc = 0
    for i in range(len(y_real)):
        sum_acc += abs(y_real[i]-y_pred[i])
    return sum_acc/len(y_real)

def load_vars():
    global users_follow
    users_follow = ezers.load_obj('follow-users_follow' + str(version)+sub_version)

def setup_hyperdash():
    exp.param('version', version)
    exp.param('nums',nums)

if __name__ == "__main__":
    main()

