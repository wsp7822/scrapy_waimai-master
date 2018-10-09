# -*- coding: utf-8 -*-
"""连接MYSQL"""

# import mysql.connector
import pymysql

from waimai import settings

cnx = pymysql.connect(
    user=settings.MYSQL_USER,
    password=settings.MYSQL_PASSWD,
    host=settings.MYSQL_HOST,
    database=settings.MYSQL_DBNAME
)

cur = cnx.cursor()
'''
Created on 2017年11月27日
@author: liuyazhuang
'''
# coding=utf-8
# 导入pymysql的包
import pymysql
# import pymysql.cursors
#
# # 获取一个数据库连接，注意如果是UTF-8类型的，需要制定数据库
# # port 必须是数字不能为字符串
# connection = pymysql.connect(host='localhost',
#                              user='root',
#                              password='123456',
#                              db='mydb',
#                              port=3306,
#                              charset='utf8')
# try:
#     # 获取一个游标
#     with connection.cursor() as cursor:
#         sql = 'select * from user'
#         cout = cursor.execute(sql)
#         print("数量： " + str(cout))
#
#         for row in cursor.fetchall():
#             # 注意int类型需要使用str函数转义
#             print("ID: " + str(row[0]) + '  名字： ' + row[1] + "  性别： " + row[2])
#         connection.commit()
#
# finally:
#     connection.close()
