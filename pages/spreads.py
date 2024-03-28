import numpy as np
import pandas as pd
pd.set_option('mode.chained_assignment', None)
import streamlit as st
st.set_page_config(layout="wide")
#from datetime import datetime
#from datetime import timedelta
import plotly.express as px
import plotly.graph_objects as go
#import scipy.optimize as optimize
from PIL import Image


##########################################################################

import json
import requests
from streamlit_lottie import st_lottie

##########################################################################
#url = requests.get(
#    "https://assets2.lottiefiles.com/packages/lf20_mDnmhAgZkb.json")
## Creating a blank dictionary to store JSON file,
## as their structure is similar to Python Dictionary
#url_json = dict()
#  
#if url.status_code == 200:
#    url_json = url.json()
#else:
#    print("Error in the URL")
#  
#  
#st.title("Adding Lottie Animation in Streamlit WebApp")
#  
#st_lottie(url_json)
#########################################################################
#url = requests.get(
#    #"https://assets2.lottiefiles.com/packages/lf20_mDnmhAgZkb.json")
#    "https://lottiefiles.com/animations/stock-market-animated-icon-xIdpRO1561.json")
#url_json = dict()
#if url.status_code == 200:
#    url_json = url.json()
#else:
#    print("Error in URL")
  

#st.title("Adding Lottie Animation in Streamlit WebApp")

url = 'animation_ljzfr9ug.json'


with open(url, 'r') as fson:  
    res = json.load(fson)


url_json = res

#st_lottie(url_json,
#          # change the direction of our animation
#          reverse=True,
#          # height and width of animation
#          #height=200,  
#          #width=100,
#          # speed of animation
#          speed=1,  
#          # means the animation will run forever like a gif, and not as a still image
#          loop=True,  
#          # quality of elements used in the animation, other values are "low" and "medium"
#          quality='high',
#           # THis is just to uniquely identify the animation
#          key='Car' 
#          )

#########################################################################







file = 'spreads.csv'

@st.cache_data
def data(file):
    df = pd.read_csv(file, delimiter=",", skipinitialspace = True)
    return df


@st.cache_data
def convert_df(df):
    return df.to_csv().encode('utf-8')


spreads = data(file)

spreads['Date']=pd.to_datetime(spreads['Date'],format="%Y/%m/%d") ##Convert to datetime


spreadsDF = convert_df(spreads)


@st.cache_data
def marketCurves(data, metric, col):

    #count = data.shape[0]

    fig = go.Figure()
    # Create and style traces'
    fig.add_trace(go.Scatter(x=data['Date'], y=data[metric], name=metric,
                            line=dict(color=col, width=4)))
    #fig.add_trace(go.Scatter(x=data['Term'], y=data[current], name = current_name,
    #                        line=dict(color='firebrick', width=4)))

    # Edit the layout
    fig.update_layout(
                    #title=metric,
                    xaxis_title='Date',
                    yaxis_title='Spread')


    fig.update_layout(height=300, width=600, margin=dict(l=0, r=0, b=0,t=0))

    return fig




ban, head = st.columns([1,2])

banner1 = Image.open('AC1.jpg')
ban.image(banner1)
ban.markdown(" ")
ban.markdown(" ")

head.markdown(" ")
head.markdown(" ")
#head.markdown("<h1 style='text-align: left; color: #008080; padding-left: 20px; font-size: 80px'><b>SA Curves & Global Bonds<b></h1>", unsafe_allow_html=True)
head.markdown("<h1 style='text-align: left; color: gray; padding-left: 20px; font-size: 80px'><b>US & SA Spreads<b></h1>", unsafe_allow_html=True)

#st.sidebar.markdown("<h1 style='text-align: left; color: gray; padding-left: 0px; font-size: 40px'><b>Cuve Tables<b></h1>", unsafe_allow_html=True)

with st.sidebar:
    st_lottie(url_json,
            # change the direction of our animation
            reverse=True,
            # height and width of animation
            height=200,  
            width=200,
            # speed of animation
            speed=1,  
            # means the animation will run forever like a gif, and not as a still image
            loop=True,  
            # quality of elements used in the animation, other values are "low" and "medium"
            quality='high',
            # THis is just to uniquely identify the animation
            key='Car' 
            )



#st.sidebar.markdown("<h1 style='text-align: left; color: gray; padding-left: 0px; font-size: 40px'><b>Cuve Tables<b></h1>", unsafe_allow_html=True)

#banner2 = Image.open('AC22.png')
#st.sidebar.image(banner2)


#a, b = st.columns([1,1])
#c, d = st.columns([1,1])


#st.sidebar.header("FRA Curve")
#st.sidebar.download_button(label="Download FRA Curve", data=fraDF, file_name='FRA_Curve.csv', mime='text/csv')
USSpread = marketCurves(spreads, 'US_10Y-2Y', 'royalblue')
st.header("US 10Y-2Y Spread")
st.plotly_chart(USSpread)
st.markdown(" ")
st.markdown(" ")

USSpread = marketCurves(spreads, 'US_Real', 'firebrick')
st.header("US_Real")
st.plotly_chart(USSpread)
st.markdown(" ")
st.markdown(" ")


USSpread = marketCurves(spreads, 'SA_Real', 'darkgreen')
st.header("SA_Real")
st.plotly_chart(USSpread)
st.markdown(" ")
st.markdown(" ")

st.sidebar.markdown("<h1 style='text-align: left; color: #008080; padding-left: 0px; font-size: 25px'><b>Spread Analysis<b></h1>", unsafe_allow_html=True)



