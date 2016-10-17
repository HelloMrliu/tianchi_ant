# coding=utf-8
from __future__ import unicode_literals
import pandas as pd
import codecs


result_path = '../combine_result.csv'

result_dict = dict()
with codecs.open(result_path, 'r', 'utf-8') as read_file:
    for line in read_file:
        info_list = line.strip('\n').split(',')
        uid = info_list[0]
        cid = info_list[1]
        date_received = info_list[2]
        result = info_list[3]
        temp_tun = (uid,cid,date_received,result)
        if uid in result_dict:
            result_dict[uid].append(temp_tun)
        else:
            result_dict[uid] = list()
            result_dict[uid].append(temp_tun)

for uid in result_dict:
    res_list = result_dict[uid]
    if len(res_list) == 0:
        continue
    else:
        std_val = res_list[0][3]
        std_time = res_list[0][2]
        count = 0
        for res in res_list:
            if abs(float(std_val) - float(res[3])) < float(std_val) / 5  and res[2] == std_time:
                count += 1
        if count == len(res_list) and count >= 2:
            print res_list[0][0]




