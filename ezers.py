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

def save_obj(obj, name):
    with open(name, 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    with open(name, 'rb') as f:
        return pickle.load(f)