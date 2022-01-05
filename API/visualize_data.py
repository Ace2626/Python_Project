import streamlit as st
import pickle
import numpy as np
import matplotlib.pyplot as plt
from predict import prepare_data, load_model
from text_parser import parse_text_data
from data_analysis import spam_distribution, load_data, plot_cm, plot_prediction_results, pca

DATA_ = load_data()
X_TRAIN_, X_TEST_, Y_TRAIN_, Y_TEST_ = prepare_data(DATA_)
MODEL_ = load_model()
PREDICTION_ = MODEL_.predict(X_TEST_)

def show_data():
    st.title("Visuals From Training Database")

    st.subheader("Spam distribution in the database")
    spam_distribution(DATA_)

    st.subheader("Prediction accuracy on a testing set")
    plot_cm(Y_TEST_,PREDICTION_)

    plot_prediction_results(PREDICTION_,Y_TEST_,X_TRAIN_,DATA_)

    pca(DATA_)



