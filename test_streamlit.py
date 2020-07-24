
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""

import streamlit as st
import feedback_functions as ff
import updated_variables as uv
import numpy as np
import time
import pycromanager as pm
from PIL import Image
import copy
import classes as cl
import pandas as pd

handles=ff.init_fcn(0)

st.title("Test acquisition function")
st.write("Current time step : ",handles.current_time_step)

st.write(handles.init_time)

st.slider('test',0,50)

#a=st.sidebar.selectbox('test1',('proposition 1','der'))

if st.button('initialize again'):
    handles.session_id=np.random.rand()
    ff.init_fcn(handles.session_id)

check=st.checkbox('this is a test')
if check:
    path=uv.__file__
    with open(path,"w") as fp:
        fp.writelines(['a=5 \n','b=7 \n'])


st.write(uv.a)

if st.button('Start acquisition'):
    ff.start_acq(handles)
    
st.sidebar.header(uv.b)
        

# =============================================================================
# t=h.PT(1,ff.printer(handles))
# t.start()
# 
# =============================================================================
if st.button('Stop acquisition'):
    ff.stop_acq(handles)


nbsteps=st.sidebar.number_input('Number of steps',1)
timestep=st.sidebar.number_input('Time step (in s)',1)    

if st.button('Acquire'):
    ff.acq_fcn(handles)
    #handles.disp_image=Image.open('test.png')
    
st.image(handles.disp_image,caption='blablabla',use_column_width=True,format='PNG')

if st.button('Add position'):
    ff.add_pos(handles.core,handles.all_pos)
    handles.num_pos=handles.num_pos+1
    
dataframe = ff.get_table(handles.all_pos,handles.num_pos,handles.session_id)
st.write(dataframe)
selected_indices = st.selectbox('Select rows:', dataframe.index)
selected_rows = dataframe.loc[selected_indices]
# =============================================================================
# @st.cache  # 👈 This function will be cached
# def my_slow_function(arg1, arg2):
#     # Do something really slow in here!
#     return the_output
# 
# =============================================================================

# =============================================================================
# progress_bar = st.progress(0)
# status_text = st.empty()
# chart = st.line_chart(np.random.randn(10, 2))
# 
# for i in range(100):
#     # Update progress bar.
#     progress_bar.progress(i + 1)
# 
#     new_rows = np.random.randn(10, 2)
# 
#     # Update status text.
#     status_text.text(
#         'The latest random number is: %s' % new_rows[-1, 1])
# 
#     # Append data to the chart.
#     chart.add_rows(new_rows)
# 
#     # Pretend we're doing some computation that takes time.
#     time.sleep(0.1)
# 
# status_text.text('Done!')
# st.balloons()
# =============================================================================
