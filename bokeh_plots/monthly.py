import pandas as pd
import bokeh.models as bkm
from bokeh.plotting import figure
from datetime import timedelta
from bokeh.models import ColumnDataSource, DatetimeTickFormatter, SaveTool, Range1d, DataRange1d
from bokeh.models.tickers import DatetimeTicker

col_names=['Year','Month','Day','Hour','Seconds','Datasource','DryBulb','DewPoint','RelativeHumidity','AtmPressure','ExtHorzRad','ExtDirRad','HorzIRSky', 'GlobalHorizontalRadiation', 'DirectNormalRadiation','DiffuseHorizontalRadiation','GloHorzIllum','DirNormIllum','DifHorzIllum','ZenLum','WindDir','WindSpeed','TotSkyCvr','OpaqSkyCvr','Visibility','CeilingHgt','PresWeathObs,PresWeathCodes','PrecipWtr','AerosolOptDepth','SnowDepth','DaysLastSnow','Albedo','Rain','RainQuantity','-']
units = ["YYYY","MM","DD","HH","s","","°C","°C","%","Pa","Wh/m2","Wh/m2","Wh/m2","Wh/m2","Wh/m2","Wh/m2","lux","lux","lux","Cd/m2","°","m/s","","","km","m","","","mm","thousandths","cm","","","mm","hr"]


def monthly(df,variable):
    #initiate bokeh figure and tools
    vars_unit = units[col_names.index(variable)]

    #initiate bokeh figure and tools
    tools=[SaveTool(),'reset']
    f3=figure(y_axis_label=variable+" "+vars_unit,x_axis_type='datetime',width=950,height=500, tools=tools)

    #calculate monthly stats
    month_low=[]
    month_high=[]
    month_mean=[]
    month_25pc=[]
    month_25pc_height=[]
    month_25pc_centre=[]
    month_75pc=[]
    month_75pc_height=[]
    month_75pc_centre=[]
    month=[]
    year=[]
    day=[]

    for i in range(12):
        year.append(2000)
        day.append(1)
        month.append(i+1)
        month_values=df[df['Month']==i+1][variable]
        stats=month_values.describe()
        val_25pc=stats['25%']
        val_75pc=stats['75%']
        val_mean=stats['mean']
        month_25pc.append(val_25pc)
        month_75pc.append(val_75pc)
        month_75pc_height.append((val_75pc-val_mean))
        month_75pc_centre.append(val_mean+(val_75pc-val_mean)/2)
        month_25pc_height.append((val_mean-val_25pc))
        month_25pc_centre.append(val_mean-(val_mean-val_25pc)/2)
        month_high.append(stats['max'])
        month_low.append(stats['min'])
        month_mean.append(val_mean)

    newdf=pd.DataFrame({'Year':year,
                        'Month':month,
                        'Day':day,
                        'low': month_low,
                        'high': month_high,
                        'mean': month_mean,
                        '25pc': month_25pc,
                        '75pc': month_75pc,
                        '75pc_centre': month_75pc_centre,
                        '75pc_height': month_75pc_height,
                        '25pc_centre': month_25pc_centre,
                        '25pc_height': month_25pc_height})

    #ColumnDataSource
    newdates=newdf[["Year","Month","Day"]]
    newdf['dates']=pd.to_datetime(newdates)
    source3=ColumnDataSource(data=newdf)

    #adjust left axis
    f3.y_range=Range1d(start=newdf['low'].min()-(max(newdf['high'])*0.1), end=newdf['high'].max()+(max(newdf['high'])*0.1))

    #add low line
    g1 = bkm.Line(x='dates', y='low',line_color='blue',line_alpha=0.5,line_width=3)
    g1_r = f3.add_glyph(source_or_glyph=source3, glyph=g1)
    f3.circle(x='dates',y='low',size=8,color='blue',source=source3)

    #add high line
    g2 = bkm.Line(x='dates', y='high',line_color='orange',line_alpha=0.5,line_width=3)
    g2_r = f3.add_glyph(source_or_glyph=source3, glyph=g2)
    f3.circle(x='dates',y='high',size=8,color='orange',source=source3)

    #add mean line
    g3 = bkm.Line(x='dates', y='mean',line_color='green',line_alpha=0.5,line_width=3)
    g3_r = f3.add_glyph(source_or_glyph=source3, glyph=g3)

    #add bars
    g4=bkm.Rect(x='dates',y='mean',width=20,height=0.5,height_units='data',
                width_units='screen',fill_color='green',line_color='green')
    g4_r = f3.add_glyph(source_or_glyph=source3, glyph=g4)
    g5=bkm.Rect(x='dates',y='75pc_centre',width=20,height='75pc_height',
                height_units='data',width_units='screen',fill_color='green',
                fill_alpha=0.3,line_color='green',line_alpha=0.6,line_width=3)
    g5_r = f3.add_glyph(source_or_glyph=source3, glyph=g5)
    g6=bkm.Rect(x='dates',y='25pc_centre',width=20,height='25pc_height',
                height_units='data',width_units='screen',fill_color='green',
                fill_alpha=0.3,line_color='green',line_alpha=0.6,line_width=3)
    g6_r = f3.add_glyph(source_or_glyph=source3, glyph=g6)
    g7=bkm.Circle(x='dates',y='25pc',size=8,fill_color='green',line_color='green')
    g7_r = f3.add_glyph(source_or_glyph=source3, glyph=g7)
    g8=bkm.Circle(x='dates',y='75pc',size=8,fill_color='green',line_color='green')
    g8_r = f3.add_glyph(source_or_glyph=source3, glyph=g8)

    #add hover tools
    g1_hover = bkm.HoverTool(renderers=[g1_r], tooltips=[('Month', '@dates{%B}'),('Min', '@low{0.0}°C')],formatters={'@dates':'datetime'})
    g2_hover = bkm.HoverTool(renderers=[g2_r], tooltips=[('Month', '@dates{%B}'),('Max', '@high{0.0}°C')],formatters={'@dates':'datetime'})
    g3_hover = bkm.HoverTool(renderers=[g3_r], tooltips=[('Month', '@dates{%B}'),('Mean', '@mean{0.0}°C')],formatters={'@dates':'datetime'})
    g7_hover = bkm.HoverTool(renderers=[g7_r], tooltips=[('Month', '@dates{%B}'),('25th percentile', '@25pc{0.0}°C')],formatters={'@dates':'datetime'})
    g8_hover = bkm.HoverTool(renderers=[g8_r], tooltips=[('Month', '@dates{%B}'),('75th percentile', '@75pc{0.0}°C')],formatters={'@dates':'datetime'})

    f3.add_tools(g1_hover)
    f3.add_tools(g2_hover)
    f3.add_tools(g3_hover)
    f3.add_tools(g7_hover)
    f3.add_tools(g8_hover)

    #formatting axes and tooolbar
    f3.x_range = DataRange1d(range_padding=0.03)
    f3.xaxis.formatter = DatetimeTickFormatter(months="%b",days="%b-%d")
    f3.xaxis.ticker=DatetimeTicker(desired_num_ticks=12)
    f3.yaxis.ticker=DatetimeTicker(desired_num_ticks=12)
    # f3.xaxis.axis_label_text_align='right'
    x_range=Range1d(newdf['dates'][0], newdf['dates'][11])
    f3.x_range.min_interval = timedelta(days=90)
    f3.x_range.max_interval = timedelta(days=340)
    f3.axis.major_tick_in=0
    f3.axis.axis_line_width=2
    f3.ygrid.grid_line_color = None
    f3.yaxis.minor_tick_line_color=None
    f3.toolbar.logo=None
    return f3