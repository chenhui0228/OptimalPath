#!/usr/bin/python
# -*- coding: UTF-8 -*-

import const
import random
import itertools as its

'''
定义障碍物和非障碍物也非包裹的常量
'''
const.BLOCK = -1
const.NORMAL = -2

const.BLOCK_RATE = 0.2
const.PACKAGE_RATE = 0.4

class Map:
    def __init__(self, size=10):
        self.size = size
        self.__vertexes = list(its.product(range(0, self.size), range(0, self.size)))
        self.__packages = []
        self.__blocks = []
        self.packages = {}
        self.blocks = {}
        self.__genarate_map()

    '''
    根据地图大小生产地图，并根据包裹占比和障碍物占比生成包裹和障碍物
    '''
    def __genarate_map(self):
        if self.size < 0:
            raise Exception("Invalid map size!", self.size)
        package_total_number = int(self.size * self.size * const.PACKAGE_RATE)
        self.__packages = random.sample(self.__vertexes, package_total_number)
        block_total_number = int(self.size * self.size * const.BLOCK_RATE)
        self.__blocks = random.sample(list(set(self.__vertexes) ^ (set(self.__packages))), block_total_number)
        for i in range(package_total_number):
            x = self.__packages[i][0]
            y = self.__packages[i][1]
            self.packages[str(x)+'|'+str(y)] = self.size
        for i in range(block_total_number):
            x = self.__blocks[i][0]
            y = self.__blocks[i][1]
            self.blocks[str(x)+'|'+str(y)] = "B"

    def update_map(self):
        pass