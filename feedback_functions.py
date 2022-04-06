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
            z=all_pos.z[pos]
            set_pos(state,[x,y,z])
            for chan in state.channels:
                set_wl(state,chan)
                acquire_save(state,state.name_exp+'_'+str(pos)+'_'+chan+'.tif')
                #there we should analyse and change the positions
                
            
            
def set_pos(state,coord):
    if state.soft:
        pass
    else:
        bridge=pm.Bridge()
        core=bridge.get_core()  
        core.set_xy_position(coord[0],coord[1])
        core.set_position(coord[2])
        
def set_wl(state,chan):
    if state.soft:
        pass
    else:
        bridge=pm.Bridge()
        core=bridge.get_core()  
        core.set_config('Channel',chan)    
        
def acquire(state):
    if state.soft:
        state.mm.RunJournal('C:/MM/app/mmproc/journals/s.JNL')
        pixvals=np.array(Image.open('C:/TEMP/tmp.tif'))
    else:
        bridge=pm.Bridge()
        core=bridge.get_core()
        core.snap_image()
        tagged_img=core.get_tagged_image()
        pixvals=np.reshape(tagged_img.pix,newshape=[tagged_img.tags['Height'], tagged_img.tags['Width']])
    contrasted = ((pixvals - pixvals.min()) / (pixvals.max()-pixvals.min())) 
    state.disp_image=contrasted
    state.img_to_save=pixvals
    
def acquire_save(state,name):
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
    tif.imwrite(name,pixvals,append=True)
    
def add_pos(state):
    bridge=pm.Bridge()
    core=bridge.get_core()    
    current_pos=pd.DataFrame(np.array([[core.get_x_position(),core.get_y_position(),core.get_position()]]),columns=['x', 'y', 'z'])
    all_pos=pd.read_pickle(state.all_pos)
    all_pos=all_pos.append(current_pos,ignore_index=True)
    all_pos.to_pickle(state.all_pos)