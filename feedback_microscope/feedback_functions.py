# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 15:58:48 2020

@author: Jean
"""
import streamlit as st
import time
import classes as cl
import pycromanager as pm
from PIL import Image
import numpy as np
import types
from datetime import datetime
import updated_variables as uv
import pandas as pd
import tifffile
import threading



@st.cache(allow_output_mutation=True)
def init_fcn(rand):
    #handles=h.handles()
    path=uv.__file__
    with open(path,"w") as fp:
        fp.writelines(['session_id='+str(rand)+' \n','a=2 \n','timer=12 \n','current_step=0 \n'])
    handles=types.SimpleNamespace()
    handles.init_time=0
    handles.test=1
    handles.disp_image=Image.open('test.png')
    handles.current_step=0
    handles.testval=0
    core=pm.Bridge().get_core()
    handles.core=core
    handles.testval=0
    handles.num_pos=2
    handles.all_pos='./all_pos.pkl'
    all_pos=pd.DataFrame(np.zeros([1,3]),columns=['x', 'y', 'z'])
    all_pos.to_pickle('./all_pos.pkl')
    handles.current_step=0
    handles.nb_steps=5
    handles.num_WL=1
    handles.current_WL=1
    handles.go_on=True
    handles.time_step=1
    return handles

#@st.cache
def start_acq(handles):
    #handles.acq=cl.PT(1,printer(handles.current_step))
    #handles.acq.start()
    #return acq
    #printer(handles.current_step)
    handles.go_on=True
    acq_fcn(handles)
        
def stop_acq(handles):
    handles.go_on=False


def printer(current_step):
    if current_step<10:
        threading.Timer(1.0, printer,[current_step+1]).start()
        tempo = datetime.today()
        h,m,s = tempo.hour, tempo.minute, tempo.second
        time=(f"{h}:{m}:{s}")
        path=uv.__file__
        with open(path,"w") as fp:
            fp.writelines(['session_id='+str(uv.session_id)+' \n','a=5 \n','timer="'+time+'" \n','current_step='+str(current_step)+' \n'])

    
        #return st.write((f"{h}:{m}:{s}"))

#@st.cache
def snap_fcn(handles):
    handles.core.snap_image()
    tagged_img=handles.core.get_tagged_image()
    pixvals=np.reshape(tagged_img.pix,newshape=[tagged_img.tags['Height'], tagged_img.tags['Width']])
    pixvals = ((pixvals - pixvals.min()) / (pixvals.max()-pixvals.min())) 
    return pixvals
    #time.sleep(1)
    #return handles
    
@st.cache
def get_table(string,num_pos,rand):
    return pd.read_pickle(string)


def add_pos(core,string):
    current_pos=pd.DataFrame(np.array([[core.get_x_position(),core.get_y_position(),core.get_position()]]),columns=['x', 'y', 'z'])
    all_pos=pd.read_pickle(string)
    all_pos=all_pos.append(current_pos,ignore_index=True)
    all_pos.to_pickle(string)
    
def acq_fcn(handles):
    if handles.current_step<handles.nb_steps and handles.go_on==True:
        handles.current_step=handles.current_step+1
        threading.Timer(handles.time_step, acq_fcn,[handles]).start()
        handles.core.snap_image()
        tagged_img=handles.core.get_tagged_image()
        pixvals=np.reshape(tagged_img.pix,newshape=[tagged_img.tags['Height'], tagged_img.tags['Width']])
        tifffile.imwrite('./test.tif',pixvals,photometric='minisblack',append=True)
        handles.disp_image = ((pixvals - pixvals.min()) / (pixvals.max()-pixvals.min())) 
        tempo = datetime.today()
        h,m,s = tempo.hour, tempo.minute, tempo.second
        time=(f"{h}:{m}:{s}")
        path=uv.__file__
        with open(path,"w") as fp:
            fp.writelines(['session_id='+str(uv.session_id)+' \n','a=5 \n','timer="'+time+'" \n','current_step='+str(handles.current_step-1)+' \n'])

