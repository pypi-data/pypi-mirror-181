from colorsys import rgb_to_hsv as rgb2hsv

COLORS_RGB = {
    'red': (255, 0, 0,),
    'orange': (255, 165, 0,),
    'yellow': (255, 255, 0,),
    'green': (0, 214, 120,),
    'lime': (0, 255, 0,),
    'aqua': (0, 255, 255,),
    'cyan': (0, 255, 255,),
    'blue': (0, 0, 255,),
    'navy': (0, 0, 128,),
    'purple': (255, 20, 147,),
    'pink': (255, 20, 147,),
    'black': (0, 0, 0,),
    'white': (255, 255, 255,)
}


def rgb2hex(r, g, b) -> str:
    code = f'{hex(r)}{hex(g)}{hex(b)}'.replace('0x', '')
    if len(code) < 6:
        last_num = code[-1]
        for i in range(6 - len(code)):
            code += last_num
    return code


def hex2rgb(code: str) -> tuple[int, int, int]:
    count = 0
    r, g, b = None, None, None

    len_code = len(code)
    if len_code == 0:
        return 255, 255, 255

    last_num = code[-1]
    if len_code < 6:
        for i in range(6 - len_code):
            code += last_num

    for i in code:
        count += 1
        if count % 2 != 0:
            last_num = i
        if count > 1 and count % 2 == 0:
            num = f'0x{last_num}{i}'
            if r is None:
                r = int(num, 16)
            elif g is None:
                g = int(num, 16)
            elif b is None:
                b = int(num, 16)
            else:
                break
    return r, g, b


def hsv2chsv(h, s, v) -> tuple[int, int, int]:
    if h < 1.1 and isinstance(h, float):
        h = h * 255
    else:
        h = h / 360 * 255
    if s < 1.1 and isinstance(s, float):
        s = s * 255
    if v < 1.1 and isinstance(v, float):
        v = v * 255

    return int(h), int(s), int(v)
