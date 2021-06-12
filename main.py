import os
os.environ['CNOCR_HOME'] = './cnocr'
os.environ['CNSTD_HOME'] = './cnstd'
os.environ['MXNET_CUDNN_AUTOTUNE_DEFAULT'] = '0'
from utils import buildOcrModel, buildStdModel
from handler import Hanlder
from mouse import Mouse
from config import Config
import time
import sys

CONSTANT_MODE = 0
THROTTLE_MODE = 1
config_file = 'config.ini'
config_encoding = 'utf-8'

def main():
    config = Config()
    global config_file
    if len(sys.argv) > 1:
        config_file = sys.argv[1]
    global config_encoding
    if len(sys.argv) > 2:
        config_encoding = sys.argv[2]
    config.read(config_file, encoding=config_encoding)
    
    std_model = buildStdModel(**dict(config.items('std')))
    ocr_model = buildOcrModel(**dict(config.items('ocr')))
    mouse = Mouse(config.getTuple('mouse', 'click_interval'), config.getTuple('mouse', 'move_time', value=float))

    handlers = []
    active = config.get('active', 'name')
    steps = config.getTuple('active', active, value=str)
    for step in steps:
        handler = Hanlder(std_model, ocr_model, mouse, bbox=config.getTuple(active, step + '_bbox'),
            click_bbox=config.getTuple(active, step + '_click_bbox'), click_times=config.getTuple(active, step + '_click_times'))
        handler.setCharacter(config.getTuple(active, step + '_char', value=str))
        handlers.append(handler)

    stop_interval = config.getint('exec', 'stop_interval')
    rest_time = config.getint('exec', 'rest_time')
    def constantExec():
        while True:
            time.sleep(stop_interval)
            handler_len = len(handlers)
            for i in range(handler_len):
                if handlers[i].handle() is True:
                    break

    def throttleExec():
        n = 0
        while True:
            time.sleep(stop_interval)
            handler_len = len(handlers)
            flag = True
            for i in range(handler_len):
                if handlers[i].handle() is True:
                    break
                if i == handler_len - 1:
                    n += 1
                    flag = False
                    if n == 10:
                        print("连续超过10次未检测到有效信息，休息%d秒" % rest_time)
                        time.sleep(rest_time)
                        n = 0
            if flag is True:
                n = 0

    exec_mode = config.getint('exec', 'mode')
    if exec_mode == CONSTANT_MODE:
        constantExec()
    elif exec_mode == THROTTLE_MODE:
        throttleExec()
    else:
        raise TypeError

if __name__ == "__main__":
    main()