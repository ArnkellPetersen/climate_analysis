import bokeh.models as bkm
import pandas as pd
from bokeh.plotting import figure
from datetime import timedelta
from bokeh.models.tools import SaveTool
from bokeh.models import DatetimeTickFormatter, Band, DataRange1d, ColumnDataSource, Range1d
from bokeh.models.tickers import DatetimeTicker
import statistics
from datetime import timedelta

col_names=['Year','Month','Day','Hour','Seconds','Datasource','DryBulb','DewPoint','RelativeHumidity','AtmPressure','ExtHorzRad','ExtDirRad','HorzIRSky', 'GlobalHorizontalRadiation', 'DirectNormalRadiation','DiffuseHorizontalRadiation','GloHorzIllum','DirNormIllum','DifHorzIllum','ZenLum','WindDir','WindSpeed','TotSkyCvr','OpaqSkyCvr','Visibility','CeilingHgt','PresWeathObs,PresWeathCodes','PrecipWtr','AerosolOptDepth','SnowDepth','DaysLastSnow','Albedo','Rain','RainQuantity','-']
units = ["YYYY","MM","DD","HH","s","","°C","°C","%","Pa","Wh/m2","Wh/m2","Wh/m2","Wh/m2","Wh/m2","Wh/m2","lux","lux","lux","Cd/m2","°","m/s","","","km","m","","","mm","thousandths","cm","","","mm","hr"]


def daily(df, variable='DryBulb'):
    

    m_days=[31,28,31,30,31,30,31,31,30,31,30,31]

    variable = 'RelativeHumidity'
    vars_unit = units[col_names.index(variable)]

    #initiate bokeh figure and tools
    tools=[SaveTool(),'reset']
    f3=figure(y_axis_label=variable+" "+vars_unit,x_axis_type='datetime',width=950,height=500, tools=tools)

    # all = []
    # for m, days in enumerate(m_days):
    #     day_sub_high = []
    #     day_sub_low = []
    #     day_sub_mean = []
    #     for h in range(24):
    #         hour_sub = []
    #         for d in range(days):
    #             hour_sub.append(df[(df['Month']==m+1) & (df['Day']==d+1) & (df['Hour']==h+1)][variable].values[0])
    #         day_sub_high.append(max(hour_sub))
    #         day_sub_low.append(min(hour_sub))
    #         day_sub_mean.append(statistics.mean(hour_sub))
    #     all_sub = [day_sub_high,day_sub_low,day_sub_mean]
    #     all.append(all_sub)
    all = []
    for m, days in enumerate(m_days):
        day_sub_high = []
        day_sub_low = []
        day_sub_mean = []
        for h in range(24):
            hour_sub = []
            for d in range(days):
                hour_sub.append(df[(df['Month']==m+1) & (df['Day']==d+1) & (df['Hour']==h+1)][variable].values[0])
            day_sub_high.append(max(hour_sub))
            day_sub_low.append(min(hour_sub))
            day_sub_mean.append(statistics.mean(hour_sub))
        all_sub = [day_sub_high,day_sub_low,day_sub_mean]
        all.append(all_sub)

    #adjust left axis
    f3.y_range=Range1d(start=df[variable].min()-5, end=df[variable].max()+5)

    for m in range(12):
        newdf = pd.DataFrame({'Year': [2000 for x in range(24)],
                        'Month': [m+1 for x in range(24)],
                        'Day': [x+3 for x in range(24)],
                        'Hour': [x for x in range(24)],
                        'high': all[m][0],
                        'low': all[m][1],
                        'mean': all[m][2]})
        
        #ColumnDataSource
        newdates=newdf[["Year","Month","Hour","Day"]]
        newdf['dates']=pd.to_datetime(newdates)
        source3=ColumnDataSource(data=newdf)

        #add low line
        g1 = bkm.Line(x='dates', y='low',line_color='blue',line_alpha=1,line_width=2)
        g1_r = f3.add_glyph(source_or_glyph=source3, glyph=g1)

        #add high line
        g2 = bkm.Line(x='dates', y='high',line_color='red',line_alpha=1,line_width=2)
        g2_r = f3.add_glyph(source_or_glyph=source3, glyph=g2)

        #add mean line
        g3 = bkm.Line(x='dates', y='mean',line_color='orange',line_alpha=1,line_width=2)
        g3_r = f3.add_glyph(source_or_glyph=source3, glyph=g3)

        #add band
        band = Band(base='dates', lower='low', upper='high', source=source3, level='underlay', fill_alpha=0.1, fill_color = 'grey')
        b_r = f3.add_layout(band)
        
        #add hover tools
        g1_hover = bkm.HoverTool(renderers=[g1_r], tooltips=[('Hour', '@dates{%H:%M}'),('Min', '@low{0.0}°C')],formatters={'@dates':'datetime'})
        g2_hover = bkm.HoverTool(renderers=[g2_r], tooltips=[('Hour', '@dates{%H:%M}'),('Max', '@high{0.0}°C')],formatters={'@dates':'datetime'})
        g3_hover = bkm.HoverTool(renderers=[g3_r], tooltips=[('Hour', '@dates{%H:%M}'),('Mean', '@mean{0.0}°C')],formatters={'@dates':'datetime'})

        f3.add_tools(g1_hover)
        f3.add_tools(g2_hover)
        f3.add_tools(g3_hover)

    #formatting axes and tooolbar
    f3.x_range = DataRange1d(range_padding=0.03)
    f3.xaxis.formatter = DatetimeTickFormatter(months="%b",days="%b-%d")
    f3.xaxis.ticker=DatetimeTicker(desired_num_ticks=12)
    f3.yaxis.ticker=DatetimeTicker(desired_num_ticks=12)
    # f3.xaxis.axis_label_text_align='right'
    f3.x_range.min_interval = timedelta(days=90)
    f3.x_range.max_interval = timedelta(days=340)
    f3.axis.major_tick_in=0
    f3.axis.axis_line_width=2
    f3.ygrid.grid_line_color = None
    f3.yaxis.minor_tick_line_color=None
    f3.toolbar.logo=None