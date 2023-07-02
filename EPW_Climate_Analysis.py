import streamlit as st
import pandas as pd
from io import StringIO
import os
from bokeh_plots.monthly import monthly
from bokeh_plots.daily import daily
from bokeh_plots.hourly import hourly
from bokeh_plots.histo2D import histo2D
from bokeh_plots.utciHeatmap import utciHeatmap

st.set_page_config(
   page_title="EPW Analysis Tool",
   page_icon="👓",
   layout="wide",
   initial_sidebar_state="expanded",
)
hide_streamlit_style = """
            <style>
            footer {visibility: hidden;}
            </style>
            """

st.write('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

epw_files = [file for file in os.listdir('data/')]
epw_files.insert(0,'None')

col_names=['Year','Month','Day','Hour','Seconds','Datasource','DryBulb','DewPoint','RelativeHumidity','AtmPressure','ExtHorzRad','ExtDirRad','HorzIRSky', 'GlobalHorizontalRadiation', 'DirectNormalRadiation','DiffuseHorizontalRadiation','GloHorzIllum','DirNormIllum','DifHorzIllum','ZenLum','WindDir','WindSpeed','TotSkyCvr','OpaqSkyCvr','Visibility','CeilingHgt','PresWeathObs,PresWeathCodes','PrecipWtr','AerosolOptDepth','SnowDepth','DaysLastSnow','Albedo','Rain','RainQuantity','-']
options = ['DryBulb','RelativeHumidity','DewPoint','WindSpeed','GlobalHorizontalRadiation','DirectNormalRadiation','DiffuseHorizontalRadiation']

st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
if 'df' not in st.session_state:
    st.session_state['df'] = None
    st.session_state['loc'] = None

col1, col2, col3 = st.columns([0.1,0.8,0.1])

with col2:  
    st.title('Welcome to EPW Analysis Tool')

    col1_epw, col2_epw = st.columns(2)
    with col1_epw:
        epw_sel = st.selectbox('Select an EPW weather file from the list below.', epw_files)
    with col2_epw:    
            uploaded_epw = st.file_uploader("Or upload an EPW weather file.",type='.epw')

    if uploaded_epw:
        df=pd.read_csv(uploaded_epw,names=col_names, skiprows=8)
        stringio = StringIO(uploaded_epw.getvalue().decode("utf-8"))
        string_data = stringio.read()
        loc_str = ''.join(string_data[:100])
        st.session_state['loc'] = loc_str.split(',')[1]

    elif epw_sel != 'None':
        df = pd.read_csv('data/'+epw_sel,names=col_names, skiprows=8)

    if uploaded_epw or epw_sel != 'None':
        df.loc[(df['Year'] > 1000,'Year')] = 2000
        dates = df[["Year","Month","Day","Hour"]]
        df['dates'] = pd.to_datetime(dates)
        df['day'] = (df.index+1)

    if uploaded_epw or epw_sel != 'None':
        
        #Monthly statistics
        st.header("Monthly Statistics")
        option_m = st.selectbox('Select a variable', options, index=0, key=0)
        st.bokeh_chart(monthly(df,option_m), use_container_width=True)

        # daily statistics
        st.header("Daily Statistics")
        option_d = st.selectbox('Select a variable', options, index=0, key=1)
        st.bokeh_chart(daily(df, variable=option_d), use_container_width=True)

        #hourly data
        st.header("Hourly Data")
        col1_h, col2_h = st.columns(2)
        with col1_h:          
            option_l = st.selectbox('Select variable for the left axis', options, index=0, key=2)
        with col2_h:
            option_r = st.selectbox('Select variable for the right axis', options, index=1, key=3)
        with st.container():
            st.bokeh_chart(hourly(df, var1=option_l, var2=option_r), use_container_width=True)

        #Histogram 2D
        st.header("Histogram 2D")
        col1_hist, col2_hist = st.columns(2)
        with col1_hist:          
            option_histo1 = st.selectbox('Select variable for the X axis', options, index=0, key=4)
        with col2_hist:
            option_histo2 = st.selectbox('Select variable for the Y axis', options, index=1, key=5)
        st.bokeh_chart(histo2D(df,[option_histo1,option_histo2]), use_container_width=False)

        #Outdoor comfort
        st.header("Universal Thermal Climate Index (UTCI) Heatmap")
        st.bokeh_chart(utciHeatmap(df), use_container_width=True)