#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：POI_20251027 
@File    ：get_pois.py
@IDE     ：PyCharm 
@Author  ：疯子同学.
@Email   ：2537118325@qq.com
@Date    ：2025/10/27 16:56 
@Brief   ：现代地图学实验设计一：通过百度地图获取POI数据，百度地图官网：https://map.baidu.com/@12575211,3253582,12z
"""
import csv
import random
from datetime import datetime
from time import sleep
import requests


# 爬取的关键字
wd = '美食'
# 长沙市
list_area_id = ['158']

# 保存数据的文件名
now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
csv_filename = f'{now}_{wd}.csv'
f = open(f'result_POI/{now}_{wd}.csv', mode='a', encoding='utf-8-sig', newline='')
csv_writer = csv.DictWriter(f, fieldnames=[
    '关键字',
    '名称',
    '省(州)',
    '市',
    '县/区',
    '电话',
    '地址',
    '经度',
    '纬度',
    '门店图片地址',
    '类型',
    '行政区域属性'
])
csv_writer.writeheader()

# 循环爬取每个城市的POI数据
for c in list_area_id:
    page = 0
    while True:
        print(f'-------------------------正在爬取城市{c}的第{page + 1}页数据-------------------------')
        sleep(random.randint(1, 3))
        url = 'https://map.baidu.com/@12575211,3253582,12z?'
        data = {
            'newmap': '1',
            'reqflag': 'pcmap',
            'biz': '1',
            'from': 'webmap',
            'da_par': 'direct',
            'pcevaname': 'pc4.1',
            'qt': 's',
            'c': c,
            'wd': wd,
            'pn': page,
            'db': '0'
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
        }
        response = requests.get(url=url, params=data, headers=headers)
        searchResult = response.json().get('content', [])
        if not searchResult:
            print('当前页没有数据！')
            break
        for items in searchResult:
            try:
                data = {
                    '关键字': wd,
                    '名称': items['name'],
                    '省(州)': items['admin_info']['province_name'],
                    '市': items['admin_info']['city_name'],
                    '县/区': items['admin_info']['area_name'],
                    '电话': items['ext']['detail_info'].get('phone', ''),
                    '地址': items['addr'],
                    '经度': items['x'],
                    '纬度': items['y'],
                    '门店图片地址': items['ext']['detail_info'].get('image', ''),
                    '类型': items['std_tag'],
                    '行政区域属性': '县/区',
                }
                csv_writer.writerow(data)
                print(data)
            except KeyError:
                continue
        page += 1
f.close()
print('数据爬取完毕！已保存至：', csv_filename)
