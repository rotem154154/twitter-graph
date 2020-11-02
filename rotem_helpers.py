import subprocess
import pickle

import psutil


def get_battery():
    try:
        cmd = 'pmset -g batt | grep -Eo "\d+%" | cut -d% -f1'
        ps = subprocess.Popen(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return float(str(ps.communicate()[0])[2:-3])/100
    except:
        return -1

def get_ram():
    try:
        return psutil.virtual_memory().percent / 100
    except:
        return -1

def hyperdash_update(exp):
    exp.metric('battery',get_battery())
    exp.metric('ram',get_ram())

def save_obj(obj, name):
    with open(name, 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    with open(name, 'rb') as f:
        return pickle.load(f)
