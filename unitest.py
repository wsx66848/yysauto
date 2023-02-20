# -*- coding:UTF-8 -*-
import os
os.environ['CNOCR_HOME'] = './cnocr'
os.environ['CNSTD_HOME'] = './cnstd'
from cnocr import CnOcr
import numpy as np
from PIL.ImageGrab import grab
from typing import List, Any, Dict, Optional, Collection, Tuple
import sys

cn_ocr = CnOcr()
bbox = (100, 100, 200, 200)
filename = 'test_images/jiesuan.PNG'

def grabImage(
    bbox: Tuple[int, int, int, int],
):
    img  = grab(bbox=bbox).convert("RGB")
    print("img.size :", img.size)
    img.show()
    ocr_res = cn_ocr.ocr_for_single_line(np.asarray(img))
    print("ocr_res: ", ocr_res)

def testFile(
    filename: str
):
    ocr_res = cn_ocr.ocr_for_single_line(filename)
    print("ocr_res: ", ocr_res)
    


if __name__ == "__main__":
    mod = 'grab'
    if len(sys.argv) > 1:
        mod = sys.argv[1]
    if mod == 'grab':
        grabImage(bbox)
    if mod == 'file':
        testFile(filename)