#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import time

import pymysql
import json
import requests

def get_agent_headers():
    headers = {
        'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
        'DNT': "1",
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Connection': 'keep-alive',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-CN;q=0.8,en;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
    }

def get_db_connection():
    conn = pymysql.connect(host='localhost', port=3306, user='stock', password='stock', database='stock')
    return conn

def print_current_datatime():
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

# get cpc distribution data
def get_pcp_distribution_data_from_xuangubao():
    print("Start to get pcp distribution  data from xuangubao api")
    print_current_datatime()

    api_url = "https://flash-api.xuangubao.cn/api/market_indicator/pcp_distribution";
    json_data = json.loads(requests.get(api_url).text)
    print(json_data)
    db_conn = get_db_connection()

    try:
        with db_conn.cursor() as cursor:
            today = time.strftime('%Y%m%d', time.localtime(time.time()))
            data = json_data["data"]
            delete__sql = "delete from tbl_pcp_distribution where date = %s" % (today)
            insert_sql = "insert into tbl_pcp_distribution(date,total_count, halt_count, limit_down_count, limit_up_count, st_limit_down_count, st_limit_up_count, \
                          range_p0,range_p1,range_p2,range_p3,range_p4,range_p5,range_p6,range_p7,range_p8,range_p9,range_p10,range_p20, \
                          range_m1,range_m2,range_m3,range_m4,range_m5,range_m6,range_m7,range_m8,range_m9,range_m10,range_m20 ,data_ts, create_time)\
                          values(%s,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%s)" % \
                          (today, data['total_count'], data['halt_count'], data['limit_down_count'],data['limit_up_count'], data['st_limit_down_count'], data['st_limit_up_count'],\
                          data['0'],data['1'],data['2'],data['3'],data['4'],data['5'],data['6'],data['7'],data['8'],data['9'],data['10'],data['20'],\
                          data['-1'],data['-2'],data['-3'],data['-4'],data['-5'],data['-6'],data['-7'],data['-8'],data['-9'],data['-10'],data['-20'], data['ts'], 'now()')
  
            cursor.execute(delete__sql)
            cursor.execute(insert_sql)
            db_conn.commit()
        
    except Exception as e:
        db_conn.rollback()
        print(e)
    finally:
        db_conn.close()

    print_current_datatime()
    print("End------")


# get rise and fall count data
def get_rise_fall_data_from_xuangubao():
    print("Start to get rise and fall count data from xuangubao api")
    print_current_datatime()

    api_url = "https://flash-api.xuangubao.cn/api/market_indicator/line?fields=rise_count,fall_count";
    json_data = json.loads(requests.get(api_url).text)
    print(json_data)
    db_conn = get_db_connection()

    try:
        with db_conn.cursor() as cursor:
            today = time.strftime('%Y%m%d', time.localtime(time.time()))
            delete__sql = "delete from tbl_rise_fall_count where date = %s" % (today)
            cursor.execute(delete__sql)
            for d in json_data["data"]:
                insert_sql = "insert into tbl_rise_fall_count(date,rise_count,fall_count,data_ts,data_ts_format,create_time) values('%s',%d,%d,%d,'%s',%s)" % \
                          (today, d['rise_count'], d['fall_count'], d['timestamp'], time.strftime('%Y-%m-%d-%H:%M:%S', time.localtime(d['timestamp'])), 'now()')
                cursor.execute(insert_sql)
            
            db_conn.commit()
        
    except Exception as e:
        db_conn.rollback()
        print(e)
    finally:
        db_conn.close()

    print_current_datatime()
    print("End------")


# get limit up and down count data
def get_limit_up_down_data_from_xuangubao():
    print("Start to get limit up and down count data from xuangubao api")
    print_current_datatime()

    api_url = "https://flash-api.xuangubao.cn/api/market_indicator/line?fields=limit_up_count,limit_down_count";
    json_data = json.loads(requests.get(api_url).text)
    print(json_data)
    db_conn = get_db_connection()

    try:
        with db_conn.cursor() as cursor:
            today = time.strftime('%Y%m%d', time.localtime(time.time()))
            delete__sql = "delete from tbl_limit_up_down_count where date = %s" % (today)
            cursor.execute(delete__sql)
            for d in json_data["data"]:
                insert_sql = "insert into tbl_limit_up_down_count(date,limit_up_count,limit_down_count,data_ts,data_ts_format,create_time) values('%s',%d,%d,%d,'%s',%s)" % \
                          (today, d['limit_up_count'], d['limit_down_count'], d['timestamp'], time.strftime('%Y-%m-%d-%H:%M:%S', time.localtime(d['timestamp'])), 'now()')
                cursor.execute(insert_sql)
            
            db_conn.commit()
        
    except Exception as e:
        db_conn.rollback()
        print(e)
    finally:
        db_conn.close()

    print_current_datatime()
    print("End------")

def main():
    #get_pcp_distribution_data_from_xuangubao()
    #get_rise_fall_data_from_xuangubao()
    get_limit_up_down_data_from_xuangubao()

if __name__ == "__main__":
    main()
    