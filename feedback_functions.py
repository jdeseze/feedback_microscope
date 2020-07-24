# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 15:58:48 2020

@author: Jean
"""
import streamlit as st
import time
import classes as cl
from pycromanager import Bridge
from PIL import Image
import numpy as np
import types
from datetime import datetime
import updated_variables as uv
import pandas as pd


@st.cache    
def start_fcn(handles):
    #timer=time.time
    #init_time=int(timer)
    handles.testval=time.perf_counter()-handles.init_time
    return handles

@st.cache(allow_output_mutation=True)
def init_fcn(rand):
    #handles=h.handles()
    path=uv.__file__
    with open(path,"w") as fp:
        fp.writelines(['a=3 \n','b=12 \n'])
    handles=types.SimpleNamespace()
    handles.init_time=0
    handles.test=1
    handles.disp_image=Image.open('test.png')
    handles.current_time_step=0
    handles.testval=0
    core=Bridge().get_core()
    handles.core=core
    handles.testval=0
    handles.num_pos=2
    handles.all_pos='./all_pos.pkl'
    all_pos=pd.DataFrame(np.zeros([1,3]),columns=['x', 'y', 'z'])
    all_pos.to_pickle('./all_pos.pkl')
    handles.current_step=0
    handles.num_steps=0
    handles.num_WL=1
    handles.current_WL=1
    handles.session_id=np.random.rand()
    return handles

#@st.cache
def start_acq(handles):
    handles.acq=cl.PT(1,printer)
    handles.acq.start()
    #return acq

def stop_acq(handles):
    handles.acq.cancel()

def printer():
    tempo = datetime.today()
    h,m,s = tempo.hour, tempo.minute, tempo.second
    time=(f"{h}:{m}:{s}")
    path=uv.__file__
    with open(path,"w") as fp:
        fp.writelines(['a=5 \n','b="'+time+'" \n'])
    #return st.write((f"{h}:{m}:{s}"))

#@st.cache
def acq_fcn(handles):
    handles.core.snap_image()
    tagged_img=handles.core.get_tagged_image()
    pixvals=np.reshape(tagged_img.pix,newshape=[tagged_img.tags['Height'], tagged_img.tags['Width']])
    pixvals = ((pixvals - pixvals.min()) / (pixvals.max()-pixvals.min())) 
    handles.disp_image=pixvals
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