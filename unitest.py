# -*- coding:UTF-8 -*-
import os
os.environ['CNOCR_HOME'] = './cnocr'
os.environ['CNSTD_HOME'] = './cnstd'
from cnstd import CnStd
from cnocr import CnOcr
from cv2 import imshow, waitKey
import numpy as np
import PIL.ImageGrab as ImageGrab
from pymouse import PyMouse

avaliable_std_models = ['mobilenetv3', 'resnet50_v1b']
avaliable_ocr_models = ['conv-lite-fc', 'densenet-lite-gru', 'densenet-lite-fc', 'densenet-lite-s-gru', 'densenet-lite-s-fc']
std = CnStd(model_name=avaliable_std_models[0])
cn_ocr = CnOcr(model_name=avaliable_ocr_models[1])

#img_fp = './jiesuan2.png'
# box_info_list = std.detect(img_fp, max_size=1500, pse_min_area=500)
img  = ImageGrab.grab(bbox=(573, 760, 851, 862))
img_fp = np.array(img.getdata(), np.uint8).reshape(img.size[1], img.size[0], 3)
imshow("grabed img", img_fp)
waitKey()
box_info_list = std.detect(img_fp)

mouse = PyMouse()

for box_info in box_info_list:
    cropped_img = box_info['cropped_img']
    imshow("img", np.array(cropped_img))
    waitKey()
    ocr_res = cn_ocr.ocr_for_single_line(cropped_img)
    ocr_str = ''.join(ocr_res)
    print("ocr result: %s\n" % ocr_str)
    if '点击' in ocr_str or '屏幕' in ocr_str or '继续' in ocr_str:
        import pdb;pdb.set_trace()
