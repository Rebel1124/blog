import streamlit as st
st.set_page_config(layout="wide")
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import json
from streamlit_lottie import st_lottie
from plotly.subplots import make_subplots

#url = 'animation_ljzfr9ug.json'
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


#st.sidebar.header('Economic Activity')
st.sidebar.markdown("<h1 style='text-align: left; color: #008080; padding-left: 0px; font-size: 25px'><b>Economic Activity<b></h1>", unsafe_allow_html=True)

gdp = st.sidebar.select_slider(
    label='Real GDP (Growth Expectations)',
    options=['Strong Negative', 'Moderate Negative', 'Neutral', 'Moderate Positive', 'Strong Positive'],
    value=('Moderate Negative'))

st.sidebar.markdown('')
st.sidebar.markdown('')
st.sidebar.markdown('')

cpi = st.sidebar.select_slider(
    'CPI (Inflation Expectations)',
    options=['Strong Negative', 'Moderate Negative', 'Neutral', 'Moderate Positive', 'Strong Positive'],
    value=('Moderate Positive'))

st.sidebar.markdown('')
st.sidebar.markdown('')
st.sidebar.markdown('')

unemployment = st.sidebar.select_slider(
    'Unemployment',
    options=['Strong Negative', 'Moderate Negative', 'Neutral', 'Moderate Positive', 'Strong Positive'],
    value=('Strong Negative'))

st.sidebar.markdown('')
st.sidebar.markdown('')
st.sidebar.markdown('')

#st.sidebar.header('System')
st.sidebar.markdown("<h1 style='text-align: left; color: #008080; padding-left: 0px; font-size: 25px'><b>System<b></h1>", unsafe_allow_html=True)

political = st.sidebar.select_slider(
    label='Political',
    options=['Strong Negative', 'Moderate Negative', 'Neutral', 'Moderate Positive', 'Strong Positive'],
    value=('Strong Negative'))

st.sidebar.markdown('')
st.sidebar.markdown('')
st.sidebar.markdown('')

bankingLegal = st.sidebar.select_slider(
    'Banking & Legal',
    options=['Strong Negative', 'Moderate Negative', 'Neutral', 'Moderate Positive', 'Strong Positive'],
    value=('Moderate Positive'))


st.sidebar.markdown('')
st.sidebar.markdown('')
st.sidebar.markdown('')

#st.sidebar.header('Policy')
st.sidebar.markdown("<h1 style='text-align: left; color: #008080; padding-left: 0px; font-size: 25px'><b>Policy<b></h1>", unsafe_allow_html=True)


repo = st.sidebar.select_slider(
    label='Repo Rate (Monetary)',
    options=['Strong Negative', 'Moderate Negative', 'Neutral', 'Moderate Positive', 'Strong Positive'],
    value=('Neutral'))

st.sidebar.markdown('')
st.sidebar.markdown('')
st.sidebar.markdown('')

ca = st.sidebar.select_slider(
    label='Current Account (Fiscal)',
    options=['Strong Negative', 'Moderate Negative', 'Neutral', 'Moderate Positive', 'Strong Positive'],
    value=('Moderate Negative'))

st.sidebar.markdown('')
st.sidebar.markdown('')
st.sidebar.markdown('')

budget = st.sidebar.select_slider(
    'Budget (Fiscal)',
    options=['Strong Negative', 'Moderate Negative', 'Neutral', 'Moderate Positive', 'Strong Positive'],
    value=('Moderate Negative'))

st.sidebar.markdown('')
st.sidebar.markdown('')
st.sidebar.markdown('')

#st.sidebar.header('Market')
st.sidebar.markdown("<h1 style='text-align: left; color: #008080; padding-left: 0px; font-size: 25px'><b>Market<b></h1>", unsafe_allow_html=True)


spread = st.sidebar.select_slider(
    label='10yr - 2yr Spread (US)',
    options=['Strong Negative', 'Moderate Negative', 'Neutral', 'Moderate Positive', 'Strong Positive'],
    value=('Neutral'))

st.sidebar.markdown('')
st.sidebar.markdown('')
st.sidebar.markdown('')

