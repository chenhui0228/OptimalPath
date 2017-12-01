import requests
import json

BASE_URL = 'http://10.2.5.64/test'


class RequestAPI:
    def __init__(self):
        pass

    def initialize(self, url, data=None):
        res = requests.post(url, data=data)
        return json.load(res.text)

    def go(self, url, data):
        res = requests.post(url, data=data)
        return json.load(res.text)


class Map:
    def __init__(self):
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
        self.__genarate_map()

    def __genarate_map(self):
        data = {'name': 'chenhui'}
        ret = self.request.initialize('http://10.2.5.64/test')
        if ret.msg == 'OK':
            self.ai = (ret.state.ai.x, ret.state.ai.y)
            for w in ret.state.walls:
                self.walls.append((w.x, w.y))
            for p in ret.state.jobs:
                self.__packages = [(p.x, p.y)]
                self.packages.append((p.x, p.y, p.value))
            self.score = ret.state.score
            self.id = ret.id

    def go(self, direction):
        url = 'http://10.2.5.64/test/' + self.id + '/move'
        data = {'direction': direction}
        __packages_now = []
        packages_now = []
        ret = self.request.go(url, data)
        if ret.msg == 'OK':
            self.ai = (ret.state.ai.x, ret.state.ai.y)
            for p in ret.state.jobs:
                __packages_now.append((p.x, p.y))
                packages_now.append((p.x, p.y, p.value))
            self.score = self.score + ret.reward
            if cmp(self.__packages.sort(), __packages_now.sort()) != 0:
                self.__packages = __packages_now
                self.packages = packages_now
                self.package_newest = True
            else:
                self.package_newest = False
            self.end = ret.done
