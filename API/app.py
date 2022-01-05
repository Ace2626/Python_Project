from warnings import showwarning
import streamlit as st
from predict import show_predict_page
from sandbox import show_sandbox
from visualize_data import show_data
from intro import show_intro

menu = st.sidebar
menu.markdown('<p style="font-family:Courier">© Yvann Vincent</p>', unsafe_allow_html=True)
menu.markdown('<p style="font-family:Courier">© Antoine Serafini</p>', unsafe_allow_html=True)
display = st.sidebar.selectbox("MENU",("Introduction","Predict From Text","Sandbox","Visualize Data"))

if display == "Introduction":
    show_intro()
elif display == "Predict From Text":
    show_predict_page()
elif display == "Sandbox":
    show_sandbox("Have fun playing around !")
else:
    show_data()