real = st.sidebar.select_slider(
    label='Real Yields',
    options=['Strong Negative', 'Moderate Negative', 'Neutral', 'Moderate Positive', 'Strong Positive'],
    value=('Neutral'))

st.sidebar.markdown('')
st.sidebar.markdown('')
st.sidebar.markdown('')

commodity = st.sidebar.select_slider(
    'Commodity Prices',
    options=['Strong Negative', 'Moderate Negative', 'Neutral', 'Moderate Positive', 'Strong Positive'],
    value=('Neutral'))

st.sidebar.markdown('')
st.sidebar.markdown('')
st.sidebar.markdown('')

currency = st.sidebar.select_slider(
    'ZAR/USD (Analytics Currency Decoder)',
    options=['Strong Negative', 'Moderate Negative', 'Neutral', 'Moderate Positive', 'Strong Positive'],
    value=('Moderate Negative'))



@st.cache_data
def scoreCalc(x):
    if(x=='Strong Negative'):
        val = 5
    elif(x=='Moderate Negative'):
        val = 4
    elif(x=='Neutral'):
        val=3
    elif(x=='Moderate Positive'):
        val=2
    else:
        val=1

    return val


gdpVal = scoreCalc(gdp)
cpiVal = scoreCalc(cpi)
unemploymentVal = scoreCalc(unemployment)
politicalVal = scoreCalc(political)
bankingLegalVal = scoreCalc(bankingLegal)
repoVal = scoreCalc(repo)
caVal = scoreCalc(ca)
budgetVal = scoreCalc(budget)
spreadVal = scoreCalc(spread)
realVal = scoreCalc(real)
commodityVal = scoreCalc(commodity)
currencyVal = scoreCalc(currency)

riskTotal = gdpVal+cpiVal+unemploymentVal+politicalVal+bankingLegalVal+repoVal+caVal+budgetVal+spreadVal+realVal+commodityVal+currencyVal

@st.cache_data
def mdTables():

    palette0 = px.colors.qualitative.Set3

    #totalColor = palette0[10]
    rowEvenColor = palette0[1]
    rowOddColor = 'white'

    palette0 = px.colors.qualitative.Set3

    headerColor = palette0[11]
    
    colors = [rowOddColor, rowEvenColor, rowOddColor, rowEvenColor, rowOddColor]

    head = ['<b>Risk Score<b>', '<b>10.00%<b>', '<b>10.75%<b>', '<b>11.50%<b>', '<b>12.25%<b>', '<b>13.00%<b>']
    
    band = ['<b>35-40<b>', '<b>40-45<b>', '<b>45-50<b>', '<b>50-55<b>', '<b>55-60<b>']
    score1 = [0.90, 0.85, 0.75, 0.65, 0.5]
    score2 = [0.95, 0.90, 0.85, 0.75, 0.65]
    score3 = [1, 0.95, 0.9, 0.85, 0.75]
    score4 = [1, 1, 0.95, 0.9, 0.85]
    score5 = [1,1,1,0.95,0.9]



    #text_color = []
    #n = len(df)
    #for col in band:
    #    if col!='output':
    #        text_color.append(["black"] * n)
    #    else:
    #        text_color.append(df["color"].to_list())


    riskCol = ['black']*5
    mdCol = ['gray']*5

    text_color = [riskCol,mdCol,mdCol,mdCol,mdCol,mdCol]

    fig = go.Figure(data=[go.Table(
        
        columnorder = [1, 2, 3, 4, 5, 6],
        columnwidth = [20, 20, 20, 20, 20,20],
        
        header=dict(values=head,
                    fill_color = headerColor,
                    line_color='darkslategray',
                    font=dict(color='black'),
                    align=['center', 'center', 'center', 'center', 'center', 'center']),
        cells=dict(values=[band, score1, score2, score3, score4, score5],
                   fill_color = [colors*5],
                   line_color='darkslategray',
                   font=dict(color=text_color),
                   align=['center', 'center', 'center', 'center', 'center', 'center']))
    ])   

    fig.update_layout(height=200, width=600, margin=dict(l=1, r=1, b=0,t=1))
    
    return fig



