import streamlit as st
import pickle
import numpy as np
import pandas as pd
from text_parser import parse_text_data
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def load_model():
    with open('model_spam.pickle','rb') as file:
        model = pickle.load(file)

    return model

model = load_model()

def show_predict_page():
    st.title("Email Spam Detector")
    st.write("#### Paste the email below")

    text = st.text_area(label="")
    submit = st.button(label="Analyse")

    if(submit):
        predict(text)

def predict(text):
    data = parse_text_data(text)
    prediction = model.predict(data)

    translator = dict({0 : 'NOT A SPAM', 1 : 'SPAM'})

    st.subheader(translator[prediction[0]])

def prepare_data(df):

    X = df
    X = X.drop('Spam',1)
    Y = df['Spam']

    X_train,X_test,Y_train,Y_test=train_test_split(X,Y,test_size=0.2)

    scaler=StandardScaler()
    scaler.fit(X_train) #on filtre uniquement sur les data d'entrainement
    X_train=scaler.transform(X_train)
    X_test=scaler.transform(X_test) #pareille transformation sur les data test

    # X_train = pd.DataFrame(X_train)
    # X_test = pd.DataFrame(X_test)
    # Y_train = pd.DataFrame(Y_train)
    # Y_test = pd.DataFrame(Y_test)

    return X_train, X_test, Y_train, Y_test

