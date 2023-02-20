# -*- coding:UTF-8 -*-
from utils import buildOcrModel, getRandomNumber
from handler import Hanlder
from mouse import Mouse
from config import Config
import time
from typing import List, Any, Dict, Optional, Collection, Tuple

# 普通模式 
OCR_CONSTANT_MODE = 0
# 限速模式
OCR_THROTTLE_MODE = 1

class Step:
    def __init__(self):
        self.bbox = tuple()
        self.click_bbox = tuple()
        self.click_times = tuple()
        self.chars = tuple()
    def __str__(self):
        return "bbox: %s, click_bbox: %s, click_times:% s, chars: %s" % (self.bbox, self.click_bbox, self.click_times, self.chars)

def ocrflow(
    config: Config, 
    steps: Tuple[Step],
):
    ocr_model = buildOcrModel(**dict(config.items('ocr')))
    mouse = Mouse(config.getTuple('mouse', 'click_interval'), config.getTuple('mouse', 'move_time', value=float))
    handlers = []
    for step in steps:
        handler = Hanlder(ocr_model, mouse, bbox=step.bbox, click_bbox=step.click_bbox, click_times=step.click_times)
        handler.setCharacter(step.chars)
        handlers.append(handler)

    stop_interval = config.getint('exec', 'stop_interval')
    rest_time = config.getint('exec', 'rest_time')

    def constantExec():
        while True:
            time.sleep(stop_interval / 1000)
            handler_len = len(handlers)
            for i in range(handler_len):
                if handlers[i].handle() is True:
                    break

    def throttleExec():
        n = 0
        while True:
            time.sleep(stop_interval/ 1000)
            handler_len = len(handlers)
            flag = True
            for i in range(handler_len):
                if handlers[i].handle() is True:
                    break
                if i == handler_len - 1:
                    n += 1
                    flag = False
                    if n == 30:
                        print("连续超过30次未检测到有效信息，休息%d秒" % rest_time)
                        time.sleep(rest_time)
                        n = 0
            if flag is True:
                n = 0

    exec_mode = config.getint('exec', 'ocr_mode')
    if exec_mode == OCR_CONSTANT_MODE:
        constantExec()
    elif exec_mode == OCR_THROTTLE_MODE:
        throttleExec()
    else:
        raise TypeError

def timeflow(config: Config):
    mouse = Mouse(config.getTuple('mouse', 'click_interval'), config.getTuple('mouse', 'move_time', value=float))
    active = config.get('active', 'name')
    steps = config.getTuple(active, 'steps', value=str)
    click_boxes = []
    click_times = []
    time_intervals = []
    for step in steps:
        box = config.getTuple(active, step + '_click_bbox')
        click_time = config.getTuple(active, step + '_click_times')
        click_boxes.append(box)
        click_times.append(click_time)
        time_intervals.append(config.getint(active, step + '_interval'))
    while True:
        for i in range(len(click_boxes)):
            click_x1, click_y1, click_x2, click_y2 = click_boxes[i]
            target_x = getRandomNumber(click_x1, click_x2)
            target_y = getRandomNumber(click_y1, click_y2)
            click_time = click_times[i]
            if len(click_times) > 1:
                click_time = getRandomNumber(click_time[0], click_time[1])
            else:
                click_time = click_time[0]
            print("time: %s, target_x: %d, target_y: %d, click_times: %d" 
                % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), target_x, target_y, click_time))
            mouse.move(target_x, target_y)
            mouse.click(target_x, target_y, n=click_time)
            time.sleep(time_intervals[i] / 1000)
