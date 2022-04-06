# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 16:33:42 2020

@author: Jean
"""

import streamlit as st
import numpy as np
from PIL import Image
import pandas as pd
import threading
import feedback_functions as ff
import time
#pip install pythonnet !!!!
import clr
import pycromanager as pm


st.set_page_config(page_title="Feedback routine", page_icon=":microscope:",layout="wide")

st.session_state['nbsteps']=0
st.session_state['timestep']=''
st.session_state['current_time_step']=1
st.session_state['name_exp']=''
st.session_state['comments']=''
st.session_state['soft']=False
st.session_state['channels']=['FITC']
st.session_state.show_image=False

st.session_state.soft=st.sidebar.checkbox('Use Metamorph')

if st.session_state.soft:
    clr.AddReference('C:\dmd\Interop.MMAppLib.dll')
    import MMAppLib
    st.session_state.mm=MMAppLib.UserCallClass()
else:
    bridge=pm.Bridge()
    core=bridge.get_core()  
    #state[core]=core

    
st.title("Test feedback acquisition function")

st.session_state['all_pos']=False

if not st.session_state.all_pos:
    st.session_state.all_pos='./all_pos.pkl'
    #creation of a dataframe 
    all_pos=pd.DataFrame(np.zeros([1,3]),columns=['x', 'y', 'z'])
    all_pos.to_pickle(st.session_state.all_pos)


c1,c2=st.columns(2)

with c1:
    st.write('---')
    st.write("Current time step : ",st.session_state.current_time_step or 0)
    st.write("Number of steps:", st.session_state.nbsteps)
    st.write("Time step:", st.session_state.timestep)
    st.write("Channels:", st.session_state.channels)

    if st.button('Initialize again'):
        st.session_state.clear()
    if st.button("Start acq"):
        st.session_state.currentstep=0
        ff.rep_acq(st.session_state)
    if st.button("Add position"):
        ff.add_pos(st.session_state)
    
    st.write(pd.read_pickle(st.session_state.all_pos))

with c2:
    if st.button("Acquire"):
        ff.acquire(st.session_state);
        st.session_state.show_image=True
    if st.session_state.show_image:
        st.image(st.session_state.disp_image,use_column_width=True,output_format='PNG')
        #st.session_state.show_image=False
    #st.write(st.session_state.error)

# in the sidebar, all the parameters are choosen
st.sidebar.title("Acquisition parameters")
options = ["Hello", "World", "Goodbye"]

time_settings=st.sidebar.expander("Time settings",expanded=False)
with time_settings:
    st.session_state.nbsteps=st.number_input('Number of steps',0,10000,st.session_state.nbsteps or 0)
    st.session_state.timestep=st.number_input('Time step (in s)',0,100000,st.session_state.timestep or 0)  

exp_settings=st.sidebar.expander("Experiment settings")
with exp_settings:
    st.session_state.name_exp = st.text_input("Name of the experiment", st.session_state.name_exp or "")
    st.session_state.comments = st.text_input("Comments", st.session_state.comments or "")

ill_settings=st.sidebar.expander("Illumination settings")
with ill_settings:
    #get setting of different channels
    options=["FITC","DAPI","Cy5","GFP","Rhodamine"]
    st.session_state.channels=st.multiselect("Select channels",options,st.session_state.channels)




