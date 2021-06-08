from pymouse import PyMouse
from utils import getRandomNumber, generateBezierCurve
import time
import numpy as np
import math

class Mouse(PyMouse):

    TICKER_INTERVAL = 10 # 10ms
    interval = tuple()
    move_time = tuple()

    def __init__(self, interval, move_time, *args, **kwargs):
        assert type(interval) in [list, tuple] and len(interval) > 0
        assert type(move_time) in [list, tuple] and len(move_time) == 2
        super().__init__(*args, **kwargs)
        self.interval = interval
        self.move_time = move_time


    def move(self, x, y):
        start_x, start_y = self.position()
        if x == start_x and y == start_y:
            return
        start_x, start_y = self.position()
        min_x, max_x = (start_x, x) if start_x < x else (x, start_x)
        min_y, max_y = (start_y, y) if start_y < y else (y, start_y)
        control_x = getRandomNumber(min_x, max_x)
        control_y = getRandomNumber(min_y, max_y)
        generator = generateBezierCurve(*np.array([[start_x, start_y], [control_x, control_y], [x, y]]))
        delta_x, delta_y = max_x - min_x + 1, max_y - min_y + 1
        step = delta_x if delta_x > delta_y else delta_y
        points = np.array([generator(t) for t in np.linspace(0, 1, step)])

        move_time = getRandomNumber(self.move_time[0], self.move_time[1], float=True) * 1000
        interval = move_time / step
        interval = interval if interval > self.TICKER_INTERVAL  else self.TICKER_INTERVAL
        task_times = int(move_time / interval)
        assert task_times > 0
        task_per_time = math.ceil(step / task_times)
        counter = 0
        for i in range(task_times):
            flag = False
            for j in range(task_per_time):
                if counter >= step:
                    flag = True
                    break
                super().move(int(points[counter][0]), int(points[counter][1]))
                counter += 1
            time.sleep(interval / 1000)
            if flag is True:
                break

    def click(self, x, y, button=1, n=1):
        for i in range(n):
            super().click(x, y, button, 1)
            interval = self.interval[0]
            if len(self.interval) > 1:
                interval = getRandomNumber(self.interval[0], self.interval[1])
            time.sleep(interval / 1000)


        



        
        
