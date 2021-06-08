import time
import random
import numpy as np
import PIL.ImageGrab as screenGrab
from cnstd import CnStd
from cnocr import CnOcr


def getRandomNumber(min, max, float=False):
    time.sleep(0.01)
    random.seed(time.time())
    if float is True:
        return random.uniform(min, max)
    return random.randint(min, max)


def getScreenShots(x1, y1, x2, y2):
    img  = screenGrab.grab(bbox=(x1, y1, x2, y2))
    return np.array(img.getdata(), np.uint8).reshape(img.size[1], img.size[0], 3)

def buildStdModel(model_name, **kwargs):
    return CnStd(model_name=model_name, **kwargs)

def buildOcrModel(model_name, **kwargs):
    return CnOcr(model_name=model_name, **kwargs)

def isListofType(container, unitype=str):
    if type(container) not in (list, tuple):
        return False
    for item in container:
        if type(item) is not unitype:
            return False
    return True

def generateBezierCurve(P0, P1, P2):
    return lambda t: (1 - t)**2 * P0 + 2 * t * (1 - t) * P1 + t**2 * P2
    
