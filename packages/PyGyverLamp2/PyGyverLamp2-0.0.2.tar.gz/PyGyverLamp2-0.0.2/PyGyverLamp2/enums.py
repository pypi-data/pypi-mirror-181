from enum import Enum


class TypeControls(Enum):
    Control = '0'
    Settings = '1'
    Effects = '2'
    Dawn = '3'
    Palette = '4'

    Sync = '20'
    CountSimultaneousRequests = '21'


class Codes(Enum):

    turn_of = '0,0'
    turn_on = '0,1'
    min_brightness = '0,2'
    max_brightness = '0,3'
    back_mode = '0,4'
    next_mode = '0,5'

    sync_settings = '20,1'
    set_auto_sync_settings = '20,2'
