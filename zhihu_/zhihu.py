# -*- coding: utf-8 -*-

import requests
#from parsel import Selector
from UA import USER_AGENT
import random
from copyheaders import headers_raw_to_dict
import time
from requests_toolbelt.multipart.encoder import MultipartEncoder
import execjs

class zhihu_login(object):
    def __init__(self, username, password):
        self.s = requests.session()
        self.username = username
        self.password = password
        self.headers = {
            'user-agent': random.choice(USER_AGENT)
        }
        self.raw_headers = b"""
        accept: application/json, text/plain, */*
        accept-encoding: gzip, deflate, br
        accept-language: zh-CN,zh;q=0.9
        authorization: oauth c3cef.......
        origin: https://www.zhihu.com
        referer: https://www.zhihu.com/signup?next=%2F
        Connection: keep-alive
        x-udid: AKDu8MXbgg2PTm-3NTrMlS4TClkyC9ye7Js=
        """
    def get_headers(self):
        headers = self.headers
        response = self.s.get('https://www.zhihu.com/signup?next=%2F', headers=headers)
        headers.update(headers_raw_to_dict(self.raw_headers))
        #随机的UA可能导致response.cookies空值
        headers['x-xsrftoken'] = response.cookies['_xsrf']
        return headers

    def get_data(self, captcha=''):
        client_id = 'c3cef7c66a1843f8b3a9.......'
        timestamp = int(time.time() * 1000)
        js1 = execjs.compile(open('js.txt', 'r').read())
        signature = js1.call('run', 'password', timestamp)

        data = {
            'client_id': client_id, 'grant_type': 'password',
            'timestamp': str(timestamp), 'source': 'com.zhihu.web',
            'signature': signature, 'username': self.username,
            'password': self.password, 'captcha': captcha,
            'lang': 'en', 'ref_source': 'homepage', 'utm_source': ''
        }
        return data

    def checkcapthca(self, headers, cn =True):
        #用session发此请求以让服务器验证，同时也检验是否存在验证码
        if cn:
            url = 'https://www.zhihu.com/api/v3/oauth/captcha?lang=cn'
        else:
            url = 'https://www.zhihu.com/api/v3/oauth/captcha?lang=en'
        headers.pop('x-xsrftoken')
        response = self.s.get(url, headers=headers)
        print(response.json())

    def login(self):
        headers = self.get_headers()
        data = self.get_data()
        self.checkcapthca(headers)
        encoder = MultipartEncoder(
            data, boundary='----WebKitFormBoundarycGPN1xiTi2hCSKKZ')
        headers['Content-Type'] = encoder.content_type
        #每一步的url都不一样，参数也不尽相同
        response = self.s.post('https://www.zhihu.com/api/v3/oauth/sign_in', headers=headers, data=encoder.to_string())
        print(response.status_code)

    def get_session(self):
        # 返回s以登陆其他网址
        self.login()
        return self.s






