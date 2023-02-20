# -*- coding:UTF-8 -*-
import os
os.environ['CNOCR_HOME'] = './cnocr'
os.environ['CNSTD_HOME'] = './cnstd'
from config import Config
import sys
import win32api, win32gui, win32print, win32con
from flow import ocrflow, timeflow, Step

OCR_MODE = 0
TIME_MODE = 1
config_file = 'config.ini'
config_encoding = 'utf-8'

if __name__ == "__main__":
    #加载配置
    config = Config()
    if len(sys.argv) > 1:
        config_file = sys.argv[1]
    if len(sys.argv) > 2:
        config_encoding = sys.argv[2]
    config.read(config_file, encoding=config_encoding)
    # mouse的位置和win32gui的一致，与ImageGrab不同，因此先计算转换因子
    hDC = win32gui.GetDC(0)
    screen_x = win32print.GetDeviceCaps(hDC, win32con.DESKTOPHORZRES)
    screen_y = win32print.GetDeviceCaps(hDC, win32con.DESKTOPVERTRES)
    print("screen size: (%d, %d)" % (screen_x, screen_y))
    mouse_x = win32api.GetSystemMetrics(0)
    mouse_y = win32api.GetSystemMetrics(1)
    print("mouse size: (%d, %d)" % (mouse_x, mouse_y))
    factor_x = screen_x / mouse_x
    factor_y = screen_y / mouse_y
    print("factor_x: %.2f, factor_y: %.2f" % (factor_x, factor_y))
    # 初始化steps
    # 根据窗体位置计算真正的step
    window_rect = win32gui.GetWindowRect(win32gui.WindowFromPoint(win32gui.GetCursorPos()))
    window_x = window_rect[0] + window_rect[2]
    window_y = window_rect[1] + window_rect[3]
    activeSteps = []
    active = config.get('active', 'name')
    steps = config.getTuple(active, 'steps', value=str)
    for step in steps:
        activeStep = Step()
        bbox_factor = config.getTuple(active, step + '_bbox', value=float)
        activeStep.bbox = (int(window_x * bbox_factor[0] * factor_x), int(window_y * bbox_factor[1] * factor_y), int(window_x * bbox_factor[2] * factor_x), int(window_y * bbox_factor[3] * factor_y))
        click_bbox_factor = config.getTuple(active, step + '_click_bbox', value=float)
        activeStep.click_bbox = (int(window_x * click_bbox_factor[0]), int(window_y * click_bbox_factor[1]), int(window_x * click_bbox_factor[2]), int(window_y * click_bbox_factor[3]))
        activeStep.click_times = config.getTuple(active, step + '_click_times')
        activeStep.chars = config.getTuple(active, step + '_char', value=str)
        print("name: %s, step: %s" % (step, activeStep))
        activeSteps.append(activeStep)

    mode = config.getint("exec", "mode")
    print(("mode: %d, start running..." % mode))
    if mode == OCR_MODE:
        ocrflow(config, activeSteps)
    if mode == TIME_MODE:
        timeflow(config)