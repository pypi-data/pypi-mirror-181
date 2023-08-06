from socket import AF_INET, SOCK_DGRAM, socket
from datetime import datetime
from json import load as jload, dump as jdump
from random import randint
from flask import Flask, request, Response
from threading import Thread
from time import sleep, time, perf_counter
from copy import deepcopy
from .color import *


class _EndpointAction(object):
    def __init__(self, action):
        self.action = action

    def __call__(self, *args):
        self.action()
        return Response(status=200, headers={})


class _FlaskAppWrapper(object):
    def __init__(self, name, host, port, debug):
        self.app = Flask(name)
        self.host = host
        self.port = port
        self.debug = debug

    def run(self):
        self.app.run(host=self.host, port=self.port, debug=self.debug)

    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None):
        self.app.add_url_rule(endpoint, endpoint_name, _EndpointAction(handler))


class Lamp:
    def __init__(self, key: str, ip: str, port: int, group_id: int, json_settings_path: str = 'settings.json',
                 server_name: str = 'GyverLampServer', server_host: str = '0.0.0.0',
                 server_port: int = 32458, server_debug: bool = False, timeout_sync: int = 5,
                 log_data_request: bool = False, enable_task_list: bool = False):

        self.key = key
        self.ip = ip
        self.port = port
        self.group_id = 0
        self.json_settings_path = json_settings_path
        self.server_name = server_name
        self.server_host = server_host
        self.server_port = server_port
        self.server_debug = server_debug
        self.timeout_sync = timeout_sync

        self.__count_multi_requests = 0
        self.__sock = socket(AF_INET, SOCK_DGRAM)
        self.__log_data_request = log_data_request
        self.__enable_task_list = enable_task_list
        if self.__enable_task_list:
            self.__task_list = []
            self.__task_list_thread = Thread(target=self.__task_list_processing)
            self.__task_list_thread.start()

        self.__is_lamp_synced = False
        self.__save_settings_after_sync = False
        self.__last_request_time = 0
        self.__settings_data = {'brightness': '100', 'adc': '1', 'min_brightness': '0', 'max_brightness': '255',
                                'regime_change': '0', 'random_order_modes': '0', 'shift_period': '1', 'strip_type': '2',
                                'maximal_current': '15', 'work_hours_from': '0', 'work_hours_to': '0',
                                'matrix_orientation': '1', 'height': '16', 'width': '16', 'gmt': '16',
                                'city_id': '524901', 'mqtt_state': '0', 'mqtt_id': 'alexLamp123',
                                'mqtt_host': 'broker.mqttdashboard.com', 'mqtt_port': '1883', 'mqtt_login': 'gyver',
                                'mqtt_pass': '123456'}
        # self.__dawn_data = {'su_state': 0, 'mo_state': 0, 'tu_state': 0, 'we_state': 0, 'th_state': 0, 'fr_state': 0,
        #                     'sa_state': 0,
        #                     'su_hours': 0, 'mo_hours': 0, 'tu_hours': 0, 'we_hours': 0, 'th_hours': 0, 'fr_hours': 0,
        #                     'sa_hours': 0,
        #                     'su_mins': 0, 'mo_mins': 0, 'tu_mins': 0, 'we_mins': 0, 'th_mins': 0, 'fr_mins': 0,
        #                     'sa_mins': 0,
        #                     'brightness': 255, 'minutes_before_dawn': 5, 'minutes_after_dawn': 5}

        self.__default_settings_data = deepcopy(self.__settings_data)
        # self.__default_dawn_data = deepcopy(self.__dawn_data)

    def send_request(self, *args, **kwargs):
        self.__send_request(args, kwargs)

    def turn_off(self, *date):
        """Turn off the lamp"""
        if len(date) == 0:
            date = 'now'
        self.__send_request('0,0', date)

    def turn_on(self, *date):
        """ Turn on the lamp"""
        if len(date) == 0:
            date = 'now'
        self.__send_request('0,1', date)

    def min_brightness(self):
        """ Set the minimum brightness of the lamp """
        self.__send_request('0,2')

    def max_brightness(self):
        """ Set the maximum brightness of the lamp """
        self.__send_request('0,3')

    def back_mode(self, *date):
        """ """
        if len(date) == 0:
            date = 'now'
        self.__send_request('0,4', date)

    def next_mode(self, *date):
        """ Next mode """
        if len(date) == 0:
            date = 'now'
        self.__send_request('0,5', date)

    def set_mode(self, mode):
        """ Set mode """
        self.__send_request(f'0,6,{mode}')

    def set_mode_wifi(self, mode):
        """ 0 - AP, 1 - Local """
        self.__send_request(f'0,7,{mode}')

    def change_role(self, role):
        """ 0 - Slave, 1 - Master """
        self.__send_request(f'0,8,{role}')

    def change_group(self, group_id):
        """ Set group"""
        self.__send_request(f'0,9,{group_id}')

    def set_wifi(self, ssid, password):
        """ Set Wi-Fi credentials """
        self.__send_request(f'0,10,{ssid},{password}')

    def restart(self):
        """ Restart the lamp"""
        self.__send_request(f'0,11')

    def firmware_update(self):
        """ Update the firmware """
        self.__send_request(f'0,12')

    def sleep_timer(self, minutes: int):
        """ 0-255 minutes"""
        self.__send_request(f'0,13,{minutes}')

    def get_settings(self):
        return self.__settings_data

    def get_param(self, name: str) -> str:
        return self.__settings_data.get(name)

    def set_auto_sync_settings(self, state: bool):
        self.__send_request(f'20,2,{int(state)}')

    def sync_settings(self, auto_sync: bool = False, wait_sync: bool = True, timeout: int = None):
        self.__send_request(f'20,1,{int(auto_sync)}')
        if wait_sync:
            return self.__wait_sync_settings(timeout if timeout else self.timeout_sync)

    def settings(self, default_settings: bool = False, wait_sync: bool = False, *date, **kwargs):
        if len(date) == 0:
            date = 'now'
        data = ''
        settings = self.__default_settings_data if default_settings else self.__settings_data
        for key, value in kwargs.items():
            if key not in settings:
                continue
            self.__settings_data[key] = value
            settings[key] = value
        for value in settings.values():
            data += f',{value}'
        self.__send_request(f'1{data}', date)
        if wait_sync:
            return self.__wait_sync_settings(timeout=self.timeout_sync)

    def set_multi_requests(self, count: int = 3):
        self.__send_request(f'21,{count}')
        self.__count_multi_requests = count

    def start_server(self, wait_after_started: bool = False):
        Thread(target=self.__start_server).start()
        if wait_after_started:
            sleep(.1)

    def random_effects(self, count: int = 3, *date, **kwargs):
        if not 0 < count < 26:
            return
        data = f'2,{count}'
        random_num = randint(1, count)
        min_brightness = kwargs.get('min_brightness') if kwargs.get('min_brightness') else 50
        max_brightness = kwargs.get('max_brightness') if kwargs.get('max_brightness') else 50
        max_brightness, min_brightness = [max_brightness, min_brightness] if max_brightness > min_brightness else [
            min_brightness, max_brightness]
        for i in range(count):
            type_effect = randint(1, 7)
            fade_brightness = randint(0, 1)
            brightness = randint(min_brightness, max_brightness)
            adv_mode = kwargs.get('adv_mode') if kwargs.get('adv_mode') else randint(1, 5)
            sound_react = kwargs.get('sound_react') if kwargs.get('sound_react') else randint(1, 3)
            min_signal = kwargs.get('min_signal') if kwargs.get('min_signal') else randint(1, 255)
            max_signal = kwargs.get('max_signal') if kwargs.get('max_signal') else randint(1, 255)
            speed = randint(50, 255)
            palette = randint(1, 26)
            scale = randint(50, 255)
            from_center = randint(0, 1)
            color = randint(0, 255)
            random_effect = randint(0, 1)
            data += f',{type_effect},{fade_brightness},{brightness},{adv_mode},{sound_react},{min_signal},{max_signal},{speed},{palette},{scale},{from_center},{color},{random_effect}'
        data += f',{random_num}'
        if len(date) == 0:
            date = 'now'
        self.__send_request(data, date)

    def palette(self, *date, **kwargs):
        if len(date) == 0:
            date = 'now'
        if kwargs.get('colour') or kwargs.get('color') or kwargs.get('rgb'):
            color = kwargs.get('colour') or kwargs.get('color') or kwargs.get('rgb')
            if color in COLORS_RGB:
                color, scale, brightness = hsv2chsv(*rgb2hsv(*COLORS_RGB[color]))
            elif kwargs.get('rgb'):
                color, scale, brightness = hsv2chsv(*rgb2hsv(*color))
            else:
                color, scale, brightness = 255, 255, 255
        elif kwargs.get('hex'):
            color, scale, brightness = hsv2chsv(*rgb2hsv(*hex2rgb(kwargs.get('hex').replace('#', ''))))
        elif kwargs.get('hsv'):
            color, scale, brightness = hsv2chsv(*kwargs.get('hsv'))
        elif kwargs.get('chsv'):
            color, scale, brightness = kwargs.get('chsv')
        else:
            color, scale, brightness = 255, 255, 255

        if kwargs.get('brightness'):
            brightness = kwargs.get('brightness')

        data = f'2,1,2,1,{brightness},1,1,0,255,105,2,{scale},0,{color},0,1'
        self.__send_request(data, date)

    def save_settings_json(self):
        with open(self.json_settings_path, 'w') as file:
            jdump(self.__settings_data, file)

    def load_settings_json(self):
        with open(self.json_settings_path, 'r') as file:
            self.__settings_data = jload(file)

    def __wait_sync_settings(self, timeout: int = 5):
        time_started = perf_counter()
        while True:
            if self.__is_lamp_synced:
                self.__is_lamp_synced = False
                return True
            if perf_counter() - time_started > timeout:
                return False
            sleep(0.1)

    def __lamp_request_handler(self):
        data = dict(request.args)
        type_data = data.get('type')
        if type_data is None or type_data != 'settings':
            return
        del data['type']
        for key, value in data.items():
            self.__settings_data[key] = value
        self.__is_lamp_synced = True

    def __send_request(self, *args, **kwargs):
        if isinstance(args[0], tuple):
            args = args[0]

        current_time = int(time() * 1000)
        if kwargs.get('skip') is None and (self.__enable_task_list and current_time - self.__last_request_time < 500):
            self.__task_list.append(args)
            return
        data = []
        for i in args:
            if i == 'now':
                i = self.__now_date()
            data.append(i)
        message = f'{self.key},{",".join(data)}'
        if self.__log_data_request:
            print(message)

        self.__sock.sendto(f"{message}".encode(), (self.ip, self.port))
        self.__last_request_time = int(time() * 1000)

    def __check_multi_requests(self, _time):
        if self.__count_multi_requests > 0 and _time - self.__last_request_time >= 100:
            self.__count_multi_requests -= 1
            if self.__count_multi_requests < 0:
                self.__count_multi_requests = 0
            return True
        return False

    def __task_list_processing(self):
        while True:
            current_time = int(time() * 1000)
            if len(self.__task_list) > 0 and (
                    current_time - self.__last_request_time >= 500 or self.__check_multi_requests(current_time)):
                task = self.__task_list[0]
                self.__task_list.pop(0)
                self.__send_request(task, skip=1)
            sleep(0.05)

    def __now_date(self):
        day = datetime.fromtimestamp(int(time()) + 1)
        return f'{day.isoweekday()},{day.hour},{day.minute},{day.second + 1}'

    def __start_server(self):
        app = _FlaskAppWrapper(name=self.server_name, host=self.server_host, port=self.server_port,
                               debug=self.server_debug)
        app.add_endpoint(endpoint='/', endpoint_name='', handler=self.__lamp_request_handler)
        app.run()
