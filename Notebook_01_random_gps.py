import time
from datetime import datetime
from threading import Thread
from collections import deque
import requests
from online_traffics.maths import rnd
# from geopy.distance import vincenty
import json
osrm_host = 'http://localhost:5000'

tehran = [
    [35.788158, 51.328564],
    [35.766610, 51.263318],
    [35.732402, 51.205000],
    [35.682704, 51.229829],
    [35.614201, 51.374178],
    [35.617017, 51.470026],
    [35.692083, 51.493699],
    [35.790657, 51.491336],
]


class Motor:
    def __init__(self, name, lat, lng, interval=20):
        self.name = name
        self.location = [lat, lng]
        self.loc_stack = deque()
        self.route = None
        self.thread = Thread(target=self.play)
        self.interval = interval

    def ack_location(self):
        self.loc_stack.append(tuple(self.location))
        if len(self.loc_stack) == 2:
            # print(f'/match/v1/driving/{";".join([str(loc[1]) + "," + str(loc[0]) for loc in self.loc_stack])}?steps=true&overview=full&annotations=true')
            res = requests.get(osrm_host + f'/match/v1/driving/{";".join([str(loc[1]) + "," + str(loc[0]) for loc in self.loc_stack])}?steps=false&overview=false&annotations=true')
            res = res.json()
            if 'matchings' in res:
                # d = vincenty(self.loc_stack[-2], self.loc_stack[-1]).m
                # v = d / self.interval
                nodes = res['matchings'][0]['legs'][0]['annotation']['nodes']
                # TODO maybe find best 2 nodes
                for i, prev in enumerate(nodes[: -1]):
                    next = nodes[i + 1]
                    mid = (locations[prev][0] + locations[next][0]) / 2, (locations[prev][1] + locations[next][1]) / 2
                    direction = locations[next][0] - locations[prev][0], locations[next][1] - locations[prev][1]
                    direction = [0, 1, 2, 3][3]
                    indexes = round((mid[0] - a_lat) / rho), round((mid[1] - a_lng) / rho)
            self.loc_stack.popleft()
        # requests.get('{}/{}/@{},{}'.format(host, self.name, *self.location))

    def dst(self, dst):
        while True:
            try:
                self.route = requests.get(osrm_host + '/route/v1/driving/{},{};{},{}'.format(
                    self.location[1], self.location[0], dst[1], dst[0]
                ), params={'steps': 'true'}).json()
                break
            except: time.sleep(.2)
        self.route = self.route['routes'][0]['legs'][0]['steps']
        self.route = [{
            'destination': [step['maneuver']['location'][1], step['maneuver']['location'][0]],
            'duration': step['duration'],
            'distance': step['distance'],
        } for step in self.route]

    def move(self, ammo):
        while ammo and self.route:
            step = self.route[0]
            if ammo >= step['duration']:
                self.location = step['destination']
                ammo -= step['duration']
                self.route = self.route[1:]
            else:
                duration = step['duration']
                step['duration'] -= ammo
                step['distance'] *= step['duration'] / duration
                self.location[0] += (step['destination'][0] - self.location[0]) * ammo / duration
                self.location[1] += (step['destination'][1] - self.location[1]) * ammo / duration
                ammo = 0
        return ammo

    def play(self):
        remain = 0
        while True:
            if not self.route:
                print("-- {}'s current route finished --".format(self.name))
                self.dst(rnd(tehran))
            remain = self.move(ammo=self.interval + remain)
            self.ack_location()
            time.sleep(self.interval / 72)


if __name__ == '__main__':
    motors = [Motor(name, *rnd(tehran)) for name in [
        'shahin',
        # 'alireza',
        # 'mehrad',
        # 'mohsen',
        # 'novid',
        # 'mohammad',
        # 'naqi',
        # 'taqi',
        # 'javad',
        # 'kazem',
        #
        # 'nosrat',
        # 'effat',
        # 'shokat',
        # 'sakineh',
        # 'halimeh',
        # 'naemeh',
        # 'maryam',
        # 'zahra',
        # 'narjes',
        # 'zeynab',
        #
        # 'bil',
        # 'jack',
        # 'muses',
        # 'nick',
        # 'liam',
        # 'william',
        # 'james',
        # 'benjamin',
        # 'mason',
        # 'logan',
        #
        # 'iris',
        # 'zeus',
        # 'hera',
        # 'poseidon',
        # 'demeter',
        # 'ares',
        # 'athena',
        # 'apollo',
        # 'hermes',
        # 'artemis',
        #
        # 'thor',
        # 'odin',
        # 'ironman',
        # 'vision',
        # 'hulk',
        # 'thanos',
        # 'superman',
        # 'captain',
        # 'spiderman',
        # 'flash'
    ]]
    for motor in motors:
        motor.thread.start()
