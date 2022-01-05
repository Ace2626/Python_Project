import streamlit as st
import pickle
import numpy as np
import random
import json
from text_parser import parse_text_data, parse_json
from predict import load_model

KEYWORDS_ = ['make','address','all','3d','our','over','remove','internet','order','mail','receive','will','people','report','addresses','free','business','email','you','credit','your','font','000','money','hp','hpl','george','650','lab','labs','telnet','857','data','415','85','technology','1999','parts','pm','direct','cs','meeting','original','project','re','edu','table','conference']
KEYCHARS_ = [';','(','[','!','$','#']
KEYLENGTHS_ = ['Average Capital Run Length','Max Capital Run Length','Total Capital Run Length']
SLIDER_VALUES_ = {}
MODEL_ = load_model()

def show_sandbox(message : str):
    st.title(message)

    slider_type = st.selectbox("What do you want to do ?",["","I want to input the values myself","Give me random !","I have values I want to import"])
    
    if slider_type == "I want to input the values myself":
        standart_sliders()
    elif slider_type == "Give me random !":
        random_sliders()
    elif slider_type == "I have values I want to import":
        import_sliders()

    send = st.button("Predict")

    if send:
        data = [list(SLIDER_VALUES_.values())]
        prediction = MODEL_.predict(data)

        translator = dict({0 : 'NOT A SPAM', 1 : 'SPAM'})
        st.subheader(translator[prediction[0]])

def standart_sliders():
    for word in KEYWORDS_:
        SLIDER_VALUES_[word] = st.slider(word + "_frequency :", min_value=0.0, max_value=100.0, step=0.01)

    for char in KEYCHARS_:
        SLIDER_VALUES_[char] = st.slider(char + "_frequency :", min_value=0.0, max_value=100.0, step=0.01)

    for length in KEYLENGTHS_:
        SLIDER_VALUES_[length] = st.number_input(length, min_value=0.0, max_value=1000.0, step = 0.1)

    standart_dl = st.button("Download Data", SLIDER_VALUES_, "data.json")

    if standart_dl:
        with open('data.json', 'w') as outfile:
            try:
                json.dump(SLIDER_VALUES_, outfile)  
                st.write("Download successful")     
            except:
                st.write("Download failed")

def import_sliders(): 
    filename = st.text_input('Enter a json file path:')
    st.write('Valid json example : {"make": 0.86, "address": 0.17, ...}')
    if filename != "" or None:
        try:
            with open(filename) as input:
                file = input.read()
                file = dict(json.loads(file))
                for val in file:
                    SLIDER_VALUES_[val] = file[val]                 
        except FileNotFoundError:
            st.error('File not found.')

def random_sliders():
    for word in KEYWORDS_:  
        SLIDER_VALUES_[word] = st.slider(word + "_frequency :", min_value=0.0, max_value=100.0, step=0.01, value=float(np.round(random.uniform(0,100),2)))

    for char in KEYCHARS_:
        SLIDER_VALUES_[char] = st.slider(char + "_frequency :", min_value=0.0, max_value=100.0, step=0.01, value=float(np.round(random.uniform(0,100),2)))

    for length in KEYLENGTHS_:
        SLIDER_VALUES_[length] = st.number_input(length, min_value=0.0, max_value=1000.0, step = 0.1)

    random_dl = st.button("Download Data")

    if random_dl:
        with open('data.json', 'w') as outfile:
            try:
                json.dump(SLIDER_VALUES_, outfile)  
                st.write("Download successful")     
            except:
                st.write("Download failed")

        

