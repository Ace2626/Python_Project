import streamlit as st
import numpy as np
import pandas as pd
from data_analysis import set_color

set_color()

def show_intro():
    st.title("Spam Email Prediction Using kNN")

    st.subheader("Introduction")

    paragraph_1 = """
    
    This web application guides you through the developpment of **an AI trained to
    recognize _SPAM emails_ ** based of the following dataset : https://archive.ics.uci.edu/ml/datasets/Spambase
        
    Our IA is based on the **k nearest neighbours (kNN) algorithm**. For each input's equivalent in the database's
    _57-dimensional_ hyperplane, the algorithm searches it's nearest neibours and predicts the input's type by returning
    the dominant neighbouring class.

    Even though slow, this algorithm yields *the best results* with this specific dataset **(94%)** by a fair margin of **5 points**
    compared to the rest. Various tries and parameter optimizations have been tried with the following as well :

    * Support Vector Machines
    * Trees / Random Forests
    * Linear Classifiers (LDA, Naive Bayes ...)
    * Logistic Regression
    """

    st.markdown(paragraph_1)

    st.subheader("Data Parser API")

    paragraph_2 = """
    
    The algorithm runs using **57 parameters** from the dataset :

    * Frequencies of various *words* in the email
    * Frequencies of various *characters* in the email
    * Average, Longest and Total *capital run length*

    Hence we've written an API to **parse the data of a text input** and turn it into the required 57 parameters,
    so we could feed it to the prediction model.

    The first step was to convert the input to a format where word frequency is easier to analyse :
    """

    text_format_func = '''def format_text_for_word_freq(text : str):
    chars = [',','.','?','!']
    for char in chars:
        text = text.replace(char,'')

    text = text.lower()
    return text'''

    st.markdown(paragraph_2)
    st.code(text_format_func)

    paragraph_3 = """
    
    Word frequency is processed using the *Counter function from the Collections library* :
    
    """

    word_freq_func = '''def get_word_freq(words : list, text : str):

    formated_text = format_text_for_word_freq(text).split()
    text_data = Counter(formated_text)
    freqs = []

    for word in words:
        if word in text_data.keys():
            freqs.append(text_data[word]/len(formated_text))
        else:
            freqs.append(0)

    zipper = zip(words,freqs)
    result = dict(zipper)
    return result'''

    st.markdown(paragraph_3)
    st.code(word_freq_func)

    paragraph_4 = """
    
    The **same process** is used to determine *char frequency*, but using the *raw text input*.

    Capital run length information is gathered with the use of a specific **parser class** created for the task. An object
    from this class takes in a string and can iterate over it char by char until it ends. Unlike an iterator, calling the 
    next() method from this class **only returns the following char of the string**.
    
    """

    parser_class_code = '''class cap_parser:
    def __init__(self, cap_text : str):
        self.text = cap_text
        self.pointer = 0
        self.current = self.text[self.pointer]

    def next(self):
        self.pointer += 1
        return self.text[self.pointer]

    def is_end(self):
        return self.text[self.pointer + 1 ] == None'''

    st.markdown(paragraph_4)
    st.code(parser_class_code)

    paragraph_5 = """
    
    The gathered data is then fit into a **2-dim array ordered like the training dataset** so the prediction model
    can process it :
    
    """

    process_func = '''def parse_text_data(text : str):
    key_words = ['make','address','all','3d','our','over','remove','internet','order','mail','receive','will','people','report','addresses','free','business','email','you','credit','your','font','000','money','hp','hpl','george','650','lab','labs','telnet','857','data','415','85','technology','1999','parts','pm','direct','cs','meeting','original','project','re','edu','table','conference']
    key_chars = [';','(','[','!','$','#']

    word_analysis = get_word_freq(key_words,text)
    char_analysis = get_char_freq(key_chars,text)
    cap_analysis = get_capital_run_length(text)

    results = dict(word_analysis)
    results.update(char_analysis)
    results.update(cap_analysis)

    res = []
    res.append([*results.values()])

    return res'''

    st.markdown(paragraph_5)
    st.code(process_func)

    st.title("Comments On The Dataset")
    st.subheader("Real World Efficiency")

    paragraph_6 = """
    
    It's import to keep in mind that _the training dataset has been assembled in **1998**_. Spam emails back in the day
    were different from today's standart. Communication in the early 2000s was not as spontaneous as it is today.
    _Messages were **longer** and **denser** in content_ due to slow network speeds making extremely spontaneous communication unrealistic

    For instance, spam emails in the dataset have an **average total capital letters count of 470**. That's more characters
    than in most of the recent spam emails we've run into.

    """

    cap_run_mean_code = '''df=pd.read_csv('spambase.data')
df[df["Spam"] == 1]['capital_run_length_total'].mean()

# >>> 470.61941533370106'''

    st.markdown(paragraph_6)
    st.code(cap_run_mean_code)

    st.subheader("Consequences on predictions")

    paragraph_7 = """
    
    The average number of capital letters in spam emails from 1998 is already a lot longer than modern spam emails in whole.
    Since modern spams are notably shorter, _it makes a frequency based approach like in the dataset **innacurate** and **overly
    sensitive** to small variations_.

    Here's an example where changing **'it'** to **'you'** in a non-spam email **makes the AI predict it as a spam**.

    Note : You can check for yourself in the "PREDICT FROM TEXT" section of the app.
    
    """

    not_spam = '''# In this first example, the AI rightfully predicts this is not a SPAM email
text_not_spam = "Please Jordan, we would like it to stop. Throwing rocks at classmates is mean."
predict(text_nspam)

# NOT A SPAM'''

    spam_1 = '''# Now we replace 'it' with 'you', and it's enough to cross the decision boundary
text_spam_1 = "Please Jordan, we would like you to stop. Throwing rocks at classmates is mean."
predict(text_spam_1)

# SPAM'''

    spam_2 = '''# The same happens by simpling adding 'your' before 'classmates'
text_spam_2 = "Please Jordan, we would like it to stop. Throwing rocks at your classmates is mean."
predict(text_spam_2)

# SPAM'''

    st.markdown(paragraph_7)
    st.code(not_spam)
    st.code(spam_1)
    st.code(spam_2)

    st.subheader("Conclusion")

    paragraph_8 = '''
    
    A frequency based approach is **not sufficient _for the more common short texts from today_**. For instance in a text of 
    10 words, _having the word 'you' appear once gives it a frequency of 10%_, enough to automatically classify the email as
    a spam.

    To correctly train a prediction model on common short texts, **both word frequency and work count are necessary**.
    FYI, a word frequency of **50%** but a count of 1 would mean the text is 2 words long. A simple message like
    "Thank you" would therefore not be classified as spam with correct model training.
    
    '''

    st.markdown(paragraph_8)