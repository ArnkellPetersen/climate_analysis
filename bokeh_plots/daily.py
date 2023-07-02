import bokeh.models as bkm
import pandas as pd
from bokeh.plotting import figure
from datetime import timedelta
from bokeh.models.tools import SaveTool
from bokeh.models import DatetimeTickFormatter, Band, DataRange1d, ColumnDataSource, Range1d
from bokeh.models.tickers import DatetimeTicker
import statistics
from datetime import timedelta
from bokeh.layouts import gridplot

col_names=['Year','Month','Day','Hour','Seconds','Datasource','DryBulb','DewPoint','RelativeHumidity','AtmPressure','ExtHorzRad','ExtDirRad','HorzIRSky', 'GlobalHorizontalRadiation', 'DirectNormalRadiation','DiffuseHorizontalRadiation','GloHorzIllum','DirNormIllum','DifHorzIllum','ZenLum','WindDir','WindSpeed','TotSkyCvr','OpaqSkyCvr','Visibility','CeilingHgt','PresWeathObs,PresWeathCodes','PrecipWtr','AerosolOptDepth','SnowDepth','DaysLastSnow','Albedo','Rain','RainQuantity','-']
units = ["YYYY","MM","DD","HH","s","","°C","°C","%","Pa","Wh/m2","Wh/m2","Wh/m2","Wh/m2","Wh/m2","Wh/m2","lux","lux","lux","Cd/m2","°","m/s","","","km","m","","","mm","thousandths","cm","","","mm","hr"]
m_days=[31,28,31,30,31,30,31,31,30,31,30,31]
months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

def daily(df, variable='DryBulb'):

    vars_unit = units[col_names.index(variable)]

    #initiate bokeh figure and tools
    tools=[SaveTool(),'reset']

    data_pts = []

    for m, days in enumerate(m_days):
        day_sub = []
        for h in range(24):
            hour_sub = []
            for d in range(days):
                if m == 0:
                    hour_sub.append(h+(d*24))
                else:
                    hour_sub.append(h+(d+sum(m_days[:(m)]))*24)
            day_sub.append(hour_sub)
        data_pts.append(day_sub)

    figures = []
    fline=figure(y_axis_label=variable+" "+vars_unit,width=0,height=400)
    fline.y_range=Range1d(start=df[variable].min()-(max(df[variable])*0.1), end=df[variable].max()+(max(df[variable])*0.1))
    fline.line(x=[0,0],y=[df[variable].min(),df[variable].max()],alpha=0)
    fline.xaxis.visible = False
    fline.ygrid.grid_line_color = None
    fline.xgrid.grid_line_color = None
    fline.outline_line_color = None
    figures.append(fline)
    for m in range(12):
        high = []
        low = []
        mean = []
        for h in range(24):
            high.append(df[variable].iloc[data_pts[m][h]].max())
            low.append(df[variable].iloc[data_pts[m][h]].min())
            mean.append(df[variable].iloc[data_pts[m][h]].mean())

        newdf = pd.DataFrame({'Year': [2000 for x in range(24)],
                        'Month': [m+1 for x in range(24)],
                        'Day': [1 for x in range(24)],
                        'Hour': [x+1 for x in range(24)],
                        'high': high,
                        'low': low,
                        'mean': mean})
        
        #create figure
        if m == 0:
            fm=figure(title=months[m],y_axis_label=variable+" "+vars_unit,width=200,height=400)
            fm.yaxis.visible = False
        else:
            fm=figure(title=months[m],x_axis_type='datetime',width=82,height=400)
            fm.yaxis.visible = False
        fm.toolbar_location = None
        fm.title.align = 'center'

        #adjust left axis
        fm.y_range=Range1d(start=df[variable].min()-(max(df[variable])*0.1), end=df[variable].max()+(max(df[variable])*0.1))

        #ColumnDataSource
        newdates=newdf[["Year","Month","Hour","Day"]]
        newdf['dates']=pd.to_datetime(newdates)
        source3=ColumnDataSource(data=newdf)

        #add low line
        g1 = bkm.Line(x='dates', y='low',line_color='blue',line_alpha=1,line_width=2)
        g1_r = fm.add_glyph(source_or_glyph=source3, glyph=g1)

        #add high line
        g2 = bkm.Line(x='dates', y='high',line_color='red',line_alpha=1,line_width=2)
        g2_r = fm.add_glyph(source_or_glyph=source3, glyph=g2)

        #add mean line
        g3 = bkm.Line(x='dates', y='mean',line_color='orange',line_alpha=1,line_width=2)
        g3_r = fm.add_glyph(source_or_glyph=source3, glyph=g3)

        #add band
        band = Band(base='dates', lower='low', upper='high', source=source3, level='underlay', fill_alpha=0.2, fill_color = 'grey')
        b_r = fm.add_layout(band)
        
        #create data points
        df_t = df[df['Month']==m+1].copy()
        df_t['Day'] = [1 for d in range(len(df_t['Day']))]
        newdates_t=df_t[["Year","Month","Day","Hour"]]
        df_t['dates']=pd.to_datetime(newdates_t)
        source = ColumnDataSource(df_t)
        g4=bkm.Circle(x='dates',y=variable,size=0.5,fill_color='black')
        g4_r = fm.add_glyph(source_or_glyph=source, glyph=g4)

        #add hover tools
        g1_hover = bkm.HoverTool(renderers=[g1_r], tooltips=[('Min', '@low{0.0}°C'),('Hour', '@dates{%H:%M}')],formatters={'@dates':'datetime'})
        g2_hover = bkm.HoverTool(renderers=[g2_r], tooltips=[('Max', '@high{0.0}°C'),('Hour', '@dates{%H:%M}')],formatters={'@dates':'datetime'})
        g3_hover = bkm.HoverTool(renderers=[g3_r], tooltips=[('Mean', '@mean{0.0}°C'),('Hour', '@dates{%H:%M}')],formatters={'@dates':'datetime'})

        fm.add_tools(g1_hover)
        fm.add_tools(g2_hover)
        fm.add_tools(g3_hover)
        
        #formatting axes and tooolbar
        fm.x_range = DataRange1d(range_padding=0.03)
        fm.xaxis.formatter = DatetimeTickFormatter(days='',hours="%Hh")
        fm.xaxis.ticker=DatetimeTicker(desired_num_ticks=4)
        fm.yaxis.ticker=DatetimeTicker(desired_num_ticks=12)
        fm.axis.major_tick_in=0
        fm.axis.axis_line_width=2
        fm.yaxis.minor_tick_line_color=None
        fm.toolbar.logo=None
        figures.append(fm)
    
    p = gridplot([figures],merge_tools=True, width= 80, height=300,sizing_mode='stretch_width',toolbar_location=None)
    return p