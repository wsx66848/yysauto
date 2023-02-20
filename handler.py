from utils import getRandomNumber, getScreenShots, isListofType
from mouse import Mouse
from cnocr import CnOcr
import numpy as np
import time

class Hanlder:

    character = list()

    def __init__(
        self, 
        ocr_model: CnOcr, 
        mouse: Mouse, 
        bbox, 
        click_bbox, 
        click_times
    ):
        assert type(bbox) is tuple and len(bbox) == 4
        assert type(click_bbox) is tuple and len(click_bbox) == 4
        assert type(click_times) is tuple and len(click_times) == 2
        self._ocr_model = ocr_model
        self._bbox = bbox
        self._click_bbox = click_bbox
        self._click_times = click_times
        self._mouse = mouse

    def setCharacter(self, character):
        if type(character) in [list, tuple] and isListofType(character, str):
            self.character = character
        elif type(character) is str:
            self.character.append(character) 
        else:
            raise TypeError
    
    def handle(self):
        ocr_res = self._ocr_model.ocr_for_single_line(getScreenShots(*self._bbox))
        if 'text' not in ocr_res:
            return False
        #import pdb;pdb.set_trace() 
        if self._checkCharacter(ocr_res.get('text')):
            click_x1, click_y1, click_x2, click_y2 = self._click_bbox
            target_x = getRandomNumber(click_x1, click_x2)
            target_y = getRandomNumber(click_y1, click_y2)
            click_times = getRandomNumber(self._click_times[0], self._click_times[1])
            print("time: %s, target_x: %d, target_y: %d, click_times: %d" 
                % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), target_x, target_y, click_times))
            self._mouse.move(target_x, target_y)
            self._mouse.click(target_x, target_y, n=click_times)
            return True
        return False

    def _checkCharacter(self, strline):
        assert type(strline) is str
        for charc in self.character:
            if charc in strline:
                return True
        return False


        


    