# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 15:58:48 2020

@author: Jean
"""
import streamlit as st
import time
import handles as h

def print_time(a):
    st.write(a)
    
def hello_world():
    st.write("Hello World")

@st.cache    
def startFcn(handles):
    #timer=time.time
    #init_time=int(timer)
    st.write('startFcn')
    return time.time()-handles.init_time

@st.cache
def initFcn():   
    handles=h.handles
    timer=time.time()
    handles.init_time=int(timer)
    return handles
