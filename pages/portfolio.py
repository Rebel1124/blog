import numpy as np
import pandas as pd
pd.set_option('mode.chained_assignment', None)
import streamlit as st
st.set_page_config(layout="wide")
from datetime import datetime
from datetime import timedelta
import plotly.express as px
import plotly.graph_objects as go

import scipy.optimize as optimize


from PIL import Image

#https://github.com/abhaydd22/BondMaths/blob/main/BondMaths.ipynb



#file = "Portfolio_Detailsv0.csv"
file = "Portfolio_Detailsv23112023v1.csv"


details = "Fund_Details.csv"

allLookup = "Lookup.csv"

ahy2u = "AHY2U.csv"

aig2u = "AIG2U.csv"

asn700 = "ASN700.csv"

iv246u = "IV246U.csv"

liquidity = "liquidity.csv"

subordination = "subordination.csv"

z_score = "z_score.csv"


realBonds = ['R197', 'I2025', 'R210', 'I2029', 'I2031', 'I2033', 'R202', 'I2038', 'I2046', 'I2050']

nomBonds = ['R186', 'R2030', 'R213', 'R2032', 'R2035', 'R209', 'R2037', 'R2040', 'R214', 'R2044', 'R2048', 'R2053']
nomBondsv1 = ['R186', 'R2 030', 'R213', 'R2 032', 'R2 035', 'R209', 'R2 037', 'R2 040', 'R214', 'R2 044', 'R2 048', 'R2 053']


#""" Get bond price from YTM """
#@st.cache_data
def b_price(fv, T, ytm, coup, freq=2):
    freq = float(freq)
    periods = T*freq
    coupon = coup/100*fv/freq
    dt = [(i+1)/freq for i in range(int(periods))]
    price = sum([coupon/(1+ytm/freq)**(freq*t) for t in dt]) + fv/(1+ytm/freq)**(freq*T)
    return price


#@st.cache_data
def b_ytm(price, fv, T, coup, freq=2, guess=0.05): #Semi Annual Coupon payment, hence Freq = 2.
    freq = float(freq) # Convert into Float variable
    periods = T*freq # total number of coupun payment
    coupon = coup/100*fv/freq # coupon value
    dt = [(i+1)/freq for i in range(int(periods))] # calculation of dt.
    ytm_func = lambda y: sum([coupon/(1+y/freq)**(freq*t) for t in dt]) + fv/(1+y/freq)**(freq*max(dt)) - price # YTM Function.
    return optimize.newton(ytm_func, guess) # Solving equation using newton optimization to arrive at final value. 


#""" Calculate modified duration of a bond """
#@st.cache_data
def mod_duration(price, par, T, coup, freq, dy=0.01):
    ytm = b_ytm(price, par, T, coup, freq)
    ytm_minus = ytm - dy
    price_minus = b_price(par, T, ytm_minus, coup, freq)
    ytm_plus = ytm + dy
    price_plus = b_price(par, T, ytm_plus, coup, freq)
    mduration = (price_minus-price_plus)/(2*price*dy)
    return mduration



#""" Calculate modified duration of a bond """
#@st.cache_data
def modified_duration(ytm, price, par, T, coup, freq, dy=0.01):
    #ytm = b_ytm(price, par, T, coup, freq)
    ytm_minus = ytm - dy
    price_minus = b_price(par, T, ytm_minus, coup, freq)
    ytm_plus = ytm + dy
    price_plus = b_price(par, T, ytm_plus, coup, freq)
    mduration = (price_minus-price_plus)/(2*price*dy)
    return mduration



today = datetime.today().date()

###today = pd.to_datetime('today').normalize()

#@st.cache_data
def data(file):
    df = pd.read_csv(file, delimiter=";", skipinitialspace = True)
    #df = pd.read_csv(file, delimiter=",", skipinitialspace = True)
    return df



#@st.cache_data
def dataNew(file):
    #df = pd.read_csv(file, delimiter=";", skipinitialspace = True)
    df = pd.read_csv(file, delimiter=",", skipinitialspace = True)
    return df


#@st.cache_data
def dataExcel(file):
    #df = pd.read_excel(file, header=True)
    df = pd.read_excel(file)
    #df = pd.read_csv(file, delimiter=",", skipinitialspace = True)
    return df



#@st.cache_data
def MTMRegressionQuarterly(data):

    fig = px.scatter(data, x='Years', y='YTM_Quarterly', text='InstrumentCode', trendline='ols', trendline_color_override='red')

    fig.update_traces(textposition='top center')

    results = px.get_trendline_results(fig)
    results0 = results.iloc[0]["px_fit_results"].summary()
    results1 = results.iloc[0]["px_fit_results"].params

    return fig, results0, results1



#@st.cache_data
def MTMRegressionJIBAR(data):

    fig = px.scatter(data, x='Years', y='jibarSpread', text='InstrumentCode', trendline='ols', trendline_color_override='red')

    fig.update_traces(textposition='top center')

    results = px.get_trendline_results(fig)
    results0 = results.iloc[0]["px_fit_results"].summary()
    results1 = results.iloc[0]["px_fit_results"].params

    return fig, results0, results1




#df = data(file)
df = dataNew(file)

#st.dataframe(df)
#df = dataExcel(file)
#st.dataframe(df)

df['Spread'] = df['Spread'].replace('-', 0)

dfAdd = data(details)

lookup = data(allLookup)

AHY2U = data(ahy2u)

AIG2U = data(aig2u)

ASN700 = data(asn700)

IV246U = data(iv246u)

liquidityScore = data(liquidity)

subordinationScore = data(subordination)

z_scoreScore = data(z_score)

df = df.rename(columns=lambda x: x.strip())
dfAdd = dfAdd.rename(columns=lambda x: x.strip())

lookup = lookup.rename(columns=lambda x: x.strip())
AHY2U = AHY2U.rename(columns=lambda x: x.strip())
AIG2U = AIG2U.rename(columns=lambda x: x.strip())
ASN700 = ASN700.rename(columns=lambda x: x.strip())
IV246U = IV246U.rename(columns=lambda x: x.strip())

liquidityScore = liquidityScore.rename(columns=lambda x: x.strip())
subordinationScore = subordinationScore.rename(columns=lambda x: x.strip())
z_scoreScore = z_scoreScore.rename(columns=lambda x: x.strip())


liquidityScore['Liquidity Measure'] = liquidityScore['Liquidity Measure'].apply(lambda x: float(x.split()[0].replace(',', '.')))
liquidityScore['Liquidity Measure']  = liquidityScore['Liquidity Measure'] .astype(float)

subordinationScore['subScore'] = subordinationScore['subScore'].apply(lambda x: float(x.split()[0].replace(',', '.')))
subordinationScore['subScore']  = subordinationScore['subScore'] .astype(float)

z_scoreScore['Z-Score'] = z_scoreScore['Z-Score'].apply(lambda x: float(x.split()[0].replace(',', '.')))
z_scoreScore['Z-Score']  = z_scoreScore['Z-Score'] .astype(float)



#try:
#    df['Spread'] = df['Spread'].apply(lambda x: float(x.split()[0].replace(',', '.')))
#except:
#    pass

df['Spread'] = df['Spread'].astype(float)


df['MTM'] = df['MTM'].fillna(0)
#df['MTM'] = df['MTM'].apply(lambda x: float(x.split()[0].replace('-', 0)))

#try:
#    df['MTM'] = df['MTM'].apply(lambda x: float(x.split()[0].replace(',', '.')))
#except:
#    pass

df['MTM'] = df['MTM'].astype(float)


df['Yield'] = df['Yield'].fillna(0)
#df['Yield'] = df['Yield'].apply(lambda x: float(x.split()[0].replace('-', 0)))

#try:
#    df['Yield'] = df['Yield'].apply(lambda x: float(x.split()[0].replace(',', '.')))
#except:
#    pass

df['Yield'] = df['Yield'].astype(float)


try:
    dfAdd['Z-Score'] = dfAdd['Z-Score'].apply(lambda x: float(x.split()[0].replace(',', '.')))
except:
    pass

try:
    dfAdd['EV'] = dfAdd['EV'].apply(lambda x: float(x.split()[0].replace(',', '.')))
except:
    pass

dfAdd['Z-Score'] = dfAdd['Z-Score'].astype(float)
dfAdd['EV'] = dfAdd['EV'].astype(float)
dfAdd['Weight'] = (1+dfAdd['Z-Score']) * dfAdd['EV']

#try:
#    df['HoldingNominal'] = df['HoldingNominal'].apply(lambda x: float(x.split()[0].replace(',', '.')))
#    df['AssetMarketValue'] = df['AssetMarketValue'].apply(lambda x: float(x.split()[0].replace(',', '.')))
#    df['Mod Duration'] = df['Mod Duration'].apply(lambda x: float(x.split()[0].replace(',', '.')))
#except:
#    pass


df['HoldingNominal'] = df['HoldingNominal'].astype(float)
df['AssetMarketValue'] = df['AssetMarketValue'].astype(float)
df['Mod Duration'] = df['Mod Duration'].astype(float)

###st.dataframe(df)

totalMV = df['AssetMarketValue'].sum()
df['issuerPercent'] = df['AssetMarketValue']/totalMV


AHY2Ulookup = lookup[['AHY2U', 'Issuer List', 'Sector']]
AHY2Ulookup = AHY2Ulookup.dropna()

AIG2Ulookup = lookup[['AIG2U', 'Issuer List', 'Sector']]
AIG2Ulookup = AIG2Ulookup.dropna()

ISICIN01lookup = lookup[['ISICIN01', 'Issuer List', 'Sector']]
ISICIN01lookup = ISICIN01lookup.dropna()


#st.header('Portfolio_Analytics')

#st.sidebar.header('Market Inputs')

#head1, ban1 = st.columns([1,1])

#banner2 = Image.open('AC22.png')
#st.sidebar.image(banner2)

st.sidebar.markdown("<h1 style='text-align: left; color: gray; padding-left: 0px; font-size: 40px'><b>Portfolio Inputs<b></h1>", unsafe_allow_html=True)



banner2 = Image.open('AC22.png')
st.sidebar.image(banner2)



st.sidebar.markdown("<h1 style='text-align: left; color: #008080; padding-left: 0px; font-size: 20px'><b>Market Inputs<b></h1>", unsafe_allow_html=True)

refRate = st.sidebar.number_input('3M JIBAR', value=8.35)
inflation = st.sidebar.number_input('12M Expected Inflation', value=5.4)


#st.sidebar.header('Sector Limits')
st.sidebar.markdown("<h1 style='text-align: left; color: #008080; padding-left: 0px; font-size: 20px'><b>Sector Limits<b></h1>", unsafe_allow_html=True)

financials_limit = st.sidebar.number_input('Financials', value=0.55)
insurance_limit = st.sidebar.number_input('Insurance', value=0.03)
sovereign_limit = st.sidebar.number_input('Sovereign', value=0.15)
state_limit = st.sidebar.number_input('State Owned', value=0.1)
corporate_limit = st.sidebar.number_input('Direct Corporate', value=0.095)
securitization_limit = st.sidebar.number_input('Securitization', value=0.01)
real_estate_limit = st.sidebar.number_input('Real Estate', value=0.03)
#soe_limit = 0.035
indirect_limit = st.sidebar.number_input('Indirect Corporate', value=0.035)

totalLimits = round((financials_limit + insurance_limit + sovereign_limit + state_limit + corporate_limit 
                     + securitization_limit + real_estate_limit + indirect_limit),2)


if (totalLimits == 1):
    st.sidebar.success('Sector Limit Sum = '+str('{:.0%}'.format(totalLimits)), icon="✅")
elif (totalLimits > 1):
    st.sidebar.error('Sector Limit Sum = '+str('{:.0%}'.format(totalLimits)), icon="🚨")
elif (totalLimits < 1):
    st.sidebar.warning('Sector Limit Sum = '+str('{:.0%}'.format(totalLimits)), icon="⚠️")


#st.sidebar.header('Metric Divisors')
st.sidebar.markdown("<h1 style='text-align: left; color: #008080; padding-left: 0px; font-size: 20px'><b>Metric Divisors<b></h1>", unsafe_allow_html=True)

qualityDiv = st.sidebar.number_input('Quality', value=500)
irRiskDiv = st.sidebar.number_input('Interest Rate Risk', value=0.5)
diversificationDiv = st.sidebar.number_input('Diversification Benefit', value=20)
liquityDiv = st.sidebar.number_input('Liquidity', value=10)
subordinationDiv = st.sidebar.number_input('Subordination', value=10)


