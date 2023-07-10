import numpy as np
import pandas as pd
pd.set_option('mode.chained_assignment', None)
import streamlit as st
#from datetime import datetime
#from datetime import timedelta
import plotly.express as px
import plotly.graph_objects as go
#import scipy.optimize as optimize
from PIL import Image


fraCurve = "FRA_30062023.csv"
bondCurve = "Bond_30062023.csv"
swapCurve = "Swap_30062023.csv"

previous = 'May'
current = 'June'

previous_name = previous+"-23"
current_name = current+"-23"

@st.cache_data
def data(file):
    df = pd.read_csv(file, delimiter=",", skipinitialspace = True)
    return df


@st.cache_data
def convert_df(df):
    return df.to_csv().encode('utf-8')


fra = data(fraCurve)
swap = data(swapCurve)
bond = data(bondCurve)

fraDF = convert_df(fra)
swapDF = convert_df(swap)
bondDF = convert_df(bond)


@st.cache_data
def marketCurves(data, previous, previous_name, current, current_name, name, title1):

    count = data.shape[0]

    fig = go.Figure()
    # Create and style traces'
    fig.add_trace(go.Scatter(x=data['Term'], y=data[previous], name=previous_name,
                            line=dict(color='royalblue', width=4)))
    fig.add_trace(go.Scatter(x=data['Term'], y=data[current], name = current_name,
                            line=dict(color='firebrick', width=4)))

    # Edit the layout
    fig.update_layout(title=title1,
                    xaxis_title=name,
                    yaxis_title='Rate')

    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.15,
        xanchor="left",
        x=-0.1
    ))

    fig.update_layout(height=35*count, width=900, margin=dict(l=0, r=0, b=0,t=0))

    return fig


@st.cache_data
def curveTables(data, previous, current):

    palette0 = px.colors.qualitative.Set3

    totalColor = palette0[10]
    rowEvenColor = 'white'
    rowOddColor = palette0[1]

    palette0 = px.colors.qualitative.Set3

    headerColor = palette0[11]
    
    count = data.shape[0]
    col = data.shape[1]

    colors = []

    for i in range(0,count):
        if((i%2) == 0):
            colors.append(rowEvenColor)
        else:
            colors.append(rowOddColor)

    colors.append(totalColor)
    

    head = ['<b>Term<b>', '<b>'+previous+'<b>', '<b>'+current+'<b>', '<b>Change<b>' ]
    

    iterm = data['Term'].to_list()
    iprevious = data[previous].map('{:,.2f}'.format).to_list()
    icurrent = data[current].map('{:,.2f}'.format).to_list()
    ichange = data['Change'].to_list()


    count1 = len(iterm)
    for i in range(0,count1):
        iterm[i] = '<b>'+str(iterm[i])+'<b>'


    fig = go.Figure(data=[go.Table(
        
        columnorder = [1,2,3, 4],
        columnwidth = [20, 20, 20, 20],
        
        header=dict(values=head,
                    fill_color = headerColor,
                    line_color='darkslategray',
                    font=dict(color='black'),
                    align=['left', 'center', 'center', 'center']),
        cells=dict(values=[iterm, iprevious, icurrent, ichange],
                   fill_color = [colors*col],
                   line_color='darkslategray',
                   font=dict(color='black'),
                   align=['left', 'center', 'center', 'center']))
    ])   

    fig.update_layout(height=35*count, width=300, margin=dict(l=1, r=0, b=0,t=1))
    
    return fig

customized_button = st.markdown("""
    <style >
    .stDownloadButton, div.stButton {text-align:left}
    .stDownloadButton button, div.stButton > button:first-child {
        background-color: #ADD8E6;
        color:#000000;
        padding-left: 20px;
        padding-right: 20px;
    }
    
    .stDownloadButton button:hover, div.stButton > button:hover {
        background-color: #ADD8E6;
        color:#000000;
    }
        }
    </style>""", unsafe_allow_html=True)