@st.cache_data
def mdVal(riskScore, rate):

    score1 = [0.90, 0.95, 1, 1, 1]
    score2 = [0.85, 0.90, 0.95, 1, 1]
    score3 = [0.75, 0.85, 0.9, 0.95, 1]
    score4 = [0.65, 0.75, 0.85, 0.9, 0.95]
    score5 = [0.5,0.65,0.75,0.85,0.9]

    scores = [score1,score2,score3,score4,score5]        

    if (riskScore < 40):
        i=0
    elif(riskScore < 45):
        i=1
    elif(riskScore < 50):
        i=2
    elif(riskScore < 55):
        i=3
    else:
        i=4

    
    if (rate <= 0.1):
        j=0
    elif(rate <= 0.1075):
        j=1
    elif(rate <= 0.115):
        j=2
    elif(rate <= 0.1225):
        j=3
    else:
        j=4

    if(j==4):
        k=4
    else:
        k=j+1

    md0 = scores[i][j]
    #md1 = scores[i][k]

    #md = [md0, md1]

    #return md
    return md0







@st.cache_data
def speedometer(risk, md):


    trace1 = go.Indicator(
        mode = "gauge+number",
        value = risk,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Risk Score", 'font': {'size': 24}},
        delta = {'reference': 35, 'increasing': {'color': "RebeccaPurple"}},
        gauge = {
            'axis': {'range': [None, 50], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 25], 'color': 'cyan'},
                {'range': [25, 50], 'color': 'royalblue'}],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 50}})


    trace2 = go.Indicator(
        mode = "gauge+number",
        value = md,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Modified Duration", 'font': {'size': 24}},
        delta = {'reference': 0.8, 'increasing': {'color': "RebeccaPurple"}},
        gauge = {
            'axis': {'range': [None, 1], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 0.5], 'color': 'cyan'},
                {'range': [0.5, 1], 'color': 'royalblue'}],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 1}})

    fig = make_subplots(
        rows=1,
        cols=2,
        specs=[[{'type' : 'indicator'}, {'type' : 'indicator'}]],
        )

    fig.append_trace(trace1, row=1, col=1)
    fig.append_trace(trace2, row=1, col=2)

    fig.update_layout(height=400, width=1000, margin=dict(l=0, r=1, b=0,t=0))


    return fig




ban, head = st.columns([1,2])

banner1 = Image.open('AC1.jpg')
ban.image(banner1)
ban.markdown(" ")
ban.markdown(" ")


process=Image.open('investment.jpg')

building = Image.open('building.jpg')

mandate = Image.open('mandate.jpg')

head.markdown(" ")
head.markdown(" ")
head.markdown("<h1 style='text-align: left; color: gray; padding-left: 20px; font-size: 80px'><b>Risk Monitor<b></h1>", unsafe_allow_html=True)



# #008080


metric, e, table = st.columns([2,0.5, 8])

metric.markdown("<h1 style='text-align: left; color: gray; padding-left: 0px; font-size: 20px'><b>Valuation<b></h1>", unsafe_allow_html=True)

metric.markdown("<h1 style='text-align: left; color: darkred; padding-left: 0px; font-size: 25px'><b>Risk Score: "+str(riskTotal)+"<b></h1>", unsafe_allow_html=True)

bondYield = metric.number_input('Bond Yield', min_value=0.000, max_value=0.200, step=0.005, value=0.1075)

#bondYield = 0.105

check = mdVal(riskTotal, bondYield)

test = mdTables()




#metric.markdown('Risk Score: '+str(riskTotal))


#metric.markdown('BondYield: '+str(bondYield))



#metric.markdown("<h1 style='text-align: left; color: darkgreen; padding-left: 0px; font-size: 20px'><b>Bond Yield: "+str(bondYield)+"<b></h1>", unsafe_allow_html=True)


if(check==1):
    #metric.markdown('MD Target: 1')
    metric.markdown("<h1 style='text-align: left; color: darkred; padding-left: 0px; font-size: 25px'><b>MD Target: 1<b></h1>", unsafe_allow_html=True)
