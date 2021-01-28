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
from SessionState import _get_state
import feedback_functions as ff
import time


def main():
    st.set_page_config(page_title="Feedback routine", page_icon=":microscope:",layout="wide")
    
    state = _get_state()
    
    state.soft=st.sidebar.checkbox('Use Metamorph')
    
    st.title("Test feedback acquisition function")
    
    if not state.all_pos:
        state.all_pos='./all_pos.pkl'
        all_pos=pd.DataFrame(np.zeros([1,3]),columns=['x', 'y', 'z'])
        all_pos.to_pickle(state.all_pos)

    
    c1,c2=st.beta_columns(2)
    
    with c1:
        st.write('---')
        st.write("Current time step : ",state.current_time_step or 0)
        st.write("Number of steps:", state.nbsteps)
        st.write("Time step:", state.timestep)
        st.write("Channels:", state.channels)

        if st.button('Initialize again'):
            state.clear()
        if st.button("Start acq"):
            state.currentstep=0
            ff.rep_acq(state)
        if st.button("Add position"):
            ff.add_pos(state)
        
        st.write(pd.read_pickle(state.all_pos))
    
    with c2:
        if st.button("Acquire"):
            ff.acquire(state);
            state.show_image=True
        if state.show_image:
            st.image(state.disp_image,use_column_width=True,output_format='PNG')
            #state.show_image=False
        st.write(state.error)

        
    # in the sidebar, all the parameters are choosen
    st.sidebar.title("Acquisition parameters")
    options = ["Hello", "World", "Goodbye"]
    
    time_settings=st.sidebar.beta_expander("Time settings",expanded=False)
    with time_settings:
        state.nbsteps=st.number_input('Number of steps',0,10000,state.nbsteps or 0)
        state.timestep=st.number_input('Time step (in s)',0,100000,state.timestep or 0)  
    
    exp_settings=st.sidebar.beta_expander("Experiment settings")
    with exp_settings:
        state.name_exp = st.text_input("Name of the experiment", state.name_exp or "")
        state.comments = st.text_input("Comments", state.comments or "")
    
    ill_settings=st.sidebar.beta_expander("Illumination settings")
    with ill_settings:
        options=["FITC","DAPI","Cy5","GFP","Rhodamine"]
        state.channels=st.multiselect("Select channels",options,state.channels)
    
    
    # Mandatory to avoid rollbacks with widgets, must be called at the end of your app
    state.sync()    

if __name__ == "__main__":
    a=time.time()
    main()
    b=time.time()
    st.write(b-a)
    
# =============================================================================
#     state.slider = st.sidebar.slider("Set slider value.", 1, 10, state.slider)
#     state.radio = st.sidebar.radio("Set radio value.", options, options.index(state.radio) if state.radio else 0)
#     state.checkbox = st.sidebar.checkbox("Set checkbox value.", state.checkbox)
#     state.selectbox = st.sidebar.selectbox("Select value.", options, options.index(state.selectbox) if state.selectbox else 0)
#     state.multiselect = st.sidebar.multiselect("Select value(s).", options, state.multiselect)
# =============================================================================
