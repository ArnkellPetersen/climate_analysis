import bokeh.models as bkm
from bokeh.plotting import figure
from bokeh.models.tools import SaveTool
from bokeh.models import ColumnDataSource, LinearAxis, Range1d, DataRange1d, DatetimeTickFormatter
from datetime import timedelta
from bokeh.models.tickers import DatetimeTicker

col_names=['Year','Month','Day','Hour','Seconds','Datasource','DryBulb','DewPoint','RelativeHumidity','AtmPressure','ExtHorzRad','ExtDirRad','HorzIRSky', 'GlobalHorizontalRadiation', 'DirectNormalRadiation','DiffuseHorizontalRadiation','GloHorzIllum','DirNormIllum','DifHorzIllum','ZenLum','WindDir','WindSpeed','TotSkyCvr','OpaqSkyCvr','Visibility','CeilingHgt','PresWeathObs,PresWeathCodes','PrecipWtr','AerosolOptDepth','SnowDepth','DaysLastSnow','Albedo','Rain','RainQuantity','-']
units = ["YYYY","MM","DD","HH","s","","°C","°C","%","Pa","Wh/m2","Wh/m2","Wh/m2","Wh/m2","Wh/m2","Wh/m2","lux","lux","lux","Cd/m2","°","m/s","","","km","m","","","mm","thousandths","cm","","","mm","hr"]

def hourly(df, var1='DryBulb',var2='RelativeHumidity'):
    #pick variables
    variables = [var1,var2]
    units_idx = [col_names.index(x)for x in variables]
    vars_units = [units[x] for x in units_idx]

    df0 = df[variables[0]]
    df1 = df[variables[1]]
    variables.append('dates')

    #ColumnDataSource
    source2 = ColumnDataSource(data=df[variables])

    #initiate bokeh figure and tols
    tools=[SaveTool(),'reset','xwheel_zoom']
    f2=figure(title='Hourly Values',x_range=Range1d(df['dates'][0],df['dates'][8759],bounds="auto"),y_axis_label=variables[0]+" "+vars_units[0],x_axis_type='datetime',width=950,height=500, tools=tools, active_scroll='xwheel_zoom')

    #adjust left axis
    f2.y_range=Range1d(start=df0.min()-2, end=df0.max()+2)

    #add first line
    g1 = bkm.Line(x='dates', y=variables[0],line_color='orange',line_alpha=0.5)
    g1_r = f2.add_glyph(source_or_glyph=source2, glyph=g1)

    #add second axis
    f2.add_layout(LinearAxis(y_range_name='second',axis_label=variables[1]+" "+vars_units[1],axis_label_text_color='green',axis_label_text_alpha=0.5), 'right')
    f2.extra_y_ranges = {'second': Range1d(start=df1.min()-2, end=df1.max()+2)}

    #add second line
    g2 = bkm.Line(x='dates', y=variables[1],line_color='green',line_alpha=0.5)
    g2_r = f2.add_glyph(source_or_glyph=source2, glyph=g2,y_range_name='second')

    #add hover tools
    g1_hover = bkm.HoverTool(renderers=[g1_r], tooltips=[('Date', '@dates{%b-%d %H:%M}'),(variables[0], '@'+variables[0]+'{0.0}'+vars_units[0])],formatters={'@dates':'datetime'})
    g2_hover = bkm.HoverTool(renderers=[g2_r], tooltips=[('Date', '@dates{%b-%d %H:%M}'),(variables[1], '@'+variables[1]+'{0}'+vars_units[1])],formatters={'@dates':'datetime'})
    f2.add_tools(g1_hover)
    f2.add_tools(g2_hover)

    #formatting axes and tooolbar
    f2.x_range = DataRange1d(range_padding=0.005)
    f2.yaxis.minor_tick_line_color=None
    f2.yaxis[0].axis_label_text_color='orange'
    f2.yaxis[0].axis_label_text_alpha=0.5
    f2.xaxis.formatter = DatetimeTickFormatter(months="%b",days="%b-%d")
    f2.axis.major_tick_in=0
    f2.axis.axis_line_width=2
    f2.ygrid.grid_line_color = None
    f2.xaxis.ticker=DatetimeTicker(desired_num_ticks=12)
    f2.yaxis.ticker=DatetimeTicker(desired_num_ticks=12)
    f2.x_range.min_interval = timedelta(days=2)
    f2.x_range.max_interval = timedelta(days=366)
    f2.toolbar.logo=None
    return f2