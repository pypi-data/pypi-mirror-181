from PyGyverLamp2 import *

lamp = Lamp(key='GL', ip='192.168.1.237', port=61197, group_id=1, log_data_request=True, enable_task_list=True)
# lamp.start_server(wait_after_started=True)
# if not lamp.sync_settings(auto_sync=True, wait_sync=True):
#     print('Error sync to lamp')
#     exit(0)
# print('Lamp is synced')
# lamp.settings(max_brightness=255, min_brightness=50, brightness=255, matrix_orientation=1, maximum_current=40)
# while True:
#     lamp.random_effects(count=1, adv_mode=1, min_signal=0, max_signal=0, min_brightness=255, max_brightness=255)
#     sleep(10)

lamp.max_brightness()