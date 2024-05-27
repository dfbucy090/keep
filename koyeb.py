#!/usr/bin/python3
# -*- coding: utf8 -*-
import json
import requests
import os
# from sendNotify import send
import time
import datetime

List = []

def get_time_stamp(result):
    utct_date = datetime.datetime.strptime(result, "%Y-%m-%dT%H:%M:%S.%f%z")
    local_date = utct_date + datetime.timedelta(hours=8)
    local_date_srt = datetime.datetime.strftime(local_date, "%Y-%m-%d %H:%M:%S")
    return local_date_srt


def login(usr, pwd):
    session = requests.Session()
    login_url = 'https://app.koyeb.com/v1/account/login'
    headers = {
        'origin': 'https://app.koyeb.com',
        'referer': 'https://app.koyeb.com/auth/signin',
        'content-type': 'application/json',
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; PBEM00) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.52 Mobile Safari/537.36'
    }
    data = {
        'email': usr,
        'password': pwd
    }
    res = session.post(login_url, headers=headers, data=json.dumps(data))
    if res.status_code == 200:
        status = res.json()
        token = status.get('token').get('id')
        check_url = 'https://app.koyeb.com/v1/account/profile'
        check_head = {
            'authorization': f'Bearer {token}',
            'referer': 'https://app.koyeb.com/auth/signin',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; PBEM00) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.52 Mobile Safari/537.36'

        }
        resp = session.get(check_url, headers=check_head)
        if resp.status_code == 200:
            info = resp.json()
            List.append(f"账号`{info.get('user').get('name')}`登陆成功")
            List.append(f"ID：{info.get('user').get('id')}")
            List.append(f"注册日期：{get_time_stamp(info.get('user').get('created_at'))}")
            lastlogin_url = 'https://app.koyeb.com/v1/activities?offset=0&limit=2'
            lastlogin_head = {
                'authorization': f'Bearer {token}',
                'referer': 'https://app.koyeb.com/activity',
                'user-agent': 'Mozilla/5.0 (Linux; Android 10; PBEM00) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.52 Mobile Safari/537.36'

            }
            time.sleep(7)
            resg = session.get(lastlogin_url, headers=lastlogin_head)
            if resg.status_code == 200:
                lastlogin = resg.json()
                if lastlogin.get('count') > 1:
                    List.append(f"上次登录日期：{get_time_stamp(lastlogin.get('activities')[1].get('created_at'))}")
                List.append(f"当前登录日期：{get_time_stamp(lastlogin.get('activities')[0].get('created_at'))}")
                List.append(f"总登录次数：{lastlogin.get('count')}次")
            else:
                print(resg.text)
        else:
            print(resp.text)
    else:
        List.append('账号登陆失败: 账号或密码错误')
        List.append(res.text)


if __name__ == '__main__':
    i = 0
    if 'KOY_EB' in os.environ:
        users = os.environ['KOY_EB'].split('&')
        for x in users:
            i += 1
            name, pwd = x.split('-')
            List.append(f'===> [账号{str(i)}]Start <===')
            def login(name, pwd):
                # 假设 lastlogin 是在某处定义的
                lastlogin = some_function_to_get_lastlogin()
    
                # 确保 lastlogin 是一个字典
                if not isinstance(lastlogin, dict):
                raise ValueError("lastlogin should be a dictionary")
    
                # 使用默认值来避免 TypeError
                count = lastlogin.get('count', 0)
    
                if count > 1:
                   # 你的逻辑代码
                   pass
                else:
                   # 其他逻辑代码
                   pass

            # 假设 name 和 pwd 是在某处定义的
            login(name, pwd)

            List.append(f'===> [账号{str(i)}]End <===\n')
            time.sleep(1)
        tt = '\n'.join(List)
        print(tt)
        # send('koyeb', tt)
    else:
        print('未配置环境变量')
        # send('koyeb', '未配置环境变量')
