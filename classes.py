# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 16:11:46 2020

@author: Jean
"""

import numpy as np
from PIL import Image
from datetime import datetime
# =============================================================================
# class handles():
#     def __init__(self):
#         self.init_time=0
#         self.test=1
#         self.disp_image=Image.open('test.png')
#         self.current_time_step=0
#         self.testval=0
# =============================================================================


from threading import Timer

class RepeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)    
            
            
from threading import Timer, Thread, Event

class PT():

    def __init__(self, t, hFunction):
        self.t = t
        self.hFunction = hFunction
        self.thread = Timer(self.t, self.handle_function)

    def handle_function(self):
        self.hFunction()
        self.thread = Timer(self.t, self.handle_function)
        self.thread.start()

    def start(self):
        self.thread.start()
        
    def cancel(self):
        self.thread.cancel()

