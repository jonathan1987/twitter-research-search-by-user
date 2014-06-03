# -*- coding: utf-8 -*-
"""
Created on Wed Mar 19 22:31:21 2014

@author: johnboy
"""

import tweepy 
import csv
import networkx as nx
from itertools import combinations
import time
import random

ckey ='???'
csecret ='???'
atoken = '???'
asecret = '???'

#Authencation
auth = tweepy.OAuthHandler(ckey,csecret)
auth.set_access_token(atoken,asecret)
api = tweepy.API(auth)

G = nx.DiGraph()
# read through the csv file
with open('<location of dataset of twitter users with specified words in their description>','rb') as f:
    reader=csv.reader(f)
    reader.next()
    for row in reader:
        G.add_node(row[12],lang=row[8],utc_timezone=row[14],num_friends=row[4])# add the screen_name to the graph
        # grabbing the description, friends_count, id, lang, location and screen_name respectively
        # as a tuple for a node
f.close()
# for each pair of nodes, check to see if they are friends (following the other) using show_friendship(user1,user2)
# which returns a tuple of two values which are classes of the tweepy.models.friendship
node = G.nodes()
sample_nodes = random.sample(node,50) # random sample of 50 users from the dataset
friendship_pairs = combinations(sample_nodes,2)
H = G.subgraph(sample_nodes) # create a subgraph based on the random sample of 50 nodes (twitter users)

ctr=1
for a in friendship_pairs: # for every combinations of two users in the dataset
    print ctr    
    try:
        friendship = api.show_friendship(source_screen_name=a[0],target_screen_name=a[1])
        if friendship[0].following: # is (user1 following user2)?
            print 'adding edge from', a[0], 'to', a[1]            
            H.add_edge(a[0],a[1]) # user1 ---> user2
        else:
            print a[0], 'is not following', a[1]
            
        if friendship[1].following: # is (user2 following user1)?
            print 'adding edge from', a[1], 'to', a[0]
            H.add_edge(a[1],a[0]) # user1 <--- user2
        else:
             print a[1], 'is not following', a[0]
    
        print '\n'
        ctr +=1
    except tweepy.TweepError:
        print '\t', 'rate limit excedded; sleeping for 15 mintues'
        time.sleep(60*15) # sleep for 15 minutes after being rate limited to use show_frienship() function again
        print '\t','resuming progress....'      
        continue
        
print 'writing to gexf file'
nx.write_gexf(H,'<location of gexf file that you want to save to be opened up using gephi and examine the graph>')    