#st.sidebar.header('Duration Limit')
st.sidebar.markdown("<h1 style='text-align: left; color: #008080; padding-left: 0px; font-size: 20px'><b>Duration Limits<b></h1>", unsafe_allow_html=True)

maxDur = st.sidebar.number_input('Max Duration', value=1.00)

#@st.cache_data
def grouping(data):

    count = data.shape[0]

    financials = []
    insurance = []
    sovereign = []
    state = []
    corporate = []
    securitization = []
    real_estate = []
    indirect = []

    for i in range(0,count):

        if (data['Grouping'][i] == 'financial'):
            issuer = data['Issuer'][i]
            financials.append(issuer)
        elif(data['Grouping'][i] == 'insurance'):
            issuer = data['Issuer'][i]
            insurance.append(issuer)
        elif(data['Grouping'][i] == 'sovereign'):
            issuer = data['Issuer'][i]
            sovereign.append(issuer) 
        elif(data['Grouping'][i] == 'state owned'):
            issuer = data['Issuer'][i]
            state.append(issuer) 
        elif(data['Grouping'][i] == 'corporate'):
            issuer = data['Issuer'][i]
            corporate.append(issuer) 
        elif(data['Grouping'][i] == 'securitization'):
            issuer = data['Issuer'][i]
            securitization.append(issuer) 
        elif(data['Grouping'][i] == 'real estate'):
            issuer = data['Issuer'][i]
            real_estate.append(issuer) 
        elif(data['Grouping'][i] == 'indirect'):
            issuer = data['Issuer'][i]
            indirect.append(issuer)  

    return financials, insurance, sovereign, state, corporate, securitization, real_estate, indirect


financials, insurance, sovereign, state, corporate, securitization, real_estate, indirect = grouping(dfAdd)


#@st.cache_data
def sectorSum(data):

    count = data.shape[0]

    financialsSum = 0
    insuranceSum = 0
    sovereignSum = 0
    stateSum = 0
    corporateSum = 0
    securitizationSum = 0
    real_estateSum = 0
    indirectSum = 0

    for i in range(0,count):

        if (data['Grouping'][i] == 'financial'):
            val = data['Weight'][i]
            financialsSum += val
        elif(data['Grouping'][i] == 'insurance'):
            val = data['Weight'][i]
            insuranceSum += val
        elif(data['Grouping'][i] == 'sovereign'):
            val = data['Weight'][i]
            sovereignSum += val
        elif(data['Grouping'][i] == 'state owned'):
            val = data['Weight'][i]
            stateSum+= val
        elif(data['Grouping'][i] == 'corporate'):
            val = data['Weight'][i]
            corporateSum += val
        elif(data['Grouping'][i] == 'securitization'):
            val = data['Weight'][i]
            securitizationSum += val
        elif(data['Grouping'][i] == 'real estate'):
            val = data['Weight'][i]
            real_estateSum+= val
        elif(data['Grouping'][i] == 'indirect'):
            val = data['Weight'][i]
            indirectSum += val
    
    
    if(financialsSum > 0):
        financialsSum = financialsSum
    else:
        financialsSum = len(data[data['Grouping']=='financial'])
    
    if(insuranceSum > 0):
        insuranceSum = insuranceSum
    else:
        insuranceSum = len(data[data['Grouping']=='insurance'])

    if(sovereignSum> 0):
        sovereignSum = sovereignSum
    else:
        sovereignSum = len(data[data['Grouping']=='sovereign'])

    if(stateSum > 0):
        stateSum = stateSum
    else:
        stateSum = len(data[data['Grouping']=='state owned'])

    if(corporateSum > 0):
        corporateSum = corporateSum
    else:
        corporateSum = len(data[data['Grouping']=='corporate'])

    if(securitizationSum > 0):
        securitizationSum = securitizationSum
    else:
        securitizationSum = len(data[data['Grouping']=='securitization'])
    
    if(real_estateSum > 0):
        real_estateSum = real_estateSum
    else:
        real_estateSum = len(data[data['Grouping']=='real estate'])

    if(indirectSum > 0):
        indirectSum = indirectSum
    else:
        indirectSum = len(data[data['Grouping']=='indirect'])
       
    return financialsSum, insuranceSum, sovereignSum, stateSum, corporateSum, securitizationSum, real_estateSum, indirectSum


financialsSum, insuranceSum, sovereignSum, stateSum, corporateSum, securitizationSum, real_estateSum, indirectSum = sectorSum(dfAdd)

#@st.cache_data
def finalWeight(data):

    count = data.shape[0]

    finalWeight = []

    for i in range(0,count):

        if (data['Grouping'][i] == 'financial'):
            weight = (data['Weight'][i]/financialsSum)*financials_limit
            finalWeight.append(weight)
        elif(data['Grouping'][i] == 'insurance'):
            weight = (data['Weight'][i]/insuranceSum)*insurance_limit
            finalWeight.append(weight)
        elif(data['Grouping'][i] == 'sovereign'):
            weight = (data['Weight'][i]/sovereignSum)*sovereign_limit
            finalWeight.append(weight)
        elif(data['Grouping'][i] == 'state owned'):
            weight = (data['Weight'][i]/stateSum)*state_limit
            finalWeight.append(weight)
        elif(data['Grouping'][i] == 'corporate'):
            weight = (data['Weight'][i]/corporateSum)*corporate_limit
            finalWeight.append(weight)
        elif(data['Grouping'][i] == 'securitization'):
            weight = (data['Weight'][i]/securitizationSum)*securitization_limit
            finalWeight.append(weight)
        elif(data['Grouping'][i] == 'real estate'):
            weight = (data['Weight'][i]/real_estateSum)*real_estate_limit
            finalWeight.append(weight)
        elif(data['Grouping'][i] == 'indirect'):
            weight = (data['Weight'][i]/indirectSum)*indirect_limit
            finalWeight.append(weight)

    return finalWeight


dfAdd['Final'] = finalWeight(dfAdd)


#@st.cache_data
def ytm(data):

    lenth = data.shape[0]

    yieldToMaturity = []

    for i in range(0,lenth):

        if(data['Companion'].iloc[i] == 'R197'):
            ytm =  data['MTM'].iloc[i] + (inflation)
            yieldToMaturity.append(ytm)

        elif(data['Companion'].iloc[i] == 'I2025'):
            ytm =  data['MTM'].iloc[i] + (inflation)
            yieldToMaturity.append(ytm)


        elif(data['Companion'].iloc[i] == 'R210'):
            ytm =  data['MTM'].iloc[i] + (inflation)
            yieldToMaturity.append(ytm)

        elif(data['Companion'].iloc[i] == 'I2029'):
            ytm =  data['MTM'].iloc[i] + (inflation)
            yieldToMaturity.append(ytm)

        elif(data['Companion'].iloc[i] == 'I2029'):
            ytm =  data['MTM'].iloc[i] + (inflation)
            yieldToMaturity.append(ytm)


        elif(data['Companion'].iloc[i] == 'R2031'):
            ytm =  data['MTM'].iloc[i] + (inflation)
            yieldToMaturity.append(ytm)

        elif(data['Companion'].iloc[i] == 'R2033'):
            ytm =  data['MTM'].iloc[i] + (inflation)
            yieldToMaturity.append(ytm)


        elif(data['Companion'].iloc[i] == 'R202'):
            ytm =  data['MTM'].iloc[i] + (inflation)
            yieldToMaturity.append(ytm)

        elif(data['Companion'].iloc[i] == 'I2038'):
            ytm =  data['MTM'].iloc[i] + (inflation)
            yieldToMaturity.append(ytm)


        elif(data['Companion'].iloc[i] == 'I2046'):
            ytm =  data['MTM'].iloc[i] + (inflation)
            yieldToMaturity.append(ytm)

        elif(data['Companion'].iloc[i] == 'I2050'):
            ytm =  data['MTM'].iloc[i] + (inflation)
            yieldToMaturity.append(ytm)




        elif(data['InstrumentCode'].iloc[i] == "IBL224"):
            #ytm = (data['Spread'].iloc[i]/100) + refRate
            ytm = data['Yield'].iloc[i]
            yieldToMaturity.append(ytm)

        elif(data['InstrumentCode'].iloc[i] == "ASN863"):
            #ytm = (data['Spread'].iloc[i]/100) + refRate
            ytm = data['Yield'].iloc[i]
            yieldToMaturity.append(ytm)


        elif(data['InstrumentCode'].iloc[i] == "FRS329"):
            #ytm = (data['Spread'].iloc[i]/100) + refRate
            ytm = data['Yield'].iloc[i]
            yieldToMaturity.append(ytm)

        elif(data['InstrumentCode'].iloc[i] == "IBL235"):
            #ytm = (data['Spread'].iloc[i]/100) + refRate
            ytm = data['Yield'].iloc[i]
            yieldToMaturity.append(ytm)

        elif(data['InstrumentCode'].iloc[i] == "IBL208"):
            #ytm = (data['Spread'].iloc[i]/100) + refRate
            ytm = data['Yield'].iloc[i]
            yieldToMaturity.append(ytm)


        elif(data['InstrumentCode'].iloc[i] == "I2025"):
            #ytm = (data['Spread'].iloc[i]/100) + refRate
            ytm = data['MTM'].iloc[i] + (inflation)
            yieldToMaturity.append(ytm)


        elif(data['Companion'].iloc[i] == 'JIBAR'):
            ytm = (data['Spread'].iloc[i]/100) + refRate
            yieldToMaturity.append(ytm)

        else:
            ytm = data['MTM'].iloc[i]

            yieldToMaturity.append(ytm)
        
    return yieldToMaturity


df['YTM'] = ytm(df)

#@st.cache_data
def ytmQuarterly(data):

    lenth = data.shape[0]

    ytmQuarterly = []

    for i in range(0,lenth):

        if((data['Companion'].iloc[i] == 'JIBAR')):
            ytmQ = round((data['YTM'].iloc[i])*1,2)
            ytmQuarterly.append(ytmQ)

        else:
            ytmQ = round((((((1+((data['YTM'].iloc[i])/200))**(2/4)) - 1)*400))*1,4)
            ytmQuarterly.append(ytmQ)
    
    return ytmQuarterly


df['YTM_Quarterly'] = ytmQuarterly(df)



#@st.cache_data
def jibarSpread(data):

    lenth = data.shape[0]

    jibarSpread = []

    for i in range(0,lenth):

        if(data['Companion'].iloc[i] == 'JIBAR'):
            spread = round((data['YTM'].iloc[i] - refRate)*100,2)
            jibarSpread.append(spread)

        else:
            spread = round((((((1+((data['YTM'].iloc[i])/200))**(2/4)) - 1)*400) - refRate)*100,2)
            jibarSpread.append(spread)
    
    return jibarSpread

df['jibarSpread'] = jibarSpread(df)


#@st.cache_data
def mDuration(data):

    lenth = data.shape[0]

    duration = []

    for i in range(0,lenth):

        if ((data['Type'][i] == 'Call Account') or (data['Type'][i] == 'Money Market CIS')):
            md = float(0.00)
            duration.append(md)
        elif ((data['Type'][i] == 'Money Market') and (data['Reference'][i] == 'JIBAR')):
            md = float(0.25)
            duration.append(md)

        elif ((data['Type'][i] == 'Step-Up Notes')):
            md = float(0.25)
            duration.append(md)
        elif ((data['Type'][i] == 'Money Market') and (data['Reference'][i] == 'FIXED')):
            ytm1 = (data['YTM'][i])*0.01
            price = ((data['AssetMarketValue'][i]/data['HoldingNominal'][i]))*100
            par = (data['HoldingNominal'][i]/data['HoldingNominal'][i])*100
            T = data['Years'][i]
            coup = data['MTM'][i]
            freq=2
            md = modified_duration(ytm1, price, par, T, coup, freq, dy=0.01)
            duration.append(md)
        elif ((data['Type'][i] == 'Treasury Bills')):
            ytm1 = (data['YTM'][i])*0.01
            price = ((data['AssetMarketValue'][i]/data['HoldingNominal'][i]))*100
            par = (data['HoldingNominal'][i]/data['HoldingNominal'][i])*100
            T = data['Years'][i]
            coup = data['MTM'][i]
            freq=2
            md = modified_duration(ytm1, price, par, T, coup, freq, dy=0.01)
            duration.append(md)
        else:
            md = data['Mod Duration'][i]
            duration.append(md)

    return duration

