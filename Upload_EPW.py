import streamlit as st
import pandas as pd
from io import StringIO
import os

st.set_page_config(
   page_title="EPW Explorer",
   page_icon="👓",
   layout="wide",
   initial_sidebar_state="expanded",
)

epw_files = [file for file in os.listdir('data/')]
epw_files.insert(0,'None')
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: visible;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
if 'df' not in st.session_state:
    st.session_state['df'] = None
    st.session_state['loc'] = None
st.title('Welcome to EPW Explorer')
# st.header("Select an EPW from the list below")
epw_sel = st.selectbox('Select an EPW from the list below. Then you can navigate the app with the menu on the left.', epw_files)
# st.header("Or upload an EPW weather file to visualise the plots")
uploaded_epw = st.file_uploader("Or upload an EPW weather file to visualise the plots")

col_names=['Year','Month','Day','Hour','Seconds','Datasource','DryBulb','DewPoint','RelativeHumidity','AtmPressure','ExtHorzRad','ExtDirRad','HorzIRSky', 'GlobalHorizontalRadiation', 'DirectNormalRadiation','DiffuseHorizontalRadiation','GloHorzIllum','DirNormIllum','DifHorzIllum','ZenLum','WindDir','WindSpeed','TotSkyCvr','OpaqSkyCvr','Visibility','CeilingHgt','PresWeathObs,PresWeathCodes','PrecipWtr','AerosolOptDepth','SnowDepth','DaysLastSnow','Albedo','Rain','RainQuantity','-']
units = ["YYYY","MM","DD","HH","s","","°C","°C","%","Pa","Wh/m2","Wh/m2","Wh/m2","Wh/m2","Wh/m2","Wh/m2","lux","lux","lux","Cd/m2","°","m/s","","","km","m","","","mm","thousandths","cm","","","mm","hr"]

if uploaded_epw:
   df=pd.read_csv(uploaded_epw,names=col_names, skiprows=8)
   stringio = StringIO(uploaded_epw.getvalue().decode("utf-8"))
   string_data = stringio.read()
   loc_str = ''.join(string_data[:100])
   st.session_state['loc'] = loc_str.split(',')[1]
elif epw_sel != 'None':
   df=pd.read_csv('data/'+epw_sel,names=col_names, skiprows=8)
   st.session_state['loc'] = epw_sel
if uploaded_epw or epw_sel != 'None':
   df.loc[(df['Year'] > 1000,'Year')] = 2000
   dates=df[["Year","Month","Day","Hour"]]
   df['dates']=pd.to_datetime(dates)
   df['day'] = (df.index+1)
   st.session_state['df'] = df

if uploaded_epw or epw_sel != 'None':
   df = st.session_state['df']
   loc = st.session_state['loc']
   st.subheader('Annual stats for '+"'"+loc+"'")
   col1, col2, col3, col4 = st.columns(4)
   db = df['DryBulb']
   rh = df['RelativeHumidity']
   db_max = str(db.max()) +'°C'
   db_max_above_avg = round(db.max() - db.mean(),1)
   db_min = str(db.min()) +'°C'
   db_min_below_avg = round(-1*(db.mean() - db.min()),1)
   rh_max = str(rh.max()) +'%'
   rh_max_above_avg = round((rh.max() - rh.mean()),1)
   rh_min = str(rh.min()) +'%'
   rh_min_below_avg = round(-1*(rh.mean() - rh.min()),1)
   col1.metric("Max Temperature ", db_max, db_max_above_avg, 'off', help = 'Maximum Dry Bulb temperature in the EPW file. The delta shown below is relative to the annual average')
   col2.metric("Min Temperature °C", db_min, db_min_below_avg, 'off', help = 'Minimum Dry Bulb temperature in the EPW file. The delta shown below is relative to the annual average')
   col3.metric("Max Humidity %", rh_max, rh_max_above_avg, 'off', help = 'Maximum Relative Humidity in the EPW file. The delta shown below is relative to the annual average')
   col4.metric("Min Humidity %", rh_min, rh_min_below_avg, 'off', help = 'Minimum Relative Humidity in the EPW file. The delta shown below is relative to the annual average')

