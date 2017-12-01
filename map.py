#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
import json


BASE_URL = 'http://10.2.5.64/test'


'''
定义HTTP请求统一接口
'''
class RequestAPI:
    def __init__(self):
        self.headers = {'Content-Type': 'application/json'}

    def initialize(self, url, data=None):
        res = requests.post(url, data=data, headers=self.headers)
        return json.loads(res.text)

    def go(self, url, data):
        res = requests.post(url, data=data, headers=self.headers)
        return json.loads(res.text)


'''
定义地图，包含ai小哥位置，包裹位置，障碍物位置等信息
'''
class Map:
    def __init__(self, name):
        self.request = RequestAPI()
        self.ai = None
        self.walls = []
        self.score = 0
        self.__packages = []
        self.packages = []
        self.id = ''
        self.end = False
        self.package_newest = False
        # self.direction = ''
        self.__genarate_map(name)

    '''
    初始化地图
    '''
    def __genarate_map(self, name):
        data = {'name': name}
        ret = self.request.initialize(BASE_URL, data=json.dumps(data))
        if ret['msg'] == 'OK':
            self.ai = (ret['state']['ai']['x'], ret['state']['ai']['y'])
            for w in ret['state']['walls']:
                self.walls.append((w['x'], w['y']))
            for p in ret['state']['jobs']:
                self.__packages.append((p['x'], p['y']))
                self.packages.append((p['x'], p['y'], p['value']))
            self.score = ret['state']['score']
            self.id = ret['id']

    '''
    每走一步，返回分数和更新地图
    '''
    def go(self, direction):
        url = BASE_URL + '/' + self.id + '/move'
        data = {'direction': direction}
        __packages_now = []
        packages_now = []
        ret = self.request.go(url, data=json.dumps(data))
        if ret['msg'] == 'OK':
            self.ai = (ret['state']['ai']['x'], ret['state']['ai']['y'])
            for p in ret['state']['jobs']:
                __packages_now.append((p['x'], p['y']))
                packages_now.append((p['x'], p['y'], p['value']))
            self.score = self.score + ret['reward']
            self.packages = packages_now
            if cmp(self.__packages.sort(), __packages_now.sort()) != 0:
                self.__packages = __packages_now
                self.package_newest = True
            else:
                self.package_newest = False
            self.end = ret['done']
