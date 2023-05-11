#!/usr/bin/env python
# -*- coding: utf-8 -*-


import xmlrpc.client
import datetime
import time
from itertools import combinations
from typing import List, Tuple



fd = open("a.config", encoding='utf-8')
content = fd.readlines()
fd.close()

slist = []
for i in range(len(content)):
    proxy = xmlrpc.client.ServerProxy('http://'+content[i].replace('\n', "")+':8000/')
    slist.append(proxy); 


def split_groups(nums: List[int], m: int) -> Tuple[List[List[List[int]]], int]:
    n = len(nums)
    nums.sort()
    result = []
    min_range_sum = float('inf')

    for combo in combinations(range(1, n), m - 1):
        combo = (0,) + combo + (n,)
        groups = [nums[combo[i]:combo[i+1]] for i in range(m)]
        print(groups)
        if any(len(group) < 2 for group in groups):
            continue
        range_sum = sum(max(group) - min(group) for group in groups)
        if range_sum < min_range_sum:
            min_range_sum = range_sum
            result.clear()
            result.append([])
            result[-1] = groups[:]
        elif range_sum == min_range_sum:
            result.append([])
            result[-1].extend(groups)

    return result, min_range_sum


def collect_flow():
    n = 0
    while(1):
        n += 1
        a="--------------------------------------------------------\n"
        time.sleep(1)
        node_dic ={}
        flow_list= []
        for i in range(len(content)):
            try:
                netinfo = slist[i].get_netinfo();
                node = {content[i].replace('\n', ""):netinfo.get("Input")}
                node_dic.update(node)
            except  Exception as e:
                node = {content[i].replace('\n', ""):0}
                node_dic.update(node)
        #print(node_dic)
        if(n >= 1 ):
            return node_dic

def part_info(groups, node_dic):    
    print("enter part_info")
    #print(groups)
    #print(node_dic)
    list_node = []
    for i in range(len(groups)):
        for j in range(len(groups[i])):
            list_node.append([])
            for k in range(len(groups[i][j])):
                num = groups[i][j][k]
                key = list(node_dic.keys())[list(node_dic.values()).index(num)]
                list_node[j].append(key)
                node_dic.pop(key)
    print(list_node)
    part_list = []
    for i in range(len(list_node)):
        part_list.append([])
        for j in range(len(list_node[i])):
            proxy = xmlrpc.client.ServerProxy('http://'+list_node[i][j]+':8000/')
            #print (proxy)
            part_list[i].append(proxy); 
    #print(part_list)
    while(1):
        for i in range(len(list_node)):
             print("------------part "+ str(i+1)+"-------------")
             tmp_flow = 0
             for j in range(len(list_node[i])):
                 try:
                     netinfo = part_list[i][j].get_netinfo();
                     node = {list_node[i][j]:netinfo.get("Input")}
                     print(node)
                     tmp_flow += netinfo.get("Input")
                 except  Exception as e:
                     node ={list_node[i][j]:0}
                     print(node)
             print("total flow :" + str(tmp_flow ))

if __name__ == '__main__':
    allnode_dic = {}
    allnode_dic = collect_flow()
    print(allnode_dic)

    nums= list(allnode_dic.values())
    #print(nums)
    m = 2
    groups, min_range_sum = split_groups(nums, m)
    print("Groups:", groups)
    print("Minimum range sum:", min_range_sum)

    part_info(groups, allnode_dic)