AHY2U_val = df.loc[df['InstrumentCode'] == 'AHY2U']['AssetMarketValue'].sum()
AIG2U_val = df.loc[df['InstrumentCode'] == 'AIG2U']['AssetMarketValue'].sum()
ASN700_val = df.loc[df['InstrumentCode'] == 'ASN700']['AssetMarketValue'].sum()
IV246U_val = df.loc[df['InstrumentCode'] == 'IV246U']['AssetMarketValue'].sum()


AHY2U = AHY2U[['AHY2U', 'Current Valuation']]
AHY2U['Current Valuation'] = AHY2U['Current Valuation'].apply(lambda x: float(x.split()[0].replace(',', '.')))
AHY2U = AHY2U.loc[AHY2U['Current Valuation'] > 0]
AHY2U = AHY2U.merge(AHY2Ulookup, how='left', on='AHY2U')
AHY2U = AHY2U.drop(['AHY2U'], axis=1, errors='ignore')
AHY2U_tot = AHY2U['Current Valuation'].sum()
AHY2U['percentHolding'] = AHY2U['Current Valuation']/AHY2U_tot
AHY2U['ExposureValue'] = AHY2U['percentHolding']*AHY2U_val


AIG2U = AIG2U[['AIG2U', 'Current Valuation']]
AIG2U['Current Valuation'] = AIG2U['Current Valuation'].apply(lambda x: float(x.split()[0].replace(',', '.')))
AIG2U = AIG2U.loc[AIG2U['Current Valuation'] > 0]
AIG2U = AIG2U.merge(AIG2Ulookup, how='left', on='AIG2U')
AIG2U = AIG2U.drop(['AIG2U'], axis=1, errors='ignore')
AIG2U_tot = AIG2U['Current Valuation'].sum()
AIG2U['percentHolding'] = AIG2U['Current Valuation']/AIG2U_tot
AIG2U['ExposureValue'] = AIG2U['percentHolding']*AIG2U_val


ASN700['Weight'] = ASN700['Weight'].apply(lambda x: float(x.split()[0].replace(',', '.')))
ASN700['ExposureValue'] = ASN700['Weight']*ASN700_val
ASN700 = ASN700[['ExposureValue', 'Issuer Exposure', 'Sector', 'Weight']]

IV246U['Weight'] = IV246U['Weight'].apply(lambda x: float(x.split()[0].replace(',', '.')))
IV246U['ExposureValue'] = IV246U['Weight']*IV246U_val
IV246U = IV246U[['ExposureValue', 'Issuer Exposure', 'Weight']]

dfIssuer = df[['Issuer', 'AssetMarketValue', 'issuerPercent']]

instrumentIssuerType = dfIssuer.groupby(['Issuer']).sum()

instrumentIssuerType['Issuer'] = instrumentIssuerType.index

instrumentIssuerType = instrumentIssuerType.reset_index(drop=True)

instrumentIssuerType.rename(columns={'AssetMarketValue': 'issuerMarketValue'}, inplace=True)

dfExposure = df[['Exposure', 'AssetMarketValue', 'issuerPercent']]

instrumentExposureType = dfExposure.groupby(['Exposure']).sum()

instrumentExposureType['Issuer'] = instrumentExposureType.index

instrumentExposureType = instrumentExposureType.reset_index(drop=True)

instrumentExposureType.rename(columns={'AssetMarketValue': 'exposureMarketValue', 'issuerPercent': 'exposurePercent'}, inplace=True)


exposure = pd.merge(instrumentIssuerType,
              instrumentExposureType,
              on ='Issuer',
              how ='inner')


#@st.cache_data
def exposureAdjustment(data, ahy2uDF, aig2uDF, asn700DF, iv246uDF):

    count = data.shape[0]

    exposureVal = []

    for name in range(0,count):

        if (data['Issuer'][name] == 'ABSA BANK LTD'):
            exp =  (data['exposureMarketValue'][name] - ASN700_val + ahy2uDF.loc[ahy2uDF['Issuer List'] == 'ABSA BANK LTD']['ExposureValue'].sum()+ aig2uDF.loc[aig2uDF['Issuer List'] == 'ABSA BANK LTD']['ExposureValue'].sum() + asn700DF.loc[asn700DF['Issuer Exposure'] == 'ABSA BANK LTD']['ExposureValue'].sum() + iv246uDF.loc[iv246uDF['Issuer Exposure'] == 'ABSA BANK LTD']['ExposureValue'].sum())


        elif (data['Issuer'][name] == 'INVESTEC BANK LTD'):
            exp =  (data['exposureMarketValue'][name] - IV246U_val + ahy2uDF.loc[ahy2uDF['Issuer List'] == 'INVESTEC BANK LTD']['ExposureValue'].sum() + aig2uDF.loc[aig2uDF['Issuer List'] == 'INVESTEC BANK LTD']['ExposureValue'].sum() + asn700DF.loc[asn700DF['Issuer Exposure'] == 'INVESTEC BANK LTD']['ExposureValue'].sum() + iv246uDF.loc[iv246uDF['Issuer Exposure'] == 'INVESTEC BANK LTD']['ExposureValue'].sum())

        elif (data['Issuer'][name]== 'ASHBURTON'):
            exp =  (data['exposureMarketValue'][name] - AHY2U_val - AIG2U_val + ahy2uDF.loc[ahy2uDF['Issuer List'] == 'ASHBURTON']['ExposureValue'].sum() + aig2uDF.loc[aig2uDF['Issuer List'] == 'ASHBURTON']['ExposureValue'].sum() + asn700DF.loc[asn700DF['Issuer Exposure'] == 'ASHBURTON']['ExposureValue'].sum() + iv246uDF.loc[iv246uDF['Issuer Exposure'] == 'ASHBURTON']['ExposureValue'].sum())

        else:
            exp =  (data['exposureMarketValue'][name] + ahy2uDF.loc[ahy2uDF['Issuer List'] == data['Issuer'][name]]['ExposureValue'].sum() + aig2uDF.loc[aig2uDF['Issuer List'] == data['Issuer'][name]]['ExposureValue'].sum() + asn700DF.loc[asn700DF['Issuer Exposure'] == data['Issuer'][name]]['ExposureValue'].sum() + iv246uDF.loc[iv246uDF['Issuer Exposure'] == data['Issuer'][name]]['ExposureValue'].sum())

        exposureVal.append(exp)

    return exposureVal


exposure['ExposureValue'] = exposureAdjustment(exposure, AHY2U, AIG2U, ASN700, IV246U)

exposure = exposure.drop(['exposureMarketValue', 'exposurePercent'], axis=1, errors='ignore')



df_final = pd.merge(dfAdd,
              exposure,
              on ='Issuer',
              how ='left')


df_final = df_final.fillna(0)



#@st.cache_data
def allExposure(data, ahy2uDF, aig2uDF, asn700DF, iv246uDF):

    count = data.shape[0]

    exposureVal = []

    for name in range(0,count):

        if (data['ExposureValue'][name] == 0):
            exp =  (ahy2uDF.loc[ahy2uDF['Issuer List'] == data['Issuer'][name]]['ExposureValue'].sum()+ aig2uDF.loc[aig2uDF['Issuer List'] == data['Issuer'][name]]['ExposureValue'].sum() + asn700DF.loc[asn700DF['Issuer Exposure'] == data['Issuer'][name]]['ExposureValue'].sum() + iv246uDF.loc[iv246uDF['Issuer Exposure'] == data['Issuer'][name]]['ExposureValue'].sum())


        else:
            exp =  (data['ExposureValue'][name])

        exposureVal.append(exp)

    return exposureVal


df_final['exposureMarketValue'] = allExposure(df_final, AHY2U, AIG2U, ASN700, IV246U)


df_final = df_final.drop(['ExposureValue'], axis=1, errors='ignore')

exposure_val = df_final['exposureMarketValue'].sum()

df_final['exposurePercent'] = df_final['exposureMarketValue']/exposure_val

df_final['Active'] = df_final['exposurePercent'] - df_final['Final']

df_final['HHI Index'] = ((df_final['exposurePercent']*100)**2)/1000

profile = df.copy()

#st.dataframe(df)

profile['Maturity'] = profile.apply(lambda x: datetime.strptime(x['Maturity'], "%Y/%m/%d").date(), axis=1)
profile['Months'] = profile.apply(lambda x: ((x['Maturity'] - today).days)/30.5, axis=1)



##@st.cache_data
#def term(data):
#
#    count = data.shape[0]
#
#    maturityTerm = []
#
#    for i in range(0,count):
#
#        if(data['Months'][i] <= 0):
#            t = 0
#        elif(data['Months'][i] <= 1):
#            t = 1
#        elif(data['Months'][i] <= 2):
#            t = 2
#        elif(data['Months'][i] <= 3):
#            t = 3
#        elif(data['Months'][i] <= 4):
#            t = 4
#        elif(data['Months'][i] <= 5):
#            t = 5
#        elif(data['Months'][i] <= 6):
#            t = 6
#        elif(data['Months'][i] <= 7):
#            t = 7
#        elif(data['Months'][i] <= 8):
#            t = 8
#        elif(data['Months'][i] <= 9):
#            t = 9
#        elif(data['Months'][i] <= 10):
#            t = 10
#        elif(data['Months'][i] <= 11):
#            t = 11
#        elif(data['Months'][i] <= 12):
#            t = 12
#        elif(data['Months'][i] <= 15):
#            t = 15
#        elif(data['Months'][i] <= 18):
#            t = 18
#        elif(data['Months'][i] <= 21):
#            t = 21
#        elif(data['Months'][i] <= 24):
#            t = 24
#        elif(data['Months'][i] <= 36):
#            t = 36
#        elif(data['Months'][i] <= 48):
#            t = 48
#        elif(data['Months'][i] <= 60):
#            t = 60
#        else:
#            t = '>60'
#
#        maturityTerm.append(t)
#
#    return maturityTerm



#@st.cache_data
def term(data, criteria):

    count = data.shape[0]

    maturityTerm = []

    for i in range(0,count):

        if(data[criteria][i] <= 0):
            t = 0
        elif(data[criteria][i] <= 1):
            t = 1
        elif(data[criteria][i] <= 2):
            t = 2
        elif(data[criteria][i] <= 3):
            t = 3
        elif(data[criteria][i] <= 4):
            t = 4
        elif(data[criteria][i] <= 5):
            t = 5
        elif(data[criteria][i] <= 6):
            t = 6
        elif(data[criteria][i] <= 7):
            t = 7
        elif(data[criteria][i] <= 8):
            t = 8
        elif(data[criteria][i] <= 9):
            t = 9
        elif(data[criteria][i] <= 10):
            t = 10
        elif(data[criteria][i] <= 11):
            t = 11
        elif(data[criteria][i] <= 12):
            t = 12
        elif(data[criteria][i] <= 15):
            t = 15
        elif(data[criteria][i] <= 18):
            t = 18
        elif(data[criteria][i] <= 21):
            t = 21
        elif(data[criteria][i] <= 24):
            t = 24
        elif(data[criteria][i] <= 36):
            t = 36
        elif(data[criteria][i] <= 48):
            t = 48
        elif(data[criteria][i] <= 60):
            t = 60
        else:
            #t = '>60'
            t=120

        maturityTerm.append(t)

    return maturityTerm







profile['Bucket'] = term(profile, 'Months')

profile = profile[['AssetMarketValue', 'issuerPercent', 'Bucket']]

yearlyProfile = df.copy()

yearlyProfile['Maturity'] = yearlyProfile.apply(lambda x: datetime.strptime(x['Maturity'], "%Y/%m/%d").date(), axis=1)
yearlyProfile['Months'] = yearlyProfile.apply(lambda x: ((x['Maturity'] - today).days)/30.5, axis=1)

##@st.cache_data
#def yearlyTerm(data):
#
#    count = data.shape[0]
#
#    maturityTerm = []
#
#    for i in range(0,count):
#
#        if(data['Months'][i] <= 3):
#            t = 3
#        elif(data['Months'][i] <= 6):
#            t = 6
#        elif(data['Months'][i] <= 12):
#            t = 12
#        elif(data['Months'][i] <= 24):
#            t = 24
#        elif(data['Months'][i] <= 36):
#            t = 36
#        elif(data['Months'][i] <= 48):
#            t = 48
#        elif(data['Months'][i] <= 60):
#            t = 60
#        elif(data['Months'][i] <= 72):
#            t = 72
#        elif(data['Months'][i] <= 84):
#            t = 84
#        elif(data['Months'][i] <= 96):
#            t = 96
#        elif(data['Months'][i] <= 108):
#            t = 108
#        else:
#            t = 120
#        maturityTerm.append(t)
#
#    return maturityTerm



