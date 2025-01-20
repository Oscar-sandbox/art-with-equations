# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 23:15:04 2025
@author: oscar
"""
import time
from worm_funcs import rgb
from multiprocessing import Pool
import numpy as np
import cv2

if __name__ == '__main__':    
    sy, sx = 1200, 2000
    grid = [(n+1,m+1) for n in range(sy) for m in range(sx)]

    start = time.time()
    with Pool(processes=16) as pool:
        records = pool.starmap(rgb, grid)   
    end = time.time()
    print(end-start)
    
    img = np.array(records, dtype=np.uint8).reshape(sy, sx, 3)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    cv2.imwrite('img.png', img)