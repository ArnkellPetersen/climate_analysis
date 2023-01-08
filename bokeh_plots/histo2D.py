import pandas as pd
import numpy as np
from bokeh.layouts import gridplot
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, SaveTool, WheelZoomTool, HoverTool, ResetTool, PanTool, BoxSelectTool, BoxAnnotation
from bokeh.models.mappers import LinearColorMapper

def histo2D(df):
    y=[x for x in range(80)]
    H, xedges, yedges = np.histogram2d(df['DB'], df['RH'], bins=[40,80], range=[[-5, 35],[20,100]])

    H_df=pd.DataFrame(H,columns=y)
    H_flat=H.flatten()
    x_=[]
    y_=[]
    for i in range(-5,35):
        for a in range(20,100):
            x_.append(i)
            y_.append(a)
           
    data=pd.DataFrame({'x':x_,'y':y_,'hist':H_flat})
    source=ColumnDataSource(data=data)

    boxAnnotation=BoxAnnotation(fill_color=None, line_dash=[5,5],line_width=2, line_color='black')
    boxSelectTool=BoxSelectTool(overlay=boxAnnotation,dimensions='height')
    wheelZoomTool=WheelZoomTool(dimensions='width')
    hoverTool=HoverTool(tooltips=[('Temp','@x{0.0}°C'),('Relative Humidity','@y{0.0}%'),('Count','@hist{0.0}')])
    tools=[hoverTool,SaveTool(),wheelZoomTool,ResetTool(),PanTool(),boxSelectTool]

    factors_x = [-5,35]
    factors_y = [20,100]
    colors = ["#75968f", "#a5bab7", "#c9d9d3", "#e2e2e2", "#dfccce", "#ddb7b1", "#cc7878", "#933b41", "#550b1d"]
    mapper = LinearColorMapper(palette=colors, low=0, high=max(H_flat))

    f5=figure(title="Dry Bulb vs RH", x_axis_label='Dry-Bulb Temperature (C)', y_axis_label='Relative Humidity (%)',
            x_range=factors_x, y_range=factors_y,tools=tools,toolbar_location='above')
    f5.rect(x='x',y='y', line_color='black',width=1,width_units='data', height=1,fill_color={'field': 'hist', 'transform': mapper},source=source)

    #1d histogram RH
    arr_hist, edges = np.histogram(df['RH'],bins = int(100/5), range = [20,100])
    rh_hist_data = pd.DataFrame({'occur': arr_hist, 
                        'left': edges[:-1], 
                        'right': edges[1:]})
    frh = figure(height = f5.height, width = 200, toolbar_location=None, y_range=f5.y_range,
            y_axis_label = 'Number of occurrences',y_axis_location="right")
    frh.quad(left=0, right=rh_hist_data['occur'], 
        top=rh_hist_data['left'], bottom=rh_hist_data['right'], 
        fill_color='blue', line_color='black')
    frh.yaxis.major_label_orientation = np.pi/4

    #1d histogram temp
    arr_hist, edges = np.histogram(df['DB'],bins = int(40/1), range = [-5, 35])
    temps_hist_data = pd.DataFrame({'occur': arr_hist, 
                        'left': edges[:-1], 
                        'right': edges[1:]})

    ftemp = figure(height = 200, width = f5.width, toolbar_location=None, x_range=f5.x_range,
            title = 'Histogram of Temps',
            x_axis_label = 'Temp (deg)', 
            y_axis_label = 'Number of occurrences',y_axis_location="right")
    ftemp.quad(bottom=0, top=temps_hist_data['occur'], 
        left=temps_hist_data['left'], right=temps_hist_data['right'], 
        fill_color='blue', line_color='black')

    layout = gridplot([[f5, frh], [ftemp, None]], merge_tools=False)
    return layout