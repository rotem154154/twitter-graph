import time

import psutil
from hyperdash import Experiment

import rotem_helpers
import work.parts.ezers as ezers
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

import sys
import threading
# echo 'export PATH=$PATH:/Users/rotemisraeli/Documents/python/work/geckodriver'

exp = Experiment("user_data_threads")

n_t = 12
count_all_threads = 0
load_file = 35450
users_follows = []
def main():

    # driver = webdriver.Firefox(firefox_binary='/Users/rotemisraeli/Documents/python/work/geckodriver')


    setup_hyperdash()
    load_vars()
    qs = chunks(users_follows, n_t)
    treads = []
    for thread_num in range(n_t):
        x = threading.Thread(target=thread_mission, args=(qs[thread_num],thread_num,))
        treads.append(x)
        x.start()

    while True:
        time.sleep(60*5)
        exp.metric('all' , float(count_all_threads)/float(len(users_follows)))
        exp.metric('ram', psutil.virtual_memory().percent/100)

        new_uf = dict(qs[0])
        for i in range(n_t-1):
            new_uf.update(qs[i+1])
        ezers.save_obj(new_uf,'/Users/rotemisraeli/Documents/python/work/parts/vars/t_uf/'+str(load_file+count_all_threads)+'.pkl')




def chunks(ufs, n):
    ds = []
    for nn in range(n):
        ds.append({key: value for i, (key, value) in enumerate(ufs.items()) if i % n == nn})
    return ds

def thread_mission(small_uf,thread_num):
    global count_all_threads
    driver = webdriver.Firefox(executable_path=r'/Users/rotemisraeli/Documents/python/work/geckodriver')

    count1 = 0
    count2 = 0
    for user,user_data in small_uf.items():
        count1+=1
        if not 'join_year' in user_data:
            try:
                get_user_data(driver, user,small_uf)
                count2 += 1
            except:
                print('error ' + user)
                # small_uf.pop(user, None)
            exp.metric(str(thread_num), float(count1) / float(len(small_uf)))
            exp.metric('laptop_battery', rotem_helpers.get_battery())

            # exp.metric('count2', count2)
            # exp.metric('battery', rotem_helpers.get_battery())
        count_all_threads+=1
    exp.end()
    driver.close()



def get_user_data(driver,user,small_uf):
    driver.get('https://foller.me/'+user)
    driver.implicitly_wait(40)
    small_uf[user]['join_year'] = driver.find_element_by_xpath('//*[@id="overview"]/div[2]/div[2]/table/tbody/tr[2]/td[2]').text.split(' ')[-1]
    try: user_overview = driver.find_elements_by_xpath('//*[@id="overview"]/div[2]/div[4]/table/tbody/tr')
    except:
        pass
    try: small_uf[user]['tweets'] = user_overview [1].find_elements_by_tag_name('td')[1].text.replace(',','')
    except:
        pass
    try: small_uf[user]['following'] = user_overview [2].find_elements_by_tag_name('td')[1].text.replace(',', '')
    except:
        pass
    try: small_uf[user]['followers_ratio'] = user_overview [3].find_elements_by_tag_name('td')[1].text.split(' ')[0].replace(',', '').split('.')[0]
    except:
        pass
    try:  small_uf[user]['listed'] = user_overview [4].find_elements_by_tag_name('td')[1].text.replace(',', '')
    except:
        pass

    try:
        user_topics = driver.find_element_by_xpath('//*[@id="topics-cloud"]').find_elements_by_tag_name('a')
        topics = []
        for t in user_topics:
            topics.append(t.text)
        small_uf[user]['topics'] = topics
    except:
        pass

    try:
        user_hashtags = driver.find_element_by_xpath('//*[@id="topics"]/div[3]/div[2]/p').find_elements_by_tag_name('a')
        hashtags = []
        for t in user_hashtags:
            hashtags.append(t.text[1:])
        small_uf[user]['hashtags'] = hashtags
    except:
        pass


    try:
        user_mentions = driver.find_element_by_xpath('//*[@id="topics"]/div[4]/div[2]/p[1]').find_elements_by_tag_name('a')
        mentions = []
        for t in user_mentions:
            mentions.append(t.get_attribute('href').split('.me/')[1])
        small_uf[user]['mentions'] = mentions
    except:
        pass



    user_tweets_analysis = driver.find_elements_by_xpath('//*[@id="tweets"]/div[2]/div[2]/table/tbody/tr')
    num_tweets = float(user_tweets_analysis[0].find_elements_by_tag_name('td')[1].text.split(' / ')[1])
    try: small_uf[user]['replies'] = float(user_tweets_analysis[0].find_elements_by_tag_name('td')[1].text.split(' / ')[0]) / num_tweets
    except:
        pass
    try: small_uf[user]['tweets_with_@mentions'] = float(user_tweets_analysis[1].find_elements_by_tag_name('td')[1].text.split(' / ')[0]) / num_tweets
    except:
        pass
    try: small_uf[user]['tweets_with_#hashtags'] = float(user_tweets_analysis[2].find_elements_by_tag_name('td')[1].text.split(' / ')[0]) / num_tweets
    except:
        pass
    try: small_uf[user]['retweets'] = float(user_tweets_analysis[3].find_elements_by_tag_name('td')[1].text.split(' / ')[0]) / num_tweets
    except:
        pass
    try: small_uf[user]['tweets_with_links'] = float(user_tweets_analysis[4].find_elements_by_tag_name('td')[1].text.split(' / ')[0]) / num_tweets
    except:
        pass
    try: small_uf[user]['tweets_with_media'] = float(user_tweets_analysis[5].find_elements_by_tag_name('td')[1].text.split(' / ')[0]) / num_tweets
    except:
        pass
    # ezers.save_obj(small_uf, 'follow-users_follow' + str(version))


def load_vars():
    global users_follows
    users_follows = ezers.load_obj('/Users/rotemisraeli/Documents/python/work/parts/vars/t_uf/'+str(load_file)+'.pkl')

def setup_hyperdash():
    exp.param('load_file', load_file)
    exp.param('n_t',n_t)


if __name__ == "__main__":
    main()

