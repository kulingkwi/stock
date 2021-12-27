#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import time
import sys
from datetime import datetime

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
    conn = pymysql.connect(host='localhost', port=3306, user='stock', password='stock', database='stock', charset='utf8')
    return conn

def print_current_datatime():
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

# get cpc distribution data
def get_pcp_distribution_data_from_xuangubao(trade_date):
    print("Start to get pcp distribution  data from xuangubao api")
    print_current_datatime()

    api_url = "https://flash-api.xuangubao.cn/api/market_indicator/pcp_distribution";
    json_data = json.loads(requests.get(api_url).text)
    print(api_url)
    db_conn = get_db_connection()

    try:
        with db_conn.cursor() as cursor:
            data = json_data["data"]
            delete__sql = "delete from tbl_pcp_distribution where date = '%s'" % (trade_date)
            insert_sql = "insert into tbl_pcp_distribution(date,total_count, halt_count, limit_down_count, limit_up_count, st_limit_down_count, st_limit_up_count, \
                          range_p0,range_p1,range_p2,range_p3,range_p4,range_p5,range_p6,range_p7,range_p8,range_p9,range_p10,range_p20, \
                          range_m1,range_m2,range_m3,range_m4,range_m5,range_m6,range_m7,range_m8,range_m9,range_m10,range_m20 ,data_ts, create_time)\
                          values('%s',%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%s)" % \
                          (trade_date, data['total_count'], data['halt_count'], data['limit_down_count'],data['limit_up_count'], data['st_limit_down_count'], data['st_limit_up_count'],\
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
    print("End------\n")


# get rise and fall count data
def get_rise_fall_data_from_xuangubao(trade_date):
    print("Start to get rise and fall count data from xuangubao api")
    print_current_datatime()

    api_url = "https://flash-api.xuangubao.cn/api/market_indicator/line?fields=rise_count,fall_count&date="+trade_date;
    json_data = json.loads(requests.get(api_url).text)
    print(api_url)
    db_conn = get_db_connection()

    try:
        with db_conn.cursor() as cursor:
            delete__sql = "delete from tbl_rise_fall_count where date = '%s'" % (trade_date)
            cursor.execute(delete__sql)
            for d in json_data["data"]:
                insert_sql = "insert into tbl_rise_fall_count(date,rise_count,fall_count,data_ts,data_ts_format,create_time) values('%s',%d,%d,%d,'%s',%s)" % \
                          (trade_date, d['rise_count'], d['fall_count'], d['timestamp'], time.strftime('%Y-%m-%d-%H:%M:%S', time.localtime(d['timestamp'])), 'now()')
                cursor.execute(insert_sql)
            
            db_conn.commit()
        
    except Exception as e:
        db_conn.rollback()
        print(e)
    finally:
        db_conn.close()

    print_current_datatime()
    print("End------\n")


# get limit up and down count data
def get_limit_up_down_data_from_xuangubao(trade_date):
    print("Start to get limit up and down count data from xuangubao api")
    print_current_datatime()

    api_url = "https://flash-api.xuangubao.cn/api/market_indicator/line?fields=limit_up_count,limit_down_count&date="+trade_date;
    json_data = json.loads(requests.get(api_url).text)
    print(api_url)
    db_conn = get_db_connection()

    try:
        with db_conn.cursor() as cursor:
            delete__sql = "delete from tbl_limit_up_down_count where date = '%s'" % (trade_date)
            cursor.execute(delete__sql)
            for d in json_data["data"]:
                insert_sql = "insert into tbl_limit_up_down_count(date,limit_up_count,limit_down_count,data_ts,data_ts_format,create_time) values('%s',%d,%d,%d,'%s',%s)" % \
                          (trade_date, d['limit_up_count'], d['limit_down_count'], d['timestamp'], time.strftime('%Y-%m-%d-%H:%M:%S', time.localtime(d['timestamp'])), 'now()')
                cursor.execute(insert_sql)
            
            db_conn.commit()
        
    except Exception as e:
        db_conn.rollback()
        print(e)
    finally:
        db_conn.close()

    print_current_datatime()
    print("End------\n")

#get quotations event
def get_quotations_event_data_from_xuangubao(trade_date):
    print("Start to get quotations event history data from xuangubao api")
    print_current_datatime()

    db_conn = get_db_connection()

    try:
        last_time_stamp = int(round(datetime.timestamp(datetime.strptime(trade_date + "-15:01:00", "%Y-%m-%d-%H:%M:%S"))))
        first_time_stamp = int(round(datetime.timestamp(datetime.strptime(trade_date + "-09:14:00", "%Y-%m-%d-%H:%M:%S"))))
        stop_sign = 1

        with db_conn.cursor() as cursor:

            delete__sql = "delete from tbl_quotation_event_history where event_timestamp > %d and event_timestamp < %d" % (first_time_stamp, last_time_stamp)
            cursor.execute(delete__sql)

            while(stop_sign > 0 and last_time_stamp > first_time_stamp):
                api_url = "https://flash-api.xuangubao.cn/api/event/history?count=50&types=10001,10005,10003,10002,10006,10004,10012,10014,10009,10010,11000,11001&timestamp=%d" % (last_time_stamp);
                json_data = json.loads(requests.get(api_url).text)
                print(api_url)
                if (json_data["code"] == 20000 and json_data["data"] is not None and  len(json_data["data"]) > 0):
                    for data in json_data["data"]:
                        if (data["event_timestamp"] > first_time_stamp):
                            insert_sql = "insert into tbl_quotation_event_history (msg_id, date, target, event_type, event_timestamp, event_timestamp_format, good_or_bad, stock_abnormal_event_data, plate_abnormal_event_data, create_time) values \
                            (%d, '%s','%s', %d, %d, '%s', %d, '%s', '%s', %s)" % \
                            (data["id"], time.strftime('%Y-%m-%d', time.localtime(data["event_timestamp"])),data["target"], data["event_type"], data["event_timestamp"], time.strftime('%Y-%m-%d-%H:%M:%S', time.localtime(data["event_timestamp"])), data["good_or_bad"],
                            json.dumps(data["stock_abnormal_event_data"]), json.dumps(data["plate_abnormal_event_data"]), 'now()')   
                            cursor.execute(insert_sql)
                            #print(insert_sql)

                    last_time_stamp = json_data["data"][-1]["event_timestamp"] if (last_time_stamp > json_data["data"][-1]["event_timestamp"]) else (json_data["data"][-1]["event_timestamp"] - 1)
                    stop_sign = 1

                else:
                    stop_sign = 0

            db_conn.commit()
    except Exception as e:
        db_conn.rollback()
        print(e)
    finally:
        db_conn.close()

    print_current_datatime()
    print("End------\n")


#get quotations message
def get_msg_data_from_xuangubao(trade_date):
    print("Start to get quotations message data from xuangubao api")
    print_current_datatime()

    db_conn = get_db_connection()

    try:
        last_time_stamp = int(round(datetime.timestamp(datetime.strptime(trade_date + "-16:00:00", "%Y-%m-%d-%H:%M:%S"))))
        first_time_stamp = int(round(datetime.timestamp(datetime.strptime(trade_date + "-09:00:00", "%Y-%m-%d-%H:%M:%S"))))
        stop_sign = 1

        with db_conn.cursor() as cursor:

            delete__sql = "delete from tbl_msg where msg_ts > %d and msg_ts < %d" % (first_time_stamp, last_time_stamp)
            cursor.execute(delete__sql)

            last_msg_id = 0
            while(stop_sign > 0 and last_time_stamp > first_time_stamp):
                api_url = "https://api.xuangubao.cn/api/pc/msgs?subjids=35&limit=30&msgIdMark=%d" % (last_msg_id);
                print(api_url)
                json_data = json.loads(requests.get(api_url).text)
                if (json_data["NewMsgs"] is not None and  len(json_data["NewMsgs"]) > 0):
                    for data in json_data["NewMsgs"]:
                        if (data["CreatedAtInSec"] > first_time_stamp):
                            insert_sql = "insert into tbl_msg (date, msg_id, msg_ts, msg_ts_format, msg_type, msg_title, msg_content, create_time) values ('%s', %d, %d, '%s', %d, '%s', '%s', %s)" % \
                            (time.strftime('%Y-%m-%d', time.localtime(data["CreatedAtInSec"])), int(data["Id"]), data["CreatedAtInSec"],  time.strftime('%Y-%m-%d-%H:%M:%S', time.localtime(data["CreatedAtInSec"])), 35, data["Title"], json.dumps(data), 'now()')   
                            cursor.execute(insert_sql)
                            
                    last_msg_id = int(json_data["TailMsgId"])
                    last_time_stamp = int(json_data["TailMark"])
                    stop_sign = 1

                else:
                    stop_sign = 0

            db_conn.commit()
    except Exception as e:
        db_conn.rollback()
        print(e)
    finally:
        db_conn.close()

    print_current_datatime()
    print("End------\n")

# get limit up and down stock pool data
def get_pool_limit_up_down_data_from_xuangubao(trade_date):
    print("Start to get limit up and down count data from xuangubao api")
    print_current_datatime()
    today = time.strftime('%Y-%m-%d', time.localtime(time.time()))

    limit_up_api_url = "https://flash-api.xuangubao.cn/api/pool/detail?pool_name=limit_up&date="+ ("" if today == trade_date else trade_date);
    limit_down_api_url = "https://flash-api.xuangubao.cn/api/pool/detail?pool_name=limit_down&date="+ ("" if today == trade_date else trade_date);
    limit_up_broken_api_url = "https://flash-api.xuangubao.cn/api/pool/detail?pool_name=limit_up_broken&date="+ ("" if today == trade_date else trade_date);
    limit_down_broken_api_url = "https://flash-api.xuangubao.cn/api/pool/detail?pool_name=limit_down_broken&date="+ ("" if today == trade_date else trade_date);
    resp_data = [{"type": "limit_up", "url": limit_up_api_url, "stock_list": json.loads(requests.get(limit_up_api_url).text)}, 
                    {"type": "limit_down", "url": limit_down_api_url, "stock_list": json.loads(requests.get(limit_down_api_url).text)},\
                    {"type": "limit_up_broken", "url": limit_up_broken_api_url, "stock_list": json.loads(requests.get(limit_up_broken_api_url).text)}, 
                    {"type": "limit_down_broken", "url": limit_down_broken_api_url, "stock_list": json.loads(requests.get(limit_down_broken_api_url).text)}]
    db_conn = get_db_connection()

    try:
        with db_conn.cursor() as cursor:
            for data in resp_data:
                print("type: %s   url: %s" % (data["type"], data["url"]))
                delete__sql = "delete from tbl_pool_limit_up_down where date = '%s' and type = '%s'" % (trade_date, data["type"])
                cursor.execute(delete__sql)
                for d in data["stock_list"]["data"]:
                    if d is not None and len(d) > 0 :
                        insert_sql = "insert into tbl_pool_limit_up_down(date,type,stock_code,stock_name,reason, content,create_time) values('%s', '%s','%s','%s','%s','%s',%s)" % \
                                (trade_date, data["type"], d['symbol'], d['stock_chi_name'], (d["surge_reason"]["stock_reason"] if d["surge_reason"] is not None and d["surge_reason"]["stock_reason"] is not None else ""), json.dumps(d), 'now()')
                        cursor.execute(insert_sql)
            
            db_conn.commit()
        
    except Exception as e:
        db_conn.rollback()
        print(e)
    finally:
        db_conn.close()

    print_current_datatime()
    print("End------\n")

def default(trade_date):
    get_pcp_distribution_data_from_xuangubao(trade_date)
    get_rise_fall_data_from_xuangubao(trade_date)
    get_limit_up_down_data_from_xuangubao(trade_date)
    get_quotations_event_data_from_xuangubao(trade_date)
    get_msg_data_from_xuangubao(trade_date)
    get_pool_limit_up_down_data_from_xuangubao(trade_date)

def main():
    trade_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    if (len(sys.argv) > 1):
        trade_date = sys.argv[1]
    if (len(sys.argv) > 2):
        func = sys.argv[2]
    else:
        func = default

    
    switcher = {
        "pcp":get_pcp_distribution_data_from_xuangubao, 
        "rise_fall": get_rise_fall_data_from_xuangubao,
        "limit_up_down": get_limit_up_down_data_from_xuangubao,
        "event": get_quotations_event_data_from_xuangubao,
        "msg": get_msg_data_from_xuangubao,
        "pool_limit_up_down": get_pool_limit_up_down_data_from_xuangubao}

    f = switcher.get(func, default)
    print(("trade date: %s, data: %s  \n") % (trade_date, f.__name__))
    
    f(trade_date)


if __name__ == "__main__":
    main()
    