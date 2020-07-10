
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""

import streamlit as st

st.write('hello world!!')

st.slider('test')

a=st.sidebar.selectbox('test1',('proposition 1','der'))

st.sidebar.button("hola")

check=st.checkbox('this is a test')

if check==True:
    "holaaaa"

# =============================================================================
# @st.cache  # 👈 This function will be cached
# def my_slow_function(arg1, arg2):
#     # Do something really slow in here!
#     return the_output
# 
# =============================================================================

