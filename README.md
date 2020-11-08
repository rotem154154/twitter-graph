# twitter-graph
i used python 3.7 but any python 3.5+ should be fine.
this project uses [hyperdash](https://hyperdash.io/) for monitoring so it's recommended to setup hyperdash.

### [followers_threads_all.py](https://github.com/rotem154154/twitter-graph/blob/master/followers_threads_all.py "followers_threads_all.py")
this code will crawl all friends of users and then continue with all of the found users.
this code will save two pickle files into two folders:
* uf: the user-follow dictionary contains the users with their layer and followers
* q: the queue of the users that not yet crawled

the folder will have many files because the code will save every 15 min.
#### useage:
 try run the code and install any import that not fond
  you can edit the variables before the main:
  * first_user: make this False for load existing save, this will load the uf_file and q_file variables under the folder vars_dir