#@st.cache_data
def yearlyTerm(data, criteria):

    count = data.shape[0]

    maturityTerm = []

    for i in range(0,count):

        if(data[criteria][i] <= 3):
            t = 3
        elif(data[criteria][i] <= 6):
            t = 6
        elif(data[criteria][i] <= 12):
            t = 12
        elif(data[criteria][i] <= 24):
            t = 24
        elif(data[criteria][i] <= 36):
            t = 36
        elif(data[criteria][i] <= 48):
            t = 48
        elif(data[criteria][i] <= 60):
            t = 60
        elif(data[criteria][i] <= 72):
            t = 72
        elif(data[criteria][i] <= 84):
            t = 84
        elif(data[criteria][i] <= 96):
            t = 96
        elif(data[criteria][i] <= 108):
            t = 108
        else:
            t = 120


        maturityTerm.append(t)

    return maturityTerm





yearlyProfile['summaryBucket'] = yearlyTerm(yearlyProfile, 'Months')

yearlyProfile = yearlyProfile[['AssetMarketValue', 'issuerPercent', 'summaryBucket']]

#def cumYearlyTerm(data):


 

###########Tables and Graphs############################################
########################################################################
##st.dataframe(df)

instrumentType = df.groupby('Issuer Type').sum()

instrumentType = instrumentType.sort_values(by='AssetMarketValue', ascending=False)

debtType = df.groupby('Type').sum()
debtType = debtType.sort_values(by='AssetMarketValue', ascending=False)



#@st.cache_data
def bankGoviLiquid(data):

    count = data.shape[0]

    bankMV = 0
    goviMV = 0
    liquidMV = 0

    bank = 0
    govi = 0
    liquid = 0

    for i in range(0,count):

        if(data.index[i] == 'Bank Senior Debt - Floating'):
            bank += data['issuerPercent'][i]
            bankMV += data['AssetMarketValue'][i]
        elif(data.index[i] == 'Bank Senior Debt - Fixed'):
            bank += data['issuerPercent'][i]
            bankMV += data['AssetMarketValue'][i]
        elif(data.index[i] == 'Bank Senior Debt - ILBs'):
            bank += data['issuerPercent'][i]
            bankMV += data['AssetMarketValue'][i]
        elif(data.index[i] == 'Bank Subordinated Debt - Tier 2'):
            bank += data['issuerPercent'][i]
            bankMV += data['AssetMarketValue'][i]
        elif(data.index[i] == 'Bank Subordinated Debt - AT1'):
            bank += data['issuerPercent'][i]
            bankMV += data['AssetMarketValue'][i]
        elif(data.index[i] == 'Money Market'):
            bank += data['issuerPercent'][i]
            bankMV += data['AssetMarketValue'][i]
            liquid += data['issuerPercent'][i]
            liquidMV += data['AssetMarketValue'][i]
        elif(data.index[i] == 'Money Market CIS'):
            bank += data['issuerPercent'][i]
            bankMV += data['AssetMarketValue'][i]
            liquid += data['issuerPercent'][i]
            liquidMV += data['AssetMarketValue'][i]
        elif(data.index[i] == 'Call Account'):
            bank += data['issuerPercent'][i]
            bankMV += data['AssetMarketValue'][i]
            liquid += data['issuerPercent'][i]
            liquidMV += data['AssetMarketValue'][i]
        elif(data.index[i] == 'Treasury Bills'):
            govi += data['issuerPercent'][i]
            goviMV += data['AssetMarketValue'][i]
            liquid += data['issuerPercent'][i]
            liquidMV += data['AssetMarketValue'][i]
        elif(data.index[i] == 'Govis'):
            govi += data['issuerPercent'][i]
            goviMV += data['AssetMarketValue'][i]
        elif(data.index[i] == 'ILBs'):
            govi += data['issuerPercent'][i]
            goviMV += data['AssetMarketValue'][i]

    return bankMV, goviMV, liquidMV, bank, govi, liquid


bankMV, goviMV, liquidMV, bank, govi, liquid = bankGoviLiquid(debtType)

referenceType = df.groupby('Reference').sum()
referenceType = referenceType.sort_values(by='AssetMarketValue', ascending=False)


def refCheck(data):

    overnightMV = 0
    jibarMV = 0
    invJIBARMV = 0
    mm_fixedMV = 0

    overnight = 0
    jibar = 0
    invJIBAR = 0
    mm_fixed = 0


    inflationBonds = data.loc[(data.index.isin(realBonds))]
    nominalBonds = data.loc[(data.index.isin(nomBonds))]

    bond_realMV = inflationBonds['AssetMarketValue'].sum()
    bond_real = inflationBonds['issuerPercent'].sum()


    bond_fixedMV = nominalBonds['AssetMarketValue'].sum()
    bond_fixed = nominalBonds['issuerPercent'].sum()

    count = data.shape[0]

    for i in range(0,count):
        if (data.index[i] == 'JIBAR'):
            jibarMV += data['AssetMarketValue'][i]
            jibar += data['issuerPercent'][i]
        elif (data.index[i] == 'INV JIBAR'):
            invJIBARMV += data['AssetMarketValue'][i]
            invJIBAR += data['issuerPercent'][i]
        elif (data.index[i] == 'OVERNIGHT'):
            overnightMV += data['AssetMarketValue'][i]
            overnight += data['issuerPercent'][i]            
        elif(data.index[i] == 'FIXED'):
            mm_fixedMV += data['AssetMarketValue'][i]
            mm_fixed += data['issuerPercent'][i]  


    totalMV = overnightMV + jibarMV + mm_fixedMV + bond_fixedMV + bond_realMV + invJIBARMV
    total = overnight + jibar + mm_fixed + bond_fixed + bond_real + invJIBAR




    head = ['<b>Reference<b>', '<b>Market Value<b>', '<b>% (MV)<b>']

    metric = ['<b>Overnight<b>', '<b>JIBAR<b>', '<b>Inverse JIBAR<b>', '<b>Fixed MM<b>', '<b>Fixed Bond<b>', '<b>Real Bond<b>', '<b>Total<b>']

    refMV = ['{:,.2f}'.format(overnightMV), '{:,.2f}'.format(jibarMV), '{:,.2f}'.format(invJIBARMV), '{:,.2f}'.format(mm_fixedMV),
             '{:,.2f}'.format(bond_fixedMV), '{:,.2f}'.format(bond_realMV), '<b>{:,.2f}<b>'.format(totalMV)]

    ref = ['{:.2%}'.format(overnight), '{:.2%}'.format(jibar), '{:.2%}'.format(invJIBAR), '{:.2%}'.format(mm_fixed),
           '{:.2%}'.format(bond_fixed), '{:.2%}'.format(bond_real), '<b>{:.2%}<b>'.format(total)]

    palette0 = px.colors.qualitative.Set3

    #colors = ['white', 'lightgray', 'white', 'lightgray', 'white', 'lightgray']
    colors = ['white', palette0[1], 'white', palette0[1], 'white', palette0[1], palette0[10]]

    headerColor = palette0[11]

    fig = go.Figure(data=[go.Table(
        
        columnorder = [1,2,3,4],
        columnwidth = [35,35,35, 35],
        
        header=dict(values=head,
                    fill_color=headerColor,
                    font=dict(color='black'),
                    line_color='darkslategray',
                    align=['left', 'center', 'center']),
        cells=dict(values=[metric, refMV, ref],
                   fill_color=[colors*3],
                   line_color='darkslategray',
                   font=dict(color='black'),
                   align=['left', 'center', 'center']))
    ])   

    fig.update_layout(height=250, width=350, margin=dict(l=2, r=2, b=0,t=2))

    names = ['Overnight', 'JIBAR', 'Inverse JIBAR', 'Fixed MM', 'Fixed Bond', 'Real Bond']
    vals = [overnightMV, jibarMV, invJIBARMV, mm_fixedMV, bond_fixedMV, bond_realMV]
    #dta = {'Ref': names, 'Val': refMV[:-1]}
    dta = {'Ref': names, 'Val': vals}
    dummyDataFrame = pd.DataFrame(data=dta)


    #colors1 = ['gold', 'mediumturquoise', 'darkorange', 'lightgreen']
    #
    #figPie = go.Figure(data=[go.Pie(labels=metric,
    #                         values=refMV)])
    #figPie.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
    #              marker=dict(line=dict(color='darkgray', width=1)))
    
    return fig, dummyDataFrame


infrastructureType = df.groupby('Infrastructure').sum()
infrastructureType = infrastructureType.sort_values(by='AssetMarketValue', ascending=False)

bucket = profile.groupby('Bucket').sum()

#st.markdown(bucket.iloc[0])
#

#st.dataframe(bucket.index)
#st.markdown(bucket["AssetMarketValue"][0])


summaryBucket= yearlyProfile.groupby('summaryBucket').sum()

#st.dataframe(summaryBucket)

sectorClean = df_final[['Sector', 'exposureMarketValue', 'exposurePercent']]
sectorType = sectorClean.groupby('Sector').sum()
sectorType = sectorType.sort_values(by='exposureMarketValue', ascending=False)


df['Maturity'] = df.apply(lambda x: datetime.strptime(x['Maturity'], "%Y/%m/%d").date(), axis=1)
df['Days'] = df.apply(lambda x: ((x['Maturity'] - today).days), axis=1)
df['Months'] = df.apply(lambda x: ((x['Maturity'] - today).days)/30.5, axis=1)
df['Years'] = df.apply(lambda x: ((x['Maturity'] - today).days)/365, axis=1)

df['MD'] = mDuration(df)
df['mdMonths'] = df['MD'] * 12

df['irScore'] = (maxDur - df['MD'])**(-1)

#@st.cache_data
def riskIndicator(data):

    count = data.shape[0]

    indicator = []

    for i in range(0,count):
        if((data['Reference'][i] == 'JIBAR') or (data['Reference'][i] == 'FIXED') or (data['Reference'][i] == 'OVERNIGHT')):
            risk = 0
            indicator.append(risk)
        else:
            risk = 1
            indicator.append(risk)
    return(indicator)

df['riskIndicator'] = riskIndicator(df)


df['Risk_Duration'] = df['riskIndicator'] * df['MD']

merged1 = pd.merge(df, liquidityScore, on='Issuer', how='left')

merged2 = pd.merge(merged1, z_scoreScore, on='Issuer', how='left')

merged3 = pd.merge(merged2, subordinationScore, on='Level of Subordination', how='left')



merged3['mdBucket1'] = term(merged3, 'mdMonths')
merged3['mdBucket2'] = yearlyTerm(merged3, 'mdMonths')


#@st.cache_data
def sumProduct(data, x, y):

    data['z'] = data[x] * data[y]
    val = data['z'].sum()
    data = data.drop(['z'], axis=1, errors='ignore')
    return val


qualityScore = sumProduct(merged3, 'issuerPercent', 'Z-Score') * -1

liquidityScore = sumProduct(merged3, 'issuerPercent', 'Liquidity Measure')

subordinationScore = sumProduct(merged3, 'issuerPercent', 'subScore')

diversificationScore = df_final['HHI Index'].sum()

mdVal = sumProduct(merged3, 'issuerPercent', 'Mod Duration')
mdVal1 = (maxDur - mdVal)

if (mdVal < maxDur):
    st.sidebar.success('Portfolio MD = '+str('{:.2f}'.format(mdVal)), icon="✅")
elif (mdVal >= maxDur):
    st.sidebar.error('Portfolio MD = '+str('{:.2f}'.format(mdVal)), icon="🚨")



if(mdVal1 > 0):
    mdScore = mdVal1**(-1)
else:
    mdScore = 200

unadjustedVal = qualityScore + liquidityScore + subordinationScore + diversificationScore + mdScore

qualityScoreAdj = qualityScore * qualityDiv
liquidityScoreAdj = liquidityScore * liquityDiv
subordinationScoreAdj = subordinationScore * subordinationDiv
diversificationScoreAdj = diversificationScore * diversificationDiv
mdScoreAdj = mdScore * irRiskDiv

adjustedVal = qualityScoreAdj + liquidityScoreAdj + subordinationScoreAdj + diversificationScoreAdj + mdScoreAdj


#riskDurationVal = sumProduct(merged3, 'issuerPercent', 'Risk_Duration')
riskDurationVal = sumProduct(merged3, 'issuerPercent', 'Risk Duration')

weightedTerm = sumProduct(merged3, 'issuerPercent', 'Years')


avgYield= sumProduct(merged3, 'issuerPercent', 'YTM')


