import streamlit as st
st.set_page_config(layout="wide")
import json
from PIL import Image
from streamlit_lottie import st_lottie


url='data.json'

with open(url, 'r') as fson:  
    res = json.load(fson)


url_json = res


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
            key='Car',
            )
    

st.sidebar.markdown("<h1 style='text-align: left; color: #008080; padding-left: 0px; font-size: 25px'><b>Fair Value Estimates<b></h1>", unsafe_allow_html=True)

fv = st.sidebar.checkbox('Show Analytics FV Model')

if fv:


    st.markdown("<h1 style='text-align: left; color: gray; padding-left: 30px; font-size: 40px'><b>Analytics Fair Value Model<b></h1>", unsafe_allow_html=True)

    st.markdown(" ")
    st.markdown(" ")

    col1, cola, col2 = st.columns([1,0.25, 1])

    banner3 = Image.open('fmModelSummary.jpg')
    col2.image(banner3)


    banner2 = Image.open('fmModelGraph.jpg')
    col1.image(banner2)

   
    col1.markdown("<h1 style='text-align: center; color: darkred; padding-left: 0px; font-size: 15px'><b>- Debt/GDP & Current Account/GDP<b></h1>", unsafe_allow_html=True)
    col1.markdown("<h1 style='text-align: center; color: darkred; padding-left: 0px; font-size: 15px'><b>- US 10Yr Bond Yield & SA 5YR CDS Spread<b></h1>", unsafe_allow_html=True)
    col1.markdown("<h1 style='text-align: center; color: darkred; padding-left: 0px; font-size: 15px'><b>- Business Confidence Index & Interest Differential<b></h1>", unsafe_allow_html=True)


else:
    st.markdown("<h1 style='text-align: left; color: gray; padding-left: 0px; font-size: 40px'><b>Absa Fair Value Forecast<b></h1>", unsafe_allow_html=True)

    banner2 = Image.open('ABSA_FV.jpg')
    st.image(banner2)

    st.markdown(" ")
    st.markdown(" ")

    banner3 = Image.open('ABSA_Comments.jpg')
    st.image(banner3)