st.sidebar.header("FRA Curve")
st.sidebar.download_button(label="Download FRA Curve", data=fraDF, file_name='FRA_Curve.csv', mime='text/csv')
fraCurve = marketCurves(fra, previous, previous_name, current, current_name, 'Term', 'FRA Curve (MOM)')
fraTable = curveTables(fra, previous, current)
#ftable, fcurve, frcurve = st.columns([1,3, 1])
#ftable.plotly_chart(fraTable, use_column_width=True)
#fcurve.plotly_chart(fraCurve, use_column_width=True)
#frcurve.header('Comments')
#frcurve.markdown('''FRA’s pricing in 1x25bps hike then flat for next year before expectations change to rate cuts''')
#frcurve.download_button(label="Download FRA Curve", data=fraDF, file_name='FRA_Curve.csv', mime='text/csv')
#ftable, fcurve = st.columns([1, 3])
#ftable.plotly_chart(fraTable, use_column_width=True)
#fcurve.plotly_chart(fraCurve, use_column_width=True)
st.sidebar.plotly_chart(fraTable)
#st.sidebar.download_button(label="Download FRA Curve", data=fraDF, file_name='FRA_Curve.csv', mime='text/csv')
st.header("FRA Curve")
st.plotly_chart(fraCurve)





st.sidebar.header("Swap Curve")
st.sidebar.download_button(label="Download Swap Curve", data=swapDF, file_name='Swap_Curve.csv', mime='text/csv')
swapCurve = marketCurves(swap, previous, previous_name, current, current_name, 'Term', 'Swap Curve (MOM)')
swapTable = curveTables(swap, previous, current)
#stable, scurve, swcurve = st.columns([1,3,1])
#stable.plotly_chart(swapTable, use_column_width=True)
#scurve.plotly_chart(swapCurve, use_column_width=True)
#swcurve.header('Comments')
#swcurve.markdown('''ABSA: Belly of Swap Curve is expected to underperform''')
#swcurve.download_button(label="Download Swap Curve", data=swapDF, file_name='Swap_Curve.csv', mime='text/csv')
#stable, scurve = st.columns([1,3])
#stable.plotly_chart(swapTable, use_column_width=True)
#scurve.plotly_chart(swapCurve, use_column_width=True)

st.sidebar.plotly_chart(swapTable)
#st.sidebar.download_button(label="Download Swap Curve", data=swapDF, file_name='Swap_Curve.csv', mime='text/csv')


st.header("Swap Curve")
st.plotly_chart(swapCurve)

#st.header("Bond Curve")
#st.download_button(label="Download Bond Curve", data=bondDF, file_name='Bond_Curve.csv', mime='text/csv')
#bondCurve = marketCurves(bond, previous, previous_name, current, current_name, 'Bond', 'Bond Curve (MOM)')
#bondTable = curveTables(bond, previous, current)
#btable, bcurve = st.columns([1,3])
#btable.plotly_chart(bondTable, use_column_width=True)
#bcurve.plotly_chart(bondCurve, use_column_width=True)


st.sidebar.header("Bond Curve")
st.sidebar.download_button(label="Download Bond Curve", data=bondDF, file_name='Bond_Curve.csv', mime='text/csv')
bondCurve = marketCurves(bond, previous, previous_name, current, current_name, 'Bond', 'Bond Curve (MOM)')
bondTable = curveTables(bond, previous, current)
#btable, bcurve, ccurve = st.columns([1,3,1])
#btable.plotly_chart(bondTable, use_column_width=True)
#bcurve.plotly_chart(bondCurve, use_column_width=True)
#ccurve.header('Comments')
#ccurve.markdown('Belly of Bond curve looks attractive: R2030 - R2032')
#ccurve.download_button(label="Download Bond Curve", data=bondDF, file_name='Bond_Curve.csv', mime='text/csv')
#btable, bcurve = st.columns([1,3])
#btable.plotly_chart(bondTable, use_column_width=True)
#bcurve.plotly_chart(bondCurve, use_column_width=True)

st.sidebar.plotly_chart(bondTable)
#st.sidebar.download_button(label="Download Bond Curve", data=bondDF, file_name='Bond_Curve.csv', mime='text/csv')

st.header("Bond Curve")
st.plotly_chart(bondCurve)