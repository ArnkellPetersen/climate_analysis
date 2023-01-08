import bokeh.models as bkm
from bokeh.plotting import figure
from bokeh.models.tools import SaveTool
from bokeh.models import ColumnDataSource, LinearAxis, Range1d, DataRange1d, DatetimeTickFormatter
from datetime import timedelta
from bokeh.models.tickers import DatetimeTicker

def lineGraph(df, var1='DB',var2='RH'):
    #ColumnDataSource
    source2 = ColumnDataSource(data=df[[var1,var2,'dates']])

    #initiate bokeh figure and tols
    tools=[SaveTool(),'reset','xwheel_zoom']
    f2=figure(x_range=Range1d(df['dates'][0],df['dates'][8759],bounds="auto"),y_axis_label='Dry-Bulb Temperature (°C)',x_axis_type='datetime',width=1050,height=400, tools=tools, active_scroll='xwheel_zoom')

    #adjust left axis
    f2.y_range=Range1d(start=df['DB'].min()-2, end=df['DB'].max()+2)

    #add first line
    g1 = bkm.Line(x='dates', y=var1,line_color='orange',line_alpha=0.5)
    g1_r = f2.add_glyph(source_or_glyph=source2, glyph=g1)

    #add second axis
    f2.add_layout(LinearAxis(y_range_name='second',axis_label='Relative Humidity (%)',axis_label_text_color='green',axis_label_text_alpha=0.5), 'right')
    f2.extra_y_ranges = {'second': Range1d(start=0, end=100)}

    #add second line
    g2 = bkm.Line(x='dates', y=var2,line_color='green',line_alpha=0.5)
    g2_r = f2.add_glyph(source_or_glyph=source2, glyph=g2,y_range_name='second')

    #add hover tools
    g1_hover = bkm.HoverTool(renderers=[g1_r], tooltips=[('Date', '@dates{%b-%d %H:%M}'),(var1, '@DB{0.0}°C')],formatters={'@dates':'datetime'})
    g2_hover = bkm.HoverTool(renderers=[g2_r], tooltips=[('Date', '@dates{%b-%d %H:%M}'),(var2, '@RH{0.0}%')],formatters={'@dates':'datetime'})
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