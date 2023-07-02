from bokeh.plotting import figure, show
from bokeh.models.mappers import LinearColorMapper, CategoricalColorMapper
from bokeh.models.tickers import DatetimeTicker
from bokeh.models.annotations import Label
from bokeh.models import BoxAnnotation, HoverTool, WheelZoomTool, BoxSelectTool, SaveTool, ResetTool, PanTool, ColumnDataSource, DataRange1d, ColorBar
from pythermalcomfort.models import utci, solar_gain
import bokeh.models as bkm
import numpy as np

def utciHeatmap(df):
    m_names=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    m_days=[31,28,31,30,31,30,31,31,30,31,30,31]
    db = df['DryBulb']
    rh = df['RelativeHumidity']
    dirSolar = df['DirectNormalRadiation']
    windSpeed = df['WindSpeed']
    #calculate MRT and UTCI
    sol_tr = 1
    df['delta_mrt'] = solar_gain(45, 90, dirSolar, sol_tr, 1, 0.5, asw=0.7, posture='seated', floor_reflectance=0.6)['delta_mrt']
    df['mrt'] = db+df['delta_mrt']
    df['utci_cat'] = utci(db,df['mrt'],windSpeed,rh,return_stress_category=True,limit_inputs=False)['stress_category']
    df['utci'] = utci(db,df['mrt'],windSpeed,rh,return_stress_category=True,limit_inputs=False)['utci']

    hoverTool=HoverTool(tooltips=[('Date','@dates{%b-%d %H:%M}'),('UTCI Cat','@utci_cat')],formatters={'@dates':'datetime'})
    wheelZoomTool=WheelZoomTool(dimensions='width')
    boxAnnotation=BoxAnnotation(fill_color=None, line_dash=[5,5],line_width=2, line_color='black')
    boxSelectTool=BoxSelectTool(overlay=boxAnnotation,dimensions='height')

    baseBoxAnnotationLine=BoxAnnotation(top=18.5,top_units='data',bottom=5.5,bottom_units='data', 
                                        fill_color=None, line_dash=[5,5],line_width=2, line_color='black')
    baseBoxAnnotationFill1=BoxAnnotation(top=24.5,top_units='data',bottom=18.5,bottom_units='data', 
                                        fill_color='white', fill_alpha=0.4)
    baseBoxAnnotationFill2=BoxAnnotation(top=0.5,top_units='data',bottom=5.5,bottom_units='data', 
                                        fill_color='white', fill_alpha=0.4)

    selecText = Label(x=3, y=5.5, text='Occupied Time',text_font_size='13px')

    tools=[hoverTool,SaveTool(),wheelZoomTool,ResetTool(),PanTool(dimensions='width'),boxSelectTool]

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
    colors = ["#1d278c", "#1d3e8c", "#1d4f8c", "#1d638c", "#1d7a8c", "#1d8c74", "#c4aa27", "#c49527", "#c48027",'#c45e27']
    utci_cats_titles = ['Extreme Cold Stress','Very Strong Cold Stress','Strong Cold Stress','Moderate Cold Stress','Slight Cold Stress', 'No Thermal Stress', 'Moderate Heat Stress','Strong Heat Stress','Very Strong Heat Stress','Extreme Heat Stress']
    utci_cats = ['extreme cold stress','very strong cold stress','strong cold stress','moderate cold stress','slight cold stress', 'no thermal stress', 'moderate heat stress','strong heat stress','very strong heat stress','extreme heat stress']
    mapper = LinearColorMapper(palette=colors, low=-40, high=50)
    catmapper_titles = CategoricalColorMapper(palette=colors, factors=utci_cats_titles)
    catmapper= CategoricalColorMapper(palette=colors, factors=utci_cats)

    source=ColumnDataSource(data=df)
    f4 = figure(tools=tools, x_range=factors_x, y_range=factors_y,
                width=950,height=300)
    r1=f4.rect(x='days', y='Hour', line_color=None,width=1,width_units='data',
            height=1,fill_color={'field': 'utci_cat', 'transform': catmapper},
            source=source,name='rects')

    selection_glyph=bkm.Rect(fill_color={'field': 'utci_cat', 'transform': catmapper},fill_alpha=1,line_color=None)
    nonselection_glyph=bkm.Rect(line_color=None,fill_color={'field': 'utci_cat', 'transform': catmapper},fill_alpha=0.4)
    r1.selection_glyph = selection_glyph
    r1.nonselection_glyph = nonselection_glyph

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

    color_bar = ColorBar(color_mapper=catmapper_titles, major_label_text_font_size="7px",
                        ticker='auto',
                        label_standoff=6, border_line_color=None)

    f4.add_layout(color_bar, 'right')

    Label(x=3, y=5.5, text='Occupied Time',text_font_size='13px')

    return f4