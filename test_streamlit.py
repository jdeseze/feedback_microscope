
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""

import streamlit as st
import feedback_functions as ff

handles=ff.initFcn()
st.write(handles.init_time)

time_step=st.number_input("Time step (in s)",0,None,0)
nb_steps=st.number_input("Number of steps",0,None,0)


st.slider('test',0,50)

#a=st.sidebar.selectbox('test1',('proposition 1','der'))

timebutton=st.button("hola")

if timebutton:
    st.write("blague")


check=st.checkbox('this is a test')

if check:
    "holaaaa"

if st.button("ohlala"):
    #ff.print_time(init_time)
    ff.hello_world()
    st.write(handles.init_time)

start_button=st.button('Start')
if start_button:
    testval=ff.startFcn()
    


# =============================================================================
# @st.cache  # 👈 This function will be cached
# def my_slow_function(arg1, arg2):
#     # Do something really slow in here!
#     return the_output
# 
# =============================================================================