avgQYield= sumProduct(merged3, 'issuerPercent', 'YTM_Quarterly')

avgCalcSpread= (avgYield - refRate)*100


avgSpread= sumProduct(merged3, 'issuerPercent', 'jibarSpread')


score = (avgSpread/adjustedVal)


#@st.cache_data
def tableScores(qualityScore, liquidityScore, subordinationScore, diversificationScore, mdScore,
               qualityScoreAdj, liquidityScoreAdj, subordinationScoreAdj, diversificationScoreAdj, mdScoreAdj,
               qualityDiv, liquityDiv, subordinationDiv, diversificationDiv, irRiskDiv,
               unadjustedVal, adjustedVal):
    

    head = ['<b>Metric<b>', '<b>Divisor<b>', '<b>Unadjusted Value<b>', '<b>Adjusted Value<b>']

    metric = ['<b>Quality<b>', '<b>Liquidity<b>', '<b>Subordination<b>', '<b>Diversification<b>', '<b>IR Risk<b>', '<b>Aggregate<b>']

    divisor = [qualityDiv, liquityDiv, subordinationDiv, diversificationDiv, irRiskDiv, '-']

    unadjusted = ['{:.2f}'.format(qualityScore), '{:.2f}'.format(liquidityScore), '{:.2f}'.format(subordinationScore), '{:.2f}'.format(diversificationScore), '{:.2f}'.format(mdScore), '{:.2f}'.format(unadjustedVal)]

    adjusted = ['{:.2f}'.format(qualityScoreAdj), '{:.2f}'.format(liquidityScoreAdj), '{:.2f}'.format(subordinationScoreAdj), '{:.2f}'.format(diversificationScoreAdj), '{:.2f}'.format(mdScoreAdj), '{:.2f}'.format(adjustedVal)]

    palette0 = px.colors.qualitative.Set3

    colors = ['white', palette0[1], 'white', palette0[1], 'white', palette0[1]]



    headerColor = palette0[11]

    fig = go.Figure(data=[go.Table(
        
        columnorder = [1,2,3,4],
        columnwidth = [35,35,35, 35],
        
        header=dict(values=head,
                    fill_color=headerColor,
                    font=dict(color='black'),
                    line_color='darkslategray',
                    align=['left', 'center', 'center', 'center']),
        cells=dict(values=[metric, divisor, unadjusted, adjusted],
                   fill_color=[colors*4],
                   line_color='darkslategray',
                   font=dict(color='black'),
                   align=['left', 'center', 'center', 'center']))
    ])   

    fig.update_layout(height=225, width=450, margin=dict(l=2, r=2, b=2,t=2))
    
    return fig


#tScores = tableScores(qualityScore, liquidityScore, subordinationScore, diversificationScore, mdScore,
#               qualityScoreAdj, liquidityScoreAdj, subordinationScoreAdj, diversificationScoreAdj, mdScoreAdj,
#               qualityDiv, liquityDiv, subordinationDiv, diversificationDiv, irRiskDiv,
#               unadjustedVal, adjustedVal)


#st.header('Metric Summary')
#tScores


#@st.cache_data
def riskReturn(avgYield, avgCalcSpread, mdVal, riskDurationVal, weightedTerm, score):
    

    head = ['<b>Statistic<b>', '<b>Value<b>']

    metric = ['<b>Yield (NACQ)<b>', '<b>JIBAR Spread<b>', '<b>Duration<b>', '<b>Risk Duration<b>', '<b>Weighted Term<b>', '<b>Score<b>']

    results = ['{:.2%}'.format((avgYield/100)), '{:.2f}'.format(avgCalcSpread), '{:.2f}'.format(mdVal), '{:.2f}'.format(riskDurationVal), '{:.2f}'.format(weightedTerm), 
               '{:.2f}'.format(score)]
    
    palette0 = px.colors.qualitative.Set3

    colors = ['white', palette0[1], 'white', palette0[1], 'white', palette0[1]]

   

    headerColor = palette0[11]


    fig = go.Figure(data=[go.Table(
        
        columnorder = [1,2],
        columnwidth = [35,35],
        
        header=dict(values=head,
                    fill_color=headerColor,
                    line_color='darkslategray',
                    font=dict(color='black'),
                    align=['left', 'center']),
        cells=dict(values=[metric, results],
                   fill_color=[colors*2],
                   line_color='darkslategray',
                   font=dict(color='black'),
                   align=['left', 'center']))
    ])   

    fig.update_layout(height=250, width=250, margin=dict(l=2, r=2, b=2,t=2))
    
    return fig



#st.header('Risk to Return Table')
#
#riskReturn = riskReturn(avgQYield, avgSpread, mdVal, riskDurationVal, weightedTerm, score)
#riskReturn


#@st.cache_data
def issuerSummary(data):

    palette0 = px.colors.qualitative.Set3

    headerColor = palette0[11]
    counter = data.index
    col = data.shape[1]

    palette = px.colors.qualitative.Set3


    colors = []

    for i in counter:
        if (data['Grouping'][i] == 'financial'):
            colors.append(palette[0])
        elif (data['Grouping'][i] == 'insurance'):
            colors.append(palette[1])
        elif (data['Grouping'][i] == 'sovereign'):
            colors.append(palette[2])
        elif (data['Grouping'][i] == 'state owned'):
            colors.append(palette[3])      
        elif (data['Grouping'][i] == 'corporate'):
            colors.append(palette[4])  
        elif (data['Grouping'][i] == 'securitization'):
            colors.append(palette[5])  
        elif (data['Grouping'][i] == 'real estate'):
            colors.append(palette[6])  
        else:
            colors.append(palette[7])
    

    

    head = ['<b>Issuer<b>', '<b>Sector<b>', '<b>Grouping<b>', '<b>Issuer MV<b>', '<b>Issuer (%)<b>', '<b>Exp MV<b>',
            '<b>Exp (%)<b>', '<b>Z-Score<b>', '<b>EV<b>', '<b>Weight<b>', '<b>Final<b>', '<b>Active<b>', '<b>HHI Index<b>']
    

    issuer = data['Issuer'].to_list()
    sector = data['Sector'].to_list()
    grouping = data['Grouping'].to_list()
    imv = data['issuerMarketValue'].map('{:,.2f}'.format).to_list()
    iholding = data['issuerPercent'].map('{:.2%}'.format).to_list()
    emv = data['exposureMarketValue'].map('{:,.2f}'.format).to_list()
    eholding = data['exposurePercent'].map('{:.2%}'.format).to_list()
    zscore = data['Z-Score'].map('{:,.4f}'.format).to_list()
    ev = data['EV'].map('{:,.2f}'.format).to_list()
    weight = data['Weight'].map('{:,.2f}'.format).to_list()
    final = data['Final'].map('{:.2%}'.format).to_list()
    active = data['Active'].map('{:.2%}'.format).to_list()
    hhi = data['HHI Index'].map('{:.4f}'.format).to_list()


    ilength = len(issuer)
    for i in range(0,ilength):
        issuer[i] = '<b>'+issuer[i]+'<b>'

    fig = go.Figure(data=[go.Table(
        
        columnorder = [1,2,3,4,5,6,7,8,9,10,11,12,13],
        columnwidth = [130,35,35,35,35,35,35,35,35,35,35,35, 35],
        
        header=dict(values=head,
                    fill_color=headerColor,
                    line_color='darkslategray',
                    font=dict(color='black'),
                    align=['left', 'center']),
        cells=dict(values=[issuer, sector, grouping, imv, iholding, emv, eholding, zscore, ev, weight, final, active, hhi],
                   fill_color=[colors*col],
                   line_color='darkslategray',
                   font=dict(color='black'),
                   align=['left', 'center']))
    ])   

    fig.update_layout(height=3200, width=1300, margin=dict(l=2, r=2, b=2,t=2))
    
    return fig

#st.header('Issuer Holding')
#
#st.write('<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: left;} </style>', unsafe_allow_html=True)
#
#st.write('<style>div.st-bf{flex-direction:column;} div.st-ag{font-weight:bold;padding-left:2px;}</style>', unsafe_allow_html=True)
#
#choose=st.radio("Filter",("Off", "Grouping", "Sector", "Issuer"))
#
#
#
#
#if (choose=="Off"):
#
#    iSummary = issuerSummary(df_final)
#    iSummary
#elif(choose=="Grouping"):
#    group = df_final['Grouping'].unique()
#
#    groupFilter = st.multiselect('Select Groupings', group, default=group[0])
#
#    filter1 = df_final.loc[(df_final['Grouping'].isin(groupFilter))]
#
#    xSummary = issuerSummary(filter1)
#    xSummary
#elif(choose=="Sector"):
#    sector = df_final['Sector'].unique()
#
#    sectorFilter = st.multiselect('Select Groupings', sector, default=sector[0])
#
#    filter2 = df_final.loc[(df_final['Sector'].isin(sectorFilter))]
#
#    xSummary = issuerSummary(filter2)
#    xSummary
#elif(choose=="Issuer"):
#    issr = df_final['Issuer'].unique()
#
#    issrFilter = st.multiselect('Select Groupings', issr, default=issr[0])
#
#    filter3 = df_final.loc[(df_final['Issuer'].isin(issrFilter))]
#
#    xSummary = issuerSummary(filter3)
#    xSummary


#figBubble = px.scatter(df_final, x="Issuer", y="exposureMarketValue",
#	         size="exposureMarketValue", color="exposureMarketValue",
#                 hover_name="Issuer", height=600, width=1300)
#figBubble


#figPie = px.pie(df_final, values='exposureMarketValue', names='Grouping', color_discrete_sequence=px.colors.sequential.RdBu, 
#                title='Grouping Allocation', hover_data=['Grouping'], width=900, height=600)
#figPie.update_traces(textposition='inside',
#                     textinfo='percent+label',
#                     marker=dict(line=dict(color='darkgray', width=1)))
#figPie

#st.dataframe(merged3)
#
#figHist = px.histogram(merged3, x='YTM_Quarterly',
#                       #color_discrete_sequence=px.colors.sequential.RdBu_r,
#                       text_auto=True,
#                        #histfunc="avg", nbins=8, text_auto=True,
#                title='NACQ YTM Distribution', width=900, height=600)
#figHist.update_traces(marker=dict(line=dict(color='darkgray', width=1)))
#figHist
#
#
#
#figBox = px.box(merged3, x="Exposure", y="YTM_Quarterly", width=1200, height=900)
#figBox
##figBox = px.box(merged3, x="Months", y="YTM_Quarterly", width=1200, height=900)
##figBox
#
#
#figBox2 = px.box(merged3, x="Level of Subordination", y="YTM_Quarterly", width=1200, height=900)
#figBox2

#@st.cache_data
def summaryTables(data, name, c, h, w):


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
    

    head = ['<b>'+name+'<b>', '<b>Market Value<b>', '<b>% (MV)<b>']
    

    itype = data.index.to_list()
    imv = data['AssetMarketValue'].map('{:,.2f}'.format).to_list()
    iholding = data['issuerPercent'].map('{:.2%}'.format).to_list()

    count1 = len(itype)
    for i in range(0,count1):
        itype[i] = '<b>'+str(itype[i])+'<b>'



    itype.append('<b>Total<b>')
    imv.append('<b>{:,.2f}<b>'.format(data['AssetMarketValue'].sum()))
    iholding.append('<b>{:.2%}<b>'.format(data['issuerPercent'].sum()))

    fig = go.Figure(data=[go.Table(
        
        columnorder = [1,2,3],
        columnwidth = [c,35,35],
        
        header=dict(values=head,
                    fill_color = headerColor,
                    line_color='darkslategray',
                    font=dict(color='black'),
                    align=['left', 'center', 'center']),
        cells=dict(values=[itype, imv, iholding],
                   fill_color = [colors*col],
                   line_color='darkslategray',
                   font=dict(color='black'),
                   align=['left', 'center', 'center']))
    ])   

    fig.update_layout(height=h, width=w, margin=dict(l=3, r=0, b=1,t=1))
    
    return fig



