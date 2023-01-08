from bokeh.plotting import figure
import numpy as np
from bokeh.models.tools import HoverTool, BoxSelectTool, SaveTool, ResetTool, PanTool
from bokeh.models.mappers import LinearColorMapper
from bokeh.models.tickers import BasicTicker,DatetimeTicker
from bokeh.models.annotations import Label
from bokeh.models import BoxAnnotation, ColumnDataSource, DataRange1d, ColorBar, NumeralTickFormatter

def heatmap(df):
    m_names=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    m_days=[31,28,31,30,31,30,31,31,30,31,30,31]
    hoverTool=HoverTool(tooltips=[('Date','@dates{%b-%d %H:%M}'),('Temp','@DB{0.0}°C')],formatters={'@dates':'datetime'})
    baseBoxAnnotationLine=BoxAnnotation(top=18.5,top_units='data',bottom=5.5,bottom_units='data', fill_color=None, line_dash=[5,5],line_width=2, line_color='black')
    baseBoxAnnotationFill1=BoxAnnotation(top=24.5,top_units='data',bottom=18.5,bottom_units='data', fill_color='white', fill_alpha=0.4)
    baseBoxAnnotationFill2=BoxAnnotation(top=0.5,top_units='data',bottom=5.5,bottom_units='data', fill_color='white', fill_alpha=0.4)

    boxAnnotation=BoxAnnotation(fill_color=None, line_dash=[5,5],line_width=2, line_color='black')
    boxSelectTool=BoxSelectTool(overlay=boxAnnotation,dimensions='height')
    selecText = Label(x=3, y=5.5, text='Occupied Time',text_font_size='13px')

    tools=[hoverTool,SaveTool(),'xwheel_zoom',ResetTool(),PanTool(dimensions='width'),boxSelectTool]

    days=[]
    cum_days = np.cumsum(m_days)
    cum_days = list(cum_days[:-1])
    cum_days.insert(0,0)

    for i,day in enumerate(df['Day']):
        month = df['Month'][i]
        days.append(day+cum_days[month-1])

    df['days'] = days

    factors_x = [1,365]
    factors_y = [1,24]
    colors = ["#75968f", "#a5bab7", "#c9d9d3", "#e2e2e2", "#dfccce", "#ddb7b1", "#cc7878", "#933b41", "#550b1d"]
    mapper = LinearColorMapper(palette=colors, low=min(df['DB']), high=max(df['DB']))

    source=ColumnDataSource(data=df)
    f4 = figure(title="Heatmap", tools=tools, x_range=factors_x, y_range=factors_y,width=950,height=300, active_scroll='xwheel_zoom')
    f4.rect(x='days', y='Hour', line_color=None,width=1,width_units='data',height=1,fill_color={'field': 'DB', 'transform': mapper},source=source,name='rects')

    f4.ygrid.grid_line_color = None
    f4.yaxis.minor_tick_line_color=None
    f4.xaxis.minor_tick_line_color=None
    f4.toolbar.logo = None
    f4.axis.major_tick_in = 0
    f4.axis.axis_line_width = 0
    f4.yaxis.ticker = DatetimeTicker(desired_num_ticks=5)
    f4.x_range = DataRange1d(range_padding=0.002)
    f4.y_range = DataRange1d(range_padding=0.002)

    f4.yaxis.ticker = [1,6,12,18,24]
    f4.xaxis.ticker = [x+1 for x in cum_days]

    month_iter = []
    for d in range(365):
        for i,m in enumerate(cum_days):
            if i<11:
                if d>m and d<=cum_days[i+1]:
                    month_iter.append(m_names[i])
            else:
                if d>m:
                    month_iter.append(m_names[-1])

    zip_iterator = zip([*range(365)],list(month_iter))
    f4.xaxis.major_label_overrides = dict(zip_iterator)

    color_bar = ColorBar(color_mapper=mapper, major_label_text_font_size="7px",
                        ticker=BasicTicker(desired_num_ticks=len(colors)),
                        formatter=NumeralTickFormatter(format='0.0'),
                        label_standoff=6, border_line_color=None)

    f4.add_layout(color_bar, 'right')
    f4.add_layout(selecText)
    f4.add_layout(baseBoxAnnotationLine)
    f4.add_layout(baseBoxAnnotationFill1)
    f4.add_layout(baseBoxAnnotationFill2)
    return f4