from PIL import Image
import numpy as np
import pandas as pd
import streamlit as st
import altair as alt
from wordcloud import WordCloud, STOPWORDS
# Importing the StringIO module.
from io import StringIO 
import glob, nltk, os, re
from nltk.corpus import stopwords
from pathlib import Path
nltk.download('all')

st.markdown('''
# Analyzing Shakespeare Texts
''')

# Create a dictionary (not  list)
books = {" ":" ","A Mid Summer Night's Dream":"data/summer.txt","The Merchant of Venice": "data/merchant.txt","Romeo and Juliet": "data/romeo.txt"}

## SIDEBAR
st.sidebar.header('Word Cloud Settings')
max_word = st.sidebar.slider("Max Words",min_value=10,max_value=200,value=100, step=10)
max_font = st.sidebar.slider("Size of largest Word",min_value=50,max_value=350,value=60, step=10)
img_width = st.sidebar.slider("Image Width",min_value=100,max_value=800,value=400, step=10)
random = st.sidebar.slider("Random State", min_value=30,max_value=100,value=20)
remove_stop_words = st.sidebar.checkbox("Remove Stop Words?",value=True)
st.sidebar.header('Word Count Settings')
n_words = st.sidebar.slider("Minimum count of words",min_value=5,max_value=100,value=40, step=1)

## Select text files
image = st.selectbox("Choose a txt file", books.keys())

# This is going to return summer/merchant/romeo because we are matching on the key and getting the value
image = books.get(image)

if image != " ":
    stop_words =[]
    raw_text = open(image,"r").read().lower()
    nltk_stop_words = stopwords.words('english')
    dataset = re.sub(r'[^\w\s]', '', raw_text)
    
    if remove_stop_words:
        stop_words = set(nltk_stop_words)
        stop_words.update(['us', 'one', 'will', 'said', 'now', 'well', 'man', 'may',
        'little', 'say', 'must', 'way', 'long', 'yet', 'mean',
        'put', 'seem', 'asked', 'made', 'half', 'much',
        'certainly', 'might', 'came'])
        
    tokens = nltk.word_tokenize(dataset)
    tokens = [w for w in tokens if not w.lower() in stop_words] 
    
tab1,tab2,tab3 = st.tabs(['Word Cloud','Bar Chart','View Text'])

with tab1:
   if image != " ":
        cloud = WordCloud(background_color = "white", 
                            max_words = max_word, 
                            max_font_size=max_font, 
                            stopwords = stop_words, 
                            random_state=random)
        wc = cloud.generate(dataset)
        word_cloud = wc.to_file('wordcloud.png')
        st.image(wc.to_array(),width=img_width)

with tab2:
    if image != " ":
        st.markdown('''
                    #### Bar Chart
                    ''')
        frequency = nltk.FreqDist(tokens)
        freq_df = pd.DataFrame(frequency.items(),columns=['word','count'])
        freq_chart = alt.Chart(freq_df).transform_filter(
            alt.FieldGTEPredicate(field='count', gte=n_words)
            ).mark_bar().encode(
                y=alt.Y('word',sort=alt.EncodingSortField('count', op='min', order='descending')),
                x='count'
                #color=alt.Color('count',scale=alt.Scale(scheme='reds'))
            ).properties(
                width=800
            )
        freq_text = freq_chart.mark_text(
            align='left',
            baseline='middle',
            dx=3
        ).encode(
            text='count'
        )
        chart = freq_chart+freq_text
        st.altair_chart(chart)
            
    

with tab3:        
    if image != " ":
        st.markdown('''
                #### All Text
                ''')
        st.write(raw_text)