#@st.cache_data
def exposureTables(data, name, c, h, w):
    palette0 = px.colors.qualitative.Set3

    totalColor = palette0[10]
    rowEvenColor = 'white'
    rowOddColor = palette0[1]

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

    head = ['<b>'+name+'<b>', '<b>Exposure Value<b>', '<b>% (MV)<b>']
    

    itype = data.index.to_list()
    imv = data['exposureMarketValue'].map('{:,.2f}'.format).to_list()
    iholding = data['exposurePercent'].map('{:.2%}'.format).to_list()

    count1 = len(itype)
    for i in range(0,count1):
        itype[i] = '<b>'+str(itype[i])+'<b>'

    itype.append('<b>Total<b>')
    imv.append('<b>{:,.2f}<b>'.format(data['exposureMarketValue'].sum()))
    iholding.append('<b>{:.2%}<b>'.format(data['exposurePercent'].sum()))

    fig = go.Figure(data=[go.Table(
        
        columnorder = [1,2,3],
        columnwidth = [c,35,35],
        
        header=dict(values=head,
                    fill_color=headerColor,
                    line_color='darkslategray',
                    font=dict(color='black'),
                    align=['left', 'center', 'center']),
        cells=dict(values=[itype, imv, iholding],
                   fill_color=[colors*col],
                   line_color='darkslategray',
                   font=dict(color='black'),
                   align=['left', 'center', 'center']))
    ])   

    fig.update_layout(height=h, width=w, margin=dict(l=2, r=2, b=2,t=2))
    
    return fig

#st.header('Issuer Type')
#iType = summaryTables(instrumentType, 'Issuer Type', 30, 250, 350)
#iType

#st.header('Seniority Type')
#dType = summaryTables(debtType, 'Seniority Type', 70, 650, 400)
#dType


#st.header('Reference')
#refType = summaryTables(referenceType, 'Reference', 25, 475, 400)
#refType

#refCheck = refCheck(referenceType)
#refCheck


#st.header('Bucket')
#bucketType = summaryTables(bucket, 'Bucket', 15, 700, 400)
#bucketType


def exposureProfile(data, title, h,w):

    counter1 = len(data.index)
    counter0 = list(range(1,counter1+1))

    figBucket = px.bar(data, x=counter0, y='issuerPercent',
                hover_data=['AssetMarketValue', 'issuerPercent'], color='issuerPercent',
                color_continuous_scale=px.colors.sequential.RdBu_r, text_auto='.2%',
                labels={'issuerPercent':'%', 'x':"Months"}, height=h, width=w)


    figBucket.update_layout(
        xaxis = dict(
            tickmode = 'array',
            tickvals = counter0,
            ticktext = data.index.to_list()
        ),
        title=dict(text=title,
                font=dict(size=30),
                automargin=True,
                yref='paper')
    )

    figBucket.update_traces(textfont_size=12,
                            textangle=0,
                            textposition="outside",
                            cliponaxis=False,
                            marker_line_color='rgb(8,48,107)',
                            marker_line_width=1.5,
                            opacity=1
                            )


    return figBucket



def typeProfile(data, title, h,w, MV, Percent):

    figBucket = px.bar(data, x=data.index.to_list(), y=Percent,
                hover_data=[MV, Percent], color=Percent,
                color_continuous_scale=px.colors.sequential.RdBu_r, text_auto='.2%',
                labels={Percent:'% Holding'}, height=h, width=w)


    figBucket.update_layout(
        #xaxis = dict(
        #    tickmode = 'array',
        #    tickvals = counter0,
        #    ticktext = data.index.to_list()
        #),
        title=dict(text=title,
                #font=dict(size=30),
                #automargin=True,
                #yref='paper'
                )
    )

    figBucket.update_traces(textfont_size=12,
                            textangle=0,
                            textposition="outside",
                            cliponaxis=False,
                            marker_line_color='rgb(8,48,107)',
                            marker_line_width=1.5,
                            opacity=1
                            )

    return figBucket




#bucketExposuregraphs = exposureProfile(bucket, 'Bucket Exposure')
#bucketExposuregraphs

#summaryBucketType = summaryTables(summaryBucket, 'summaryBucket', 25, 450, 400)
#summaryBucketType

#yearlyBucketExposure = exposureProfile(summaryBucket, 'Summary Bucket Exposure')
#yearlyBucketExposure 

#st.header('Infrastructure')
#infraType = summaryTables(infrastructureType, 'Infrastructure', 25, 125, 400)
#infraType



#st.header('Sector Allocation')
#secType = exposureTables(sectorType, 'Sector', 25, 500, 400)
#secType

#figBubble = px.scatter(sectorType, x=sectorType.index, y="exposureMarketValue",
#	         size="exposureMarketValue", color="exposureMarketValue",
#                 hover_name=sectorType.index, size_max=60)
#figBubble



#@st.cache_data
def liquidityCheck(bankMV, goviMV, liquidMV, bank, govi, liquid):
    
    bankANDgoviMV = bankMV + goviMV
    bankANDgovi = bank + govi

    head = ['<b>Metric<b>', '<b>Market Value<b>', '<b>% (MV)<b>']

    
    name = ['<b>Very Liquid<b>', '<b>-----------------------------<b>',
            '<b>Bank<b>', '<b>Govi<b>', '<b>-----------------------------<b>',
            '<b>Bank + Govi<b>']
    marketVal = ['{:,.2f}'.format(liquidMV), '<b>-----------------------------<b>', '{:,.2f}'.format(bankMV),
                 '{:,.2f}'.format(goviMV), '<b>-----------------------------<b>', '{:,.2f}'.format(bankANDgoviMV)]
    marketPercent = ['{:.2%}'.format(liquid), '<b>-----------------------------<b>', '{:.2%}'.format(bank),
                     '{:.2%}'.format(govi), '<b>-----------------------------<b>', '{:.2%}'.format(bankANDgovi)]

    palette0 = px.colors.qualitative.Set3

    colors = ['white', palette0[1], 'white', palette0[1], 'white', palette0[1]]

    headerColor = palette0[11]

    fig = go.Figure(data=[go.Table(
        
        columnorder = [1,2,3],
        columnwidth = [35,35,35],
        
        header=dict(values=head,
                    fill_color=headerColor,
                    line_color='darkslategray',
                    font=dict(color='black'),
                    align=['left', 'center', 'center']),
        cells=dict(values=[name, marketVal, marketPercent],
                   fill_color=[colors*3],
                   line_color='darkslategray',
                   font=dict(color='black'),
                   align=['left', 'center', 'center']))
    ])   

    fig.update_layout(height=225, width=400, margin=dict(l=2, r=2, b=2,t=2))
    
    return fig



#st.header('Liquidity Check')
#liquidityStatus = liquidityCheck(bankMV, goviMV, liquidMV, bank, govi, liquid)
#liquidityStatus

#########################################################################################################################
###################### All Graphs and Tables ############################################################################

ban, head = st.columns([1,2])
#head, ban = st.columns([1.15,1])
#blank, ban, head = st.columns([0.4, 1,2])

#st.markdown(" ")
banner1 = Image.open('AC1.jpg')
ban.image(banner1)
ban.markdown(" ")
ban.markdown(" ")


#head.markdown(" ")
head.markdown(" ")
head.markdown(" ")
head.markdown("<h1 style='text-align: left; color: #008080; padding-left: 20px; font-size: 80px'><b>Ci Diversified Income<b></h1>", unsafe_allow_html=True)
#st.markdown("<h1 style='text-align: left; color: gray; padding-left: 0px; font-size: 40px'><b>Portfolio Analytics<b></h1>", unsafe_allow_html=True)
#st.markdown("<h2 style='text-align: left; color: gray; padding-left: 0px; font-size: 30px'><b>Portfolio Analytics<b></h2>", unsafe_allow_html=True)
#st.markdown("<h3 style='text-align: left; color: #872657; padding-left: 0px; font-size: 30px'><b>Portfolio Analysis<b></h3>", unsafe_allow_html=True)


#st.header('Portfolio Analytics')
#st.markdown(" ")
#st.markdown(" ")
#st.markdown(" ")
#st.markdown(" ")

metric, liq, riskRt = st.columns([1.1 ,1, 1])

metric.header('Metric Summary')
# - #008080
#metric.markdown("<h1 style='text-align: left; color: gray; padding-left: 0px; font-size: 30px'><b>Metric Summary<b></h1>", unsafe_allow_html=True)
tScores = tableScores(qualityScore, liquidityScore, subordinationScore, diversificationScore, mdScore,
               qualityScoreAdj, liquidityScoreAdj, subordinationScoreAdj, diversificationScoreAdj, mdScoreAdj,
               qualityDiv, liquityDiv, subordinationDiv, diversificationDiv, irRiskDiv,
               unadjustedVal, adjustedVal)
metric.plotly_chart(tScores, use_column_width=True)

liq.header('Liquidity Check')
liquidityStatus = liquidityCheck(bankMV, goviMV, liquidMV, bank, govi, liquid)
liq.plotly_chart(liquidityStatus, use_column_width=True)

riskRt.header('Risk-Return Table')


riskReturns = riskReturn(avgYield, avgCalcSpread, mdVal, riskDurationVal, weightedTerm, score)
riskRt.plotly_chart(riskReturns, use_column_width=True)

bucket1a, bucket1b, bucket1c = st.columns([1, 1, 1])

bucket1a.header('Bucket Exposure')
bucketType = summaryTables(bucket, 'Bucket', 15, 715, 400)
#bucketType
bucket1a.plotly_chart(bucketType, use_column_width=True)

#######
#bucketExposuregraphs = exposureProfile(bucket, "Exposure Profile", 450, 800)
#bucket1b.markdown(" ")
#bucket1b.markdown(" ")
#bucket1b.markdown(" ")
#bucket1b.markdown(" ")
#bucket1b.markdown(" ")
#bucket1b.markdown(" ")
#bucket1b.markdown(" ")
#bucket1b.markdown(" ")
#bucket1b.markdown(" ")
#bucket1b.markdown(" ")
#bucket1b.markdown(" ")
#bucket1b.markdown(" ")
#bucket1b.markdown(" ")
#bucket1b.markdown(" ")
#bucket1b.plotly_chart(bucketExposuregraphs, use_column_width=True)
####





bucket2a, bucket2b = st.columns([0.5, 1])

#bucket2a.header('Grouped Bucket Exposure')
#summaryBucketType = summaryTables(summaryBucket, 'summaryBucket', 25, 450, 400)
#bucket2a.plotly_chart(summaryBucketType, use_column_width=True)

bucket1b.header('Grouped Bucket Exposure')
summaryBucketType = summaryTables(summaryBucket, 'summaryBucket', 25, 450, 400)
bucket1b.plotly_chart(summaryBucketType, use_column_width=True)

bucket1b.header('Infrastructure')
infraType = summaryTables(infrastructureType, 'Infrastructure', 25, 130, 400)
bucket1b.plotly_chart(infraType, use_column_width=True)



bucket1c.header('Seniority Type')
bucket1c.markdown(' ')
#bucket1c.markdown(' ')
#sen2.markdown(' ')
dType = summaryTables(debtType, 'Seniority Type', 70, 655, 400)
bucket1c.plotly_chart(dType, use_column_width=True)

#yearlyBucketExposure = exposureProfile(summaryBucket, "Group Exposure Profile", 400, 850)
#bucket2b.markdown(" ")
#bucket2b.markdown(" ")
#bucket2b.markdown(" ")
#bucket2b.markdown(" ")
#bucket2b.markdown(" ")
#bucket2b.markdown(" ")
#bucket2b.markdown(" ")
##bucket2b.markdown(" ")
#bucket2b.plotly_chart(yearlyBucketExposure, use_column_width=True)

exp1, exp2 = st.columns([1,1])

bucketExposuregraphs = exposureProfile(bucket, "Exposure Profile", 300, 700)
exp1.plotly_chart(bucketExposuregraphs, use_column_width=True)

yearlyBucketExposure = exposureProfile(summaryBucket, "Group Exposure Profile", 300, 700)
exp2.plotly_chart(yearlyBucketExposure, use_column_width=True)


#####

mdBucket = merged3[['AssetMarketValue', 'issuerPercent', 'mdBucket1']]
mdBucketGrouped = merged3[['AssetMarketValue', 'issuerPercent', 'mdBucket2']]

mdGroupBucket= mdBucket.groupby('mdBucket1').sum()
mdGroupedBucket= mdBucketGrouped.groupby('mdBucket2').sum()

#st.dataframe(mdGroupBucket)
#st.dataframe(mdGroupedBucket)


mdbucketExposuregraphs = exposureProfile(mdGroupBucket, "MD Exposure Profile", 300, 700)
#st.plotly_chart(mdbucketExposuregraphs)
exp1.plotly_chart(mdbucketExposuregraphs)

mdbucketGroupedgraphs = exposureProfile(mdGroupedBucket, "MD Grouped Exposure Profile", 300, 700)
#st.plotly_chart(mdbucketGroupedgraphs)
exp2.plotly_chart(mdbucketGroupedgraphs)

####



check = typeProfile(debtType,'Seniority Breakdown', 400,1400, 'AssetMarketValue', 'issuerPercent')
check

sec1, ref1, iss1 = st.columns([1,0.9,1])

#st.header('Sector Allocation')
#sec1.markdown(' ')
#sec1.markdown(' ')
sec1.header('Sector Allocation')
sec1.markdown(' ')
sec1.markdown(' ')
secType = exposureTables(sectorType, 'Sector', 25, 500, 400)
sec1.plotly_chart(secType, use_column_width=True)

#check0 = typeProfile(sectorType,'Sector Allocation', 400,1300, 'exposureMarketValue', 'exposurePercent')
#check0



#st.header("Reference")
ref1.header("Reference")
refCheck11, ref_df1 = refCheck(referenceType)
ref1.plotly_chart(refCheck11, use_column_width=True)
#ref_df1


def pieGraph(data, title, h, w):
    figPie = px.pie(data, values='Val', names='Ref', color_discrete_sequence=px.colors.sequential.RdBu, 
                    title=title, hover_data=['Ref'],  height=h, width=w)
    figPie.update_traces(textposition='inside',
                        textinfo='percent+label',
                        marker=dict(line=dict(color='darkgray', width=1)))
    return figPie



refPie = pieGraph(ref_df1, "Instrument Split", 450, 400)
sec1.plotly_chart(refPie, use_column_width=True)



#iss1.header('Issuer Type')
#iType = summaryTables(instrumentType, 'Issuer Type', 30, 250, 350)
#iss1.plotly_chart(iType, use_column_width=True)


#ref1.header('Issuer Type')
iType = summaryTables(instrumentType, 'Issuer Type', 30, 250, 350)
ref1.plotly_chart(iType, use_column_width=True)


iss1.markdown(' ')
#iss1.markdown(' ')
iss1.header('Companion')
iss1.markdown(' ')
iss1.markdown(' ')
refType = summaryTables(referenceType, 'Reference', 25, 475, 400)
iss1.plotly_chart(refType, use_column_width=True)


def pieGraph2(data, title, h, w):
    figPie = px.pie(data, values='AssetMarketValue', names=data.index, color_discrete_sequence=px.colors.sequential.RdBu, 
                    title=title,  height=h, width=w)
    figPie.update_traces(textposition='inside',
                        textinfo='percent+label',
                        marker=dict(line=dict(color='darkgray', width=1)))
    return figPie

issuerPie = pieGraph2(instrumentType, 'Issuer Split', 450, 400)
ref1.plotly_chart(issuerPie, use_column_width=True)


###sen2, ref2, graf = st.columns([1,1, 1])

#sen2.header('Seniority Type')
#sen2.markdown(' ')
#sen2.markdown(' ')
##sen2.markdown(' ')
#dType = summaryTables(debtType, 'Seniority Type', 70, 655, 400)
#sen2.plotly_chart(dType, use_column_width=True)



#check = typeProfile(debtType,'Seniority Breakdown', 400,1300, 'AssetMarketValue', 'issuerPercent')
#check


#ref2.header('Companion Reference')
#refType = summaryTables(referenceType, 'Reference', 25, 475, 400)
#ref2.plotly_chart(refType, use_column_width=True)



#ref2.header('Infrastructure')
#infraType = summaryTables(infrastructureType, 'Infrastructure', 25, 130, 400)
#ref2.plotly_chart(infraType, use_column_width=True)

refePie = pieGraph2(referenceType, 'Companion Split', 450, 400)
iss1.plotly_chart(refePie, use_column_width=True)

#check0 = typeProfile(sectorType,'Sector Allocation', 400,1300, 'exposureMarketValue', 'exposurePercent')
#check0




st.header('Issuer Holding Analysis')

st.write('<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: left;} </style>', unsafe_allow_html=True)

#st.write('<style>div.st-bf{flex-direction:column;} div.st-ag{font-weight:bold;padding-left:2px;}</style>', unsafe_allow_html=True)

#showDF = st.radio("Show Issuer Table",("No", "Yes"))

showDF = st.selectbox("Show Issuer Table",("No", "Yes"))


if (showDF == "Yes"):
    #st.write('<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: left;} </style>', unsafe_allow_html=True)

    #st.write('<style>div.st-bf{flex-direction:column;} div.st-ag{font-weight:bold;padding-left:2px;}</style>', unsafe_allow_html=True)
    ########
    choose=st.radio("Filter",("Off", "Grouping", "Sector", "Issuer"))



    if (choose=="Off"):

        iSummary = issuerSummary(df_final)
        iSummary


    elif(choose=="Grouping"):
        group = df_final['Grouping'].unique()

        groupFilter = st.multiselect('Select Groupings', group, default=group[0])

        filter1 = df_final.loc[(df_final['Grouping'].isin(groupFilter))]

        xSummary = issuerSummary(filter1)
        xSummary
    elif(choose=="Sector"):
        sector = df_final['Sector'].unique()

        sectorFilter = st.multiselect('Select Groupings', sector, default=sector[0])

        filter2 = df_final.loc[(df_final['Sector'].isin(sectorFilter))]

        xSummary = issuerSummary(filter2)
        xSummary
    elif(choose=="Issuer"):
        issr = df_final['Issuer'].unique()

        issrFilter = st.multiselect('Select Groupings', issr, default=issr[0])

        filter3 = df_final.loc[(df_final['Issuer'].isin(issrFilter))]

        xSummary = issuerSummary(filter3)
        xSummary

########

#figPie = px.pie(df_final, values='exposureMarketValue', names='Grouping', color_discrete_sequence=px.colors.sequential.RdBu, 
#                title='Grouping Allocation', hover_data=['Grouping'], width=900, height=600)
#figPie.update_traces(textposition='inside',
#                     textinfo='percent+label',
#                     marker=dict(line=dict(color='darkgray', width=1)))
#figPie


###st.dataframe(df_final)

groupType = df_final.groupby('Grouping').sum()
groupType = groupType.sort_values(by='exposureMarketValue', ascending=False)

###st.dataframe(groupType)

def groupProfile(data, title, Percent, financials_limit, insurance_limit, sovereign_limit, state_limit, corporate_limit,
                 securitization_limit, real_estate_limit, indirect_limit, h, w):
#def groupProfile():

    limits = [financials_limit, sovereign_limit, state_limit, corporate_limit, indirect_limit, insurance_limit,
              real_estate_limit, securitization_limit]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=data.index.to_list(),
        y=data[Percent],
        text=data[Percent],
        texttemplate='%{text:.2f}',
        name='Sector',
        #marker_color='gold'
        #marker_color='dodgerblue'
        #marker_color='dodgerblue'
    ))
    fig.add_trace(go.Bar(
        x=data.index.to_list(),
        #y=data['Final'],
        y=limits,
        text=limits,
        texttemplate='%{text:.2f}',
        name='Limit',
        #marker_color='darkred'
        #marker_color='lawngreen'
        #marker_color='lawngreen'
    ))

    # Here we modify the tickangle of the xaxis, resulting in rotated labels.
    fig.update_layout(barmode='group',
                      #xaxis_tickangle=-45,
                      title_text=title,
                      height=h,
                      width=w)
    
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.25,
        xanchor="left",
        x=0.4
    ))
    return fig


sectorAlloc, groupAlloc = st.columns([1,1])

check0 = typeProfile(sectorType,'Sector Allocation', 300,700, 'exposureMarketValue', 'exposurePercent')
sectorAlloc.plotly_chart(check0, use_column_width=True)


checker = groupProfile(groupType, 'Grouping Allocation', 'exposurePercent', financials_limit, insurance_limit, sovereign_limit, state_limit, corporate_limit,
                       securitization_limit, real_estate_limit, indirect_limit, 300,700)
groupAlloc.plotly_chart(checker, use_column_width=True)
#check8 = groupProfile(groupType,'Grouping', 400,1300, 'exposureMarketValue', 'exposurePercent')
#check8

#check00 = typeProfile(df_final,'Active Allocation', 400,1300, 'Active', 'exposurePercent')
#check00

def activeProfile(data, h,w):

    data = data.sort_values(by='Active', ascending=False)

    figBucket = px.bar(data, x='Issuer', y='Active',
                color='Active',
                color_continuous_scale=px.colors.sequential.RdBu_r, text_auto='.2%',
                labels={'Active':'Active Holding'}, height=h, width=w)


    figBucket.update_layout(
        #xaxis = dict(
        #    tickmode = 'array',
        #    tickvals = counter0,
        #    ticktext = data.index.to_list()
        #),
        title=dict(text='Issuer Active Holding',
                font=dict(size=30),
                automargin=True,
                yref='paper')
    )

    figBucket.update_traces(textfont_size=12,
                            textangle=0,
                            textposition="outside",
                            cliponaxis=False,
                            marker_line_color='rgb(8,48,107)',
                            marker_line_width=1.5,
                            opacity=1
                            )

    return figBucket

checking = activeProfile(df_final, 700,1400)
checking

#showMergedDF = st.radio("Show Holdings Table",("No", "Yes"))

showMergedDF = st.selectbox("Show Holdings Table",("No", "Yes"))

if (showMergedDF == "Yes"):

    #st.dataframe(merged3)



#showDF = st.radio("Show Issuer Table",("No", "Yes"))

#if (showDF == "Yes"):
    #st.write('<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: left;} </style>', unsafe_allow_html=True)

    #st.write('<style>div.st-bf{flex-direction:column;} div.st-ag{font-weight:bold;padding-left:2px;}</style>', unsafe_allow_html=True)
    ########
    choose=st.radio("Filter",("Off", "Issuer", "Level", "Type", "Companion"))


    if (choose=="Off"):

        st.dataframe(merged3)
    
    elif(choose=="Issuer"):
        group = merged3['Issuer'].unique()

        groupFilter = st.multiselect('Select Issuers', group, default=group[0])

        filter1 = merged3.loc[(merged3['Issuer'].isin(groupFilter))]

        st.dataframe(filter1)

        showRegression = st.radio("Show Regression Model",("No", "Yes"))
        #showRegression = st.selectbox("Show Regression Model",("No", "Yes"))

        if (showRegression == "Yes"):

            yieldRegressionType =st.radio("Type",("YTM", "JIBAR Spread"))

            if(yieldRegressionType == "YTM"):

                yieldGraph, summary, param = MTMRegressionQuarterly(filter1)
                
                graphCol, summaryCol = st.columns([1.1,0.9])

                graphCol.header('OLS Yield to Maturity')

                graphCol.plotly_chart(yieldGraph)
                

                summaryCol.header('Yield to Maturity Regression Model')

                constant = round(param[0],5)
                gradient = round(param[1],5)

                summaryCol.markdown(' ')
                summaryCol.markdown(' ')
                summaryCol.markdown(' ')
                summaryCol.markdown(' ')

                summaryCol.markdown('YTM = '+str(round(param[0],2))+' + ' + str(round(param[1],2)) + ' x Term')

                inputTerm = summaryCol.number_input('Term', value=1.00)

                Spread = round(constant + gradient*inputTerm,2)

                summaryCol.markdown('Estimated YTM = '+str(Spread))

            elif(yieldRegressionType == "JIBAR Spread"):
#####
                jibarGraph, summary0, param0 = MTMRegressionJIBAR(filter1)
                
                
                graphCol0, summaryCol0 = st.columns([1.1,0.9])

                graphCol0.header('OLS JIBAR Spread')

                graphCol0.plotly_chart(jibarGraph)
                

                summaryCol0.header('JIBAR Spread Regression Model')

                constant0 = round(param0[0],5)
                gradient0 = round(param0[1],5)

                summaryCol0.markdown(' ')
                summaryCol0.markdown(' ')
                summaryCol0.markdown(' ')
                summaryCol0.markdown(' ')

                summaryCol0.markdown('JIBAR Spread = '+str(round(param0[0],2))+' + ' + str(round(param0[1],2)) + ' x Term')

                inputTerm0 = summaryCol0.number_input('Years', value=1.00)

                Spread0 = round(constant0 + gradient0*inputTerm0,2)

                summaryCol0.markdown('Estimated JIBAR Spread = '+str(Spread0))

####


    elif(choose=="Level"):
        level = merged3['Level of Subordination'].unique()

        levelFilter = st.multiselect('Select Level', level, default=level[0])

        #filter2 = merged3.loc[(merged3['Sector'].isin(levelFilter))]
        filter2 = merged3.loc[(merged3['Level of Subordination'].isin(levelFilter))]

        st.dataframe(filter2)





        showRegression = st.radio("Show regression Model",("No", "Yes"))

        if (showRegression == "Yes"):

            yieldRegressionType =st.radio("Type",("YTM", "JIBAR Spread"))

            if(yieldRegressionType == "YTM"):

                yieldGraph, summary, param = MTMRegressionQuarterly(filter2)
                
                graphCol, summaryCol = st.columns([1.1,0.9])

                graphCol.header('OLS Yield to Maturity')

                graphCol.plotly_chart(yieldGraph)
                

                summaryCol.header('Yield to Maturity Regression Model')

                constant = round(param[0],5)
                gradient = round(param[1],5)

                summaryCol.markdown(' ')
                summaryCol.markdown(' ')
                summaryCol.markdown(' ')
                summaryCol.markdown(' ')

                summaryCol.markdown('YTM = '+str(round(param[0],2))+' + ' + str(round(param[1],2)) + ' x Term')

                inputTerm = summaryCol.number_input('Term', value=1.00)

                Spread = round(constant + gradient*inputTerm,2)

                summaryCol.markdown('Estimated YTM = '+str(Spread))

            elif(yieldRegressionType == "JIBAR Spread"):
#####
                jibarGraph, summary0, param0 = MTMRegressionJIBAR(filter2)
                
                
                graphCol0, summaryCol0 = st.columns([1.1,0.9])

                graphCol0.header('OLS JIBAR Spread')

                graphCol0.plotly_chart(jibarGraph)
                

                summaryCol0.header('JIBAR Spread Regression Model')

                constant0 = round(param0[0],5)
                gradient0 = round(param0[1],5)

                summaryCol0.markdown(' ')
                summaryCol0.markdown(' ')
                summaryCol0.markdown(' ')
                summaryCol0.markdown(' ')

                summaryCol0.markdown('JIBAR Spread = '+str(round(param0[0],2))+' + ' + str(round(param0[1],2)) + ' x Term')

                inputTerm0 = summaryCol0.number_input('Years', value=1.00)

                Spread0 = round(constant0 + gradient0*inputTerm0,2)

                summaryCol0.markdown('Estimated JIBAR Spread = '+str(Spread0))

    
    elif(choose=="Type"):
        types = merged3['Issuer Type'].unique()

        typeFilter = st.multiselect('Select Type', types, default=types[0])

        filter3 = merged3.loc[(merged3['Issuer Type'].isin(typeFilter))]

        st.dataframe(filter3)



        showRegression = st.radio("Show regression Model",("No", "Yes"))

        if (showRegression == "Yes"):

            yieldRegressionType =st.radio("Type",("YTM", "JIBAR Spread"))

            if(yieldRegressionType == "YTM"):

                yieldGraph, summary, param = MTMRegressionQuarterly(filter3)
                
                graphCol, summaryCol = st.columns([1.1,0.9])

                graphCol.header('OLS Yield to Maturity')

                graphCol.plotly_chart(yieldGraph)
                

                summaryCol.header('Yield to Maturity Regression Model')

                constant = round(param[0],5)
                gradient = round(param[1],5)

                summaryCol.markdown(' ')
                summaryCol.markdown(' ')
                summaryCol.markdown(' ')
                summaryCol.markdown(' ')

                summaryCol.markdown('YTM = '+str(round(param[0],2))+' + ' + str(round(param[1],2)) + ' x Term')

                inputTerm = summaryCol.number_input('Term', value=1.00)

                Spread = round(constant + gradient*inputTerm,2)

                summaryCol.markdown('Estimated YTM = '+str(Spread))

            elif(yieldRegressionType == "JIBAR Spread"):
#####
                jibarGraph, summary0, param0 = MTMRegressionJIBAR(filter3)
                
                
                graphCol0, summaryCol0 = st.columns([1.1,0.9])

                graphCol0.header('OLS JIBAR Spread')

                graphCol0.plotly_chart(jibarGraph)
                

                summaryCol0.header('JIBAR Spread Regression Model')

                constant0 = round(param0[0],5)
                gradient0 = round(param0[1],5)

                summaryCol0.markdown(' ')
                summaryCol0.markdown(' ')
                summaryCol0.markdown(' ')
                summaryCol0.markdown(' ')

                summaryCol0.markdown('JIBAR Spread = '+str(round(param0[0],2))+' + ' + str(round(param0[1],2)) + ' x Term')

                inputTerm0 = summaryCol0.number_input('Years', value=1.00)

                Spread0 = round(constant0 + gradient0*inputTerm0,2)

                summaryCol0.markdown('Estimated JIBAR Spread = '+str(Spread0))



    elif(choose=="Companion"):
        companion = merged3['Companion'].unique()

        companionFilter = st.multiselect('Select Companion', companion, default=companion[0])

        filter4 = merged3.loc[(merged3['Companion'].isin(companionFilter))]

        st.dataframe(filter4)


        showRegression = st.radio("Show regression Model",("No", "Yes"))

        if (showRegression == "Yes"):

            yieldRegressionType =st.radio("Type",("YTM", "JIBAR Spread"))

            if(yieldRegressionType == "YTM"):

                yieldGraph, summary, param = MTMRegressionQuarterly(filter4)
                
                graphCol, summaryCol = st.columns([1.1,0.9])

                graphCol.header('OLS Yield to Maturity')

                graphCol.plotly_chart(yieldGraph)
                

                summaryCol.header('Yield to Maturity Regression Model')

                constant = round(param[0],5)
                gradient = round(param[1],5)

                summaryCol.markdown(' ')
                summaryCol.markdown(' ')
                summaryCol.markdown(' ')
                summaryCol.markdown(' ')

                summaryCol.markdown('YTM = '+str(round(param[0],2))+' + ' + str(round(param[1],2)) + ' x Term')

                inputTerm = summaryCol.number_input('Term', value=1.00)

                Spread = round(constant + gradient*inputTerm,2)

                summaryCol.markdown('Estimated YTM = '+str(Spread))

            elif(yieldRegressionType == "JIBAR Spread"):
#####
                jibarGraph, summary0, param0 = MTMRegressionJIBAR(filter4)
                
                
                graphCol0, summaryCol0 = st.columns([1.1,0.9])

                graphCol0.header('OLS JIBAR Spread')

                graphCol0.plotly_chart(jibarGraph)
                

                summaryCol0.header('JIBAR Spread Regression Model')

                constant0 = round(param0[0],5)
                gradient0 = round(param0[1],5)

                summaryCol0.markdown(' ')
                summaryCol0.markdown(' ')
                summaryCol0.markdown(' ')
                summaryCol0.markdown(' ')

                summaryCol0.markdown('JIBAR Spread = '+str(round(param0[0],2))+' + ' + str(round(param0[1],2)) + ' x Term')

                inputTerm0 = summaryCol0.number_input('Years', value=1.00)

                Spread0 = round(constant0 + gradient0*inputTerm0,2)

                summaryCol0.markdown('Estimated JIBAR Spread = '+str(Spread0))


histogram1, histogram2 = st.columns([1,1])


figHist = px.histogram(merged3, x='YTM_Quarterly',
                       #color_discrete_sequence=px.colors.sequential.RdBu_r,
                       color_discrete_sequence=['gold'],
                       text_auto=True,
                        #histfunc="avg", nbins=8, text_auto=True,
                title='NACQ YTM Distribution', width=650, height=500)
figHist.update_traces(marker=dict(line=dict(color='darkgray', width=1)))

histogram1.plotly_chart(figHist, use_column_width=True)



figHist2 = px.histogram(merged3, x='jibarSpread',
                       #color_discrete_sequence=px.colors.sequential.RdBu_r,
                       color_discrete_sequence=['red'],
                       text_auto=True,
                        #histfunc="avg", nbins=8, text_auto=True,
                title='Spread over JIBAR Distribution', width=650, height=500)
figHist2.update_traces(marker=dict(line=dict(color='darkgray', width=1)))
histogram2.plotly_chart(figHist2, use_column_width=True)

#boxType = st.selectbox('Box Type', ['YTM', 'Spread'])
boxType = st.radio("BoxPlot Type",("YTM", "JIBAR"))

if (boxType == 'YTM'):
    select = 'YTM_Quarterly'
else:
    select = 'jibarSpread'

figBox = px.box(merged3, x="Exposure", y=select, width=1350, height=700)
figBox

#figBox2 = px.box(merged3, x="Level of Subordination", y="YTM_Quarterly", width=1200, height=900)
#figBox2

#figBubble = px.scatter(sectorType, x=sectorType.index, y="exposureMarketValue",
#	         size="exposureMarketValue", color="exposureMarketValue",
#                 hover_name=sectorType.index, size_max=60)
#figBubble


maturityList = merged3[['InstrumentCode','Exposure', 'HoldingNominal', 'AssetMarketValue', 'Weight (%) Pre', 'YTM_Quarterly', 'Maturity', 'Type']]

maturityList = maturityList.sort_values(by='Maturity', ascending=True)

maturityList = maturityList.reset_index(drop=True)

#st.dataframe(maturityList)

st.markdown(' ')
st.markdown(' ')
st.header('Instrument Maturities')

sdate, edate = st.columns([1,1])

#today = datetime.today().date()

end_date = today + timedelta(days=10)

start_date = today
#start_date = maturityList['Maturity'][0]
end_date = end_date
#end_date = maturityList['Maturity'][0]

startDate = sdate.date_input('Start Date', start_date)
endDate = edate.date_input('End Date', end_date)

#st.markdown(maturityList['Maturity'][0])


#@st.cache_data
def instrumentMaturityTable(data, stDate, enDate):

    data = data[(data['Maturity'] >= stDate) & (data['Maturity'] <= enDate)]

    data = data[(data['Type'] != 'Call Account')]

    data = data[(data['Exposure'] != 'SOUTHCHESTER (RF) LTD')]

    data = data[(data['Exposure'] != 'NEDGROUP INVESTMENTS')]

    palette0 = px.colors.qualitative.Set3

    totalColor = palette0[10]
    rowEvenColor = 'white'
    rowOddColor = palette0[1]

    palette0 = px.colors.qualitative.Set3

    headerColor = palette0[11]
    
    count = data.shape[0]

    if (count==0):
        count=1

    col = data.shape[1]

    colors = []

    for i in range(0,count):
        if((i%2) == 0):
            colors.append(rowEvenColor)
        else:
            colors.append(rowOddColor)

    colors.append(totalColor)
    

    head = ['<b>Issuer<b>', '<b>Code<b>', '<b>Nominal<b>', '<b>Market Value<b>', '<b>% (MV)<b>', '<b>YTM NACQ<b>', '<b>Maturity<b>']
    

    icode = itype = data['InstrumentCode'].to_list()
    itype = data['Exposure'].to_list()
    inom = data['HoldingNominal'].map('{:,.2f}'.format).to_list()
    #inom = data['HoldingNominal'].to_list()
    imv = data['AssetMarketValue'].map('{:,.2f}'.format).to_list()
    #imv = data['AssetMarketValue'].to_list()
    iweight = data['Weight (%) Pre'].map('{:.2%}'.format).to_list()
    #iweight = data['Weight (%) Pre'].to_list()
    iytm = data['YTM_Quarterly'].map('{:,.2f}'.format).to_list()
    #iytm = data['YTM_Quarterly'].to_list()
    imaturity = data['Maturity'].to_list()

    count1 = len(itype)
    for i in range(0,count1):
        itype[i] = '<b>'+str(itype[i])+'<b>'



    #itype.append('<b>Total<b>')
    #imv.append('<b>{:,.2f}<b>'.format(data['AssetMarketValue'].sum()))
    #iholding.append('<b>{:.2%}<b>'.format(data['issuerPercent'].sum()))

    fig = go.Figure(data=[go.Table(
        
        columnorder = [1,2,3,4,5,6,7],
        columnwidth = [20,20, 20,20, 20, 20, 20],
        
        header=dict(values=head,
                    fill_color = headerColor,
                    line_color='darkslategray',
                    font=dict(color='black'),
                    align=['left', 'center', 'center']),
        cells=dict(values=[itype, icode, inom, imv, iweight, iytm, imaturity],
                   fill_color = [colors*col],
                   line_color='darkslategray',
                   font=dict(color='black'),
                   align=['left', 'center', 'center']))
    ])   

    fig.update_layout(height=60*count, width=1420, margin=dict(l=3, r=0, b=1,t=1))
    
    return fig

#@st.dataframe(maturityList)

test = instrumentMaturityTable(maturityList, startDate, endDate)

st.plotly_chart(test)


