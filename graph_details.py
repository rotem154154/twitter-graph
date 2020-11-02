import pickle
import sys

def load_obj(name ):
    with open(name, 'rb') as f:
        return pickle.load(f)

# folder_path = '/Users/rotemisraeli/Documents/python/work/parts/vars/t_uf/'
# graph_name = '70573.pkl'

# folder_path = '/Users/rotemisraeli/Documents/python/work/parts/vars/t_uf/'
# graph_name = '81422.pkl'
folder_path = '/Users/rotemisraeli/Documents/python/work/parts/vars/t_uf/'
graph_name = '32440.pkl'

users_follow = load_obj(folder_path+graph_name)

print('nodes in graph:',len(users_follow))

list_user_data = []
list_botmeter = []
list_all = []
for user, user_data in users_follow.items():
    if 'join_year' in user_data:
        list_user_data.append(user)
    if 'bot_meter' in user_data:
        list_botmeter.append(user)
    if 'join_year' in user_data and 'bot_meter' in user_data:
        list_all.append(user)

print('nodes with user data:',len(list_user_data))
print('nodes with bot score:',len(list_botmeter))
print('nodes with both user data and bot score:',len(list_all))

#IsraelMFA