else:
    #metric.markdown('MD Target: '+str(check)+' ± 0.05')
    metric.markdown("<h1 style='text-align: left; color: darkred; padding-left: 0px; font-size: 25px'><b>MD Target: "+str(check)+" ± 0.05<b></h1>", unsafe_allow_html=True)


#e.markdown(" ")

table.markdown("<h1 style='text-align: left; color: gray; padding-left: 0px; font-size: 20px'><b>MD Matrix<b></h1>", unsafe_allow_html=True)

table.plotly_chart(test)






speed = speedometer(riskTotal, check)

st.plotly_chart(speed)

##############################################################################################################################################
##############################################################################################################################################

st.markdown("<h3 style='text-align: left; color: #008080; padding-left: 0px; font-size: 40px'><b>Philosophy<b></h3>", unsafe_allow_html=True) 


with st.expander('Portfolio Philosophy and Indicator Descriptions'):

    st.markdown(' ')
    st.markdown("<h5 style='text-align: left; color: #872657; padding-left: 0px; font-size: 25px'><b>Mandate<b></h5>", unsafe_allow_html=True)
    st.markdown(' ')
    st.image(mandate)


    st.markdown(' ')
    st.markdown(' ')
    st.markdown("<h5 style='text-align: left; color: #872657; padding-left: 0px; font-size: 25px'><b>Investment Process<b></h5>", unsafe_allow_html=True)
    st.markdown(' ')
    st.image(process)


    st.markdown(' ')
    st.markdown(' ')
    st.markdown("<h5 style='text-align: left; color: #872657; padding-left: 0px; font-size: 25px'><b>Building Blocks<b></h5>", unsafe_allow_html=True)
    st.markdown(' ')
    st.image(building)

    st.markdown(' ')
    st.markdown(' ')
    st.markdown("<h3 style='text-align: left; color: #008080; padding-left: 0px; font-size: 30px'><b>Indicator Description<b></h3>", unsafe_allow_html=True) 
    st.markdown(' ')
    st.markdown("<h5 style='text-align: left; color: #872657; padding-left: 0px; font-size: 25px'><b>Economic Activity<b></h5>", unsafe_allow_html=True)
    

    st.markdown("<h6 style='text-align: left; color: #551A8B; padding-left: 0px; font-size: 20px'><b>Real GDP (Growth Expectations)<b></h6>", unsafe_allow_html=True)
    st.markdown('''<p style='font-size: 15px'>Add description</p>''', unsafe_allow_html=True)
    
    
    st.markdown(' ')
    st.markdown("<h6 style='text-align: left; color: #551A8B; padding-left: 0px; font-size: 20px'><b>CPI (Inflation Expectations)<b></h6>", unsafe_allow_html=True)
    st.markdown('''<p style='font-size: 15px'>Add description</p>''', unsafe_allow_html=True)
    
    
    st.markdown(' ')
    st.markdown("<h5 style='text-align: left; color: #551A8B; padding-left: 0px; font-size: 20px'><b>Unemployment<b></h5>", unsafe_allow_html=True)
    st.markdown('''<p style='font-size: 15px'>Add description</p>''', unsafe_allow_html=True)
    
    
    
    
    st.markdown(' ')
    st.markdown("<h5 style='text-align: left; color: #872657; padding-left: 0px; font-size: 25px'><b>System<b></h5>", unsafe_allow_html=True)
    

    st.markdown("<h5 style='text-align: left; color: #551A8B; padding-left: 0px; font-size: 20px'><b>Political<b></h5>", unsafe_allow_html=True)
    st.markdown('''<p style='font-size: 15px'>Add description</p>''', unsafe_allow_html=True)



    st.markdown(' ')
    st.markdown("<h6 style='text-align: left; color: #551A8B; padding-left: 0px; font-size: 20px'><b>Banking & Legal<b></h6>", unsafe_allow_html=True)
    st.markdown('''<p style='font-size: 15px'>Add description</p>''', unsafe_allow_html=True)


    
    st.markdown(' ')
    st.markdown("<h5 style='text-align: left; color: #872657; padding-left: 0px; font-size: 25px'><b>Policy<b></h5>", unsafe_allow_html=True)

    st.markdown("<h6 style='text-align: left; color: #551A8B; padding-left: 0px; font-size: 20px'><b>Repo Rate (Monetary)<b></h6>", unsafe_allow_html=True)
    st.markdown('''<p style='font-size: 15px'>Add description</p>''', unsafe_allow_html=True)
    
    
    st.markdown(' ')
    st.markdown("<h5 style='text-align: left; color: #551A8B; padding-left: 0px; font-size: 20px'><b>Current Account (Fiscal)<b></h5>", unsafe_allow_html=True)
    st.markdown('''<p style='font-size: 15px'>Add description</p>''', unsafe_allow_html=True)
    

    st.markdown(' ')
    st.markdown("<h5 style='text-align: left; color: #551A8B; padding-left: 0px; font-size: 20px'><b>Budget (Fiscal)<b></h5>", unsafe_allow_html=True)
    st.markdown('''<p style='font-size: 15px'>Add description</p>''', unsafe_allow_html=True)
    


    st.markdown(' ')
    st.markdown("<h5 style='text-align: left; color: #872657; padding-left: 0px; font-size: 25px'><b>Market<b></h5>", unsafe_allow_html=True)

    st.markdown(' ')
    st.markdown("<h5 style='text-align: left; color: #551A8B; padding-left: 0px; font-size: 20px'><b>10yr - 2yr Spread (US)<b></h5>", unsafe_allow_html=True)
    st.markdown('''<p style='font-size: 15px'>Add description</p>''', unsafe_allow_html=True)
    

    st.markdown(' ')
    st.markdown("<h5 style='text-align: left; color: #551A8B; padding-left: 0px; font-size: 20px'><b>Real Yields<b></h5>", unsafe_allow_html=True)
    st.markdown('''<p style='font-size: 15px'>Add description</p>''', unsafe_allow_html=True)
    

    st.markdown(' ')
    st.markdown("<h5 style='text-align: left; color: #551A8B; padding-left: 0px; font-size: 20px'><b>Commodity Prices<b></h5>", unsafe_allow_html=True)
    st.markdown('''<p style='font-size: 15px'>Add description</p>''', unsafe_allow_html=True)
    

    st.markdown(' ')
    st.markdown("<h5 style='text-align: left; color: #551A8B; padding-left: 0px; font-size: 20px'><b>ZAR/USD (Analytics Currency Decoder)<b></h5>", unsafe_allow_html=True)
    st.markdown('''<p style='font-size: 15px'>Add description</p>''', unsafe_allow_html=True)

    
    st.markdown(' ')
    st.markdown("<h5 style='text-align: left; color: #872657; padding-left: 0px; font-size: 25px'><b>References<b></h5>", unsafe_allow_html=True)
   
    st.markdown("<i style='text-align: left; color: #551A8B; padding-left: 0px; font-size: 15px'><b>The Strategic Bond Investor - https://www.amazon.com/Strategic-Bond-Investor-Third-Strategies/dp/1260473678<b></i>", unsafe_allow_html=True)
    st.markdown("<i style='text-align: left; color: #551A8B; padding-left: 0px; font-size: 15px'><b>Fixed Income Relative Value Analysis - https://www.amazon.com/Fixed-Income-Relative-Analysis-Website/dp/1118477197<b></i>", unsafe_allow_html=True)
    st.markdown("<i style='text-align: left; color: #551A8B; padding-left: 0px; font-size: 15px'><b>A Concise Guide To Macro Economics - https://www.amazon.com/Concise-Guide-Macroeconomics-Second-Executives-ebook/dp/B00IHGQVSE/ref=sr_1_1?crid=231575WJPERNY&keywords=a+concise+guide+to+macro&qid=1690888500&s=books&sprefix=a+concise+guide+to+macro+%2Cstripbooks-intl-ship%2C312&sr=1-1<b></i>", unsafe_allow_html=True)
