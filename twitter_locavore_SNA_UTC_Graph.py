# -*- coding: utf-8 -*-
"""
Created on Tue Mar 25 08:31:56 2014

# Author: Jonathan Hernandez
# Email: jayhernandez1987@gmail.com
"""

import csv
import networkx as nx
from itertools import combinations

# for graph coloring red for en, blue for f and green for none
color_lang = {'en': 'r', 'fr': 'b', 'None': 'g'}
# for graph labeling keys correspond to the utc timezones and values are their offset
utc_dict = {'Eastern Time (US & Canada)': -5, 
            'Central Time (US & Canada)': -6, 
            'Greenwich Mean Time': 0, 
            'Pacific Time (US & Canada)': -9, 
            'Western European Time': 0, 
            'Mountain Time (US & Canada)': -7, 
            'Indonesia Western Time': 7, 
            'Ecuador Time': -5, 
            'India Time': 5.5, 
            'Hawaii-Aleutian Time': -10, 
            'Atlantic Time (Canada)': -4, 
            'Alaska Time': -9, 
            'Australian Eastern Time': 10, 
            'China Time': 8,
            'Central European Time': 1, 
            'Iran Time': 3.5, 
            'Hong Kong Time': 8, 
            'Eastern European Time': 2, 
            'South Africa Time': 2, 
            'Pakistan Time': 5, 
            'Thailand Time': 7,  
            '': -999}

G = nx.Graph()
with open('locavore_twitter_search_results_timezone_mod.csv','rb') as f:
    reader=csv.reader(f)
    reader.next() # skip header row
    for row in reader:
        # screen_name is the name of the node with two attributes, color for representing the language 
        # and utc_offset label for different timezone offsets
        G.add_node(row[12],color=color_lang[row[8]],utc=row[14],utc_offset=utc_dict[row[14]]) # add the screen_name to the graph

# with all the graph nodes set draw the graph and color and label it
node_list=G.nodes(data=True) 

# make complete graphs and plot them each complete graph is a group of people with certain timezones.
# To do: draw complete graphs such that each graph corresponds to users who match a certain time zone
graph_list = [] # list will contain graphs (complete), first graph will consist of nodes (users) who are in the eastern time zone
for k in utc_dict.iterkeys():
    subgraph_nodes = [x for x in node_list if x[1]['utc'] == k]  # filter/group users based on their time zone
    subgraph_edges = combinations([x[0] for x in subgraph_nodes],2) # draw edges for each of these users connecting to other users in the graph (complete graph)
    H = nx.Graph() # create a new graph for this group (subgraph)
    H.add_nodes_from(subgraph_nodes)
    H.add_edges_from(subgraph_edges)
    graph_list.append(H) # add this subgraph to list of collected subgraphs (clusters)
    
nx.write_gexf(graph_list[21],'<name of gexf file you want to save UTC graph>')
