from utils import getRandomNumber, getScreenShots, isListofType
from mouse import Mouse

class Hanlder:

    character = list()

    def __init__(self, std_model, ocr_model, mouse, bbox, click_bbox, click_times):
        assert type(bbox) in [tuple, int] and len(bbox) == 4
        assert type(click_bbox) in [tuple, int] and len(click_bbox) == 4
        assert type(click_times) in [tuple, int] and len(click_times) > 0
        self._std_model = std_model
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
        img_fp = getScreenShots(*self._bbox)
        box_info_list = self._std_model.detect(img_fp)
        for box_info in box_info_list:
            cropped_img = box_info['cropped_img']
            ocr_res = self._ocr_model.ocr_for_single_line(cropped_img)
            ocr_str = ''.join(ocr_res)
            if self._checkCharacter(ocr_str):
                click_x1, click_y1, click_x2, click_y2 = self._click_bbox
                target_x = getRandomNumber(click_x1, click_x2)
                target_y = getRandomNumber(click_y1, click_y2)
                click_times = self._click_times[0]
                if len(self._click_times) > 1:
                    click_times = getRandomNumber(self._click_times[0], self._click_times[1])
                print("target_x: %d, target_y: %d, click_times: %d" % (target_x, target_y, click_times))
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


        


    