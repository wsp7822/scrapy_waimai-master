import urllib

import requests
import json
import pymysql
import logging

import sys

from eleme import reqsetting

geohash = 'wx4ekbzmdyps'
latitude = '39.951386'
longitude = '116.23445'

offset = 0
limit = 25

db = pymysql.connect("127.0.0.1", "root", "123456", "eleme", charset='utf8')

logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s] %(name)s:%(levelname)s: %(message)s"
)

for index in range(4):
    # url = "https://www.ele.me/restapi/shopping/restaurants?extras%5B%5D=activities&geohash=" + str(geohash) + \
    #       "&latitude=" + str(latitude) + "&longitude=" + str(longitude) + "&offset=" + str(offset) + \
    #       "&limit=" + str(limit) + "&terminal=web"
    # print(url)
    # cookies = dict(SID='*', USERID='*',
    #                ubt_ssid="*"
    #                )
    # data = requests.get(url, cookies=cookies).json()

    weburl = "https://mainsite-restapi.ele.me/shopping/restaurants?"
    webheaders = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Cookie": "ubt_ssid=aljer72855q5kxhxn12ba0tylnxawxa8_2018-09-28; _utrace=908d16f73f446241d239a898c44f6b9d_2018-09-28; track_id=1538145248|77cf24f83819face4a33522503665aa609444b047f3ab200e4|4850253820df707e9623e2ad27a6a579; USERID=492048802; SID=2ZvKrBUPkVF3v1IdtepjciO3hs4jpD0QJztA",
        "Host": "mainsite-restapi.ele.me",
        "Origin": "https://www.ele.me",
        # "Referer":"https://www.ele.me/place/wx4g56v1d2m",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
    }
    req = urllib.request.Request(url=weburl, headers=webheaders)
    req = reqsetting()
    req.add_header("Refer", "https://www.ele.me/place/wx4em10hdzmd?latitude=39.952594&longitude=116.235477")  # 修改请求头的refer
    newUrl = req.get_full_url()
    params = {
        "extras[]": "activities",
        "geohash": "wx4em10hdzmd",
        "latitude": "39.952594",
        "longitude": "116.235477",
        "terminal": "web",
        "limit": 24,
        "offset": 0
    }
    params = urllib.parse.urlencode(params)  # 请求参数编码
    req.full_url = newUrl + params  # 重新生成url请求
    webpage = urllib.request.urlopen(req)
    contentBytes = webpage.read().decode("utf-8")

    data = json.loads(contentBytes)

    logging.info("offset:" + str(offset))
    logging.debug(data)
    if len(data) <= 0:
        logging.info("end")
        sys.exit(0)

    offset += limit
    for restaurant in data:
        for activitie in restaurant['activities']:
            if "type" in activitie and activitie['type'] is 102:
                attribute = json.loads(activitie["attribute"])
                for manjian in attribute:
                    name = restaurant["name"]
                    tips = activitie["tips"]
                    buy = manjian
                    discount = attribute[manjian]["1"]
                    cursor = db.cursor()
                    # SQL 插入语句
                    sql = "INSERT INTO activities(name, \
                           tips, buy, discount) \
                           VALUES ('%s', '%s', '%s', '%s')" % \
                          (name, tips, buy, discount)

                    # 执行sql语句
                    cursor.execute(sql)
                    # 提交到数据库执行
                    db.commit()

db.close()