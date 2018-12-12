# -*- coding: utf-8 -*-

# -----------------------------------------------------------------------------
import time
import datetime
import pandas as pd
from math import floor,ceil
import argparse

from pynvml import (nvmlInit,
                     nvmlDeviceGetCount, 
                     nvmlDeviceGetHandleByIndex, 
                     nvmlDeviceGetUtilizationRates,
                     nvmlDeviceGetName)

def gpu_info():
    "Returns a tuple of (GPU ID, GPU Description, GPU % Utilization)"
    nvmlInit()
    deviceCount = nvmlDeviceGetCount()
    info = []
    for i in range(0, deviceCount): 
        handle = nvmlDeviceGetHandleByIndex(i) 
        util = nvmlDeviceGetUtilizationRates(handle)
        desc = nvmlDeviceGetName(handle) 
        info.append((i, desc, util.gpu)) #['GPU %i - %s' % (i, desc)] = util.gpu
    return info

# -----------------------------------------------------------------------------

__all__ = ['plot']

# -----------------------------------------------------------------------------

def plot(series, cfg={}):
    #print(cfg)
    minimum = cfg['minimum'] if 'minimum' in cfg else min(series)
    maximum = cfg['maximum'] if 'maximum' in cfg else max(series)
    #print(minimum,maximum)

    interval = abs(float(maximum) - float(minimum))
    offset = cfg['offset'] if 'offset' in cfg else 3
    padding = cfg['padding'] if 'padding' in cfg else '           '
    height = cfg['height'] if 'height' in cfg else interval
    ratio = height / interval
    min2 = floor(float(minimum) * ratio)
    max2 = ceil(float(maximum) * ratio)

    intmin2 = int(min2)
    intmax2 = int(max2)

    rows = abs(intmax2 - intmin2)
    width = len(series) + offset
    placeholder = cfg['format'] if 'format' in cfg else '{:8.2f} '

    result = [[' '] * width for i in range(rows + 1)]

    # axis and labels
    for y in range(intmin2, intmax2 + 1):
        label = placeholder.format(float(maximum) - ((y - intmin2) * interval / rows))
        result[y - intmin2][max(offset - len(label), 0)] = label
        result[y - intmin2][offset - 1] = '┼' if y == 0 else '┤'

    y0 = int(series[0] * ratio - min2)
    result[rows - y0][offset - 1] = '┼' # first value

    for x in range(0, len(series) - 1): # plot the line
        y0 = int(round(series[x + 0] * ratio) - intmin2)
        y1 = int(round(series[x + 1] * ratio) - intmin2)
        if y0 == y1:
            result[rows - y0][x + offset] = '─'
        else:
            result[rows - y1][x + offset] = '╰' if y0 > y1 else '╭'
            result[rows - y0][x + offset] = '╮' if y0 > y1 else '╯'
            start = min(y0, y1) + 1
            end = max(y0, y1)
            for y in range(start, end):
                result[rows - y][x + offset] = '│'

    return '\n'.join([''.join(row) for row in result])

parser = argparse.ArgumentParser(description='nvidia-gpu usage plot')
parser.add_argument('-g','--gpus',type=str)
args = parser.parse_args()

if args.gpus:
    gpu_idx = args.gpus.split(',')

utils = []

config = {
    'minimum':0,
    'maximum':100,
    'height':10
}

columns = 70

while True:
    try:
        dt = datetime.datetime.now()
        util = gpu_info()
        utils.append([dt] + [x[2] for x in util])
        if len(utils) > columns:
            utils.pop(0)
        # Don't plot anything on the first pass
        if len(utils) == 1:
            continue
        df = pd.DataFrame(utils, columns=['dt'] + 
                          ['GPU %i - %s' % (x[0], x[1].decode()) for x in util]).set_index('dt')
        
        gpus = df.columns
        n_rows = 0
        for i,gpu in enumerate(gpus):
            if args.gpus:
                if str(i) in gpu_idx:
                    print(gpu)
                    graph = plot(df[gpu].values, config)
                    print(graph)
                    n_rows += len(graph.splitlines()) + 1
            else:
                print(gpu)
                graph = plot(df[gpu].values, config)
                print(graph)
                n_rows += len(graph.splitlines()) + 1
        print("\u001B[%dA" % n_rows, end="", flush=True)
        time.sleep(1)

    except KeyboardInterrupt:
        break
