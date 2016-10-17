# coding=utf-8
from __future__ import unicode_literals
import os
import codecs
import pandas


result_dir = '../result_data/'

name_list = os.listdir(result_dir)

count = 0
uid_list = list()
cid_list = list()
received_time_list = list()
result_list = list()

for file_name in name_list:
    file_path = result_dir + file_name
    temp_list = list()
    with codecs.open(file_path, 'r', 'utf-8') as read_file:
        for line in read_file:
            info_list = line.strip('\n').split(',')
            if count == 0:
                uid_list.append(info_list[0])
                cid_list.append(info_list[1])
                received_time_list.append(info_list[2])
            temp_list.append(info_list[3])
    result_list.append(temp_list)
    count += 1

new_result_list = list()
for index in range(len(result_list[0])):
    new_result_list.append(0.0)

for temp_list in result_list:
    for index in range(len(temp_list)):
        new_result_list[index] += float(temp_list[index])

length = len(result_list)
for index in range(len(uid_list)):
    new_result_list[index] = new_result_list[index] / length

with codecs.open('../combine_result.csv', 'w', 'utf-8') as write_file:
    for index in range(len(uid_list)):
        write_file.write(str(uid_list[index]) + ',' + str(cid_list[index]) + ',' + str(received_time_list[index]) + ',' + str("%.6f" % float(new_result_list[index])))
        write_file.write('\n')