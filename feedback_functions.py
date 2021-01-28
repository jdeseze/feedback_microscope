# -*- coding: utf-8 -*-
"""
Created on Tue Oct 13 15:02:25 2020

@author: Jean
"""

import numpy as np
import time

from PIL import Image
import copy
import pandas as pd
import threading
import streamlit.report_thread as report_thread
import random
import sys
from threading import Thread
import time
import pycromanager as pm
import tifffile as tif



def rep_acq(state):
    if state.currentstep<state.nbsteps:
        state.currentstep+=1
        t=threading.Timer(state.timestep,rep_acq,[state])
        t.start()
        
        all_pos=pd.read_pickle(state.all_pos)
        for pos in range(all_pos.x.size):
            x=all_pos.x[pos]
            y=all_pos.y[pos]
            go_to_pos(state,[x,y])
            acquire_save(state)
            
            
def go_to_pos(state,coord):
    if state.soft:
        pass
    else:
        bridge=pm.Bridge()
        core=bridge.get_core()  
        core.set_xy_position(coord[0],coord[1])
        
def acquire(state):
    if state.soft:
        pixvals=state.mm.RunJournal('C:/MM/app/mmproc/journals/s.JNL')
    else:
        bridge=pm.Bridge()
        core=bridge.get_core()
        core.snap_image()
        tagged_img=core.get_tagged_image()
    pixvals=np.reshape(tagged_img.pix,newshape=[tagged_img.tags['Height'], tagged_img.tags['Width']])
    contrasted = ((pixvals - pixvals.min()) / (pixvals.max()-pixvals.min())) 
    state.disp_image=contrasted
    state.img_to_save=pixvals
    state.sync()
    
def acquire_save(state):
    if state.soft:
        pass
    else:
        bridge=pm.Bridge()
        core=bridge.get_core()
        core.snap_image()
        tagged_img=core.get_tagged_image()
    pixvals=np.reshape(tagged_img.pix,newshape=[tagged_img.tags['Height'], tagged_img.tags['Width']])
    norm = ((pixvals - pixvals.min()) / (pixvals.max()-pixvals.min())) 
    state.disp_image=norm
    #with Image.open('test.tif') as temp_img:
    tif.imwrite('test.tif',pixvals,append=True)
    state.sync()
    
def add_pos(state):
    bridge=pm.Bridge()
    core=bridge.get_core()    
    current_pos=pd.DataFrame(np.array([[core.get_x_position(),core.get_y_position(),core.get_position()]]),columns=['x', 'y', 'z'])
    all_pos=pd.read_pickle(state.all_pos)
    all_pos=all_pos.append(current_pos,ignore_index=True)
    all_pos.to_pickle(state.all_pos)