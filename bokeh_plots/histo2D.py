import pandas as pd
import numpy as np
from bokeh.layouts import gridplot
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, SaveTool, WheelZoomTool, HoverTool, ResetTool, PanTool, BoxSelectTool, CustomJS
from bokeh.models.mappers import LinearColorMapper
from bokeh.palettes import Turbo256

def histo2D(df, variables):
    #2d histogram
    x = df['DB']
    y = df['TotSkyCvr']
    min_x = int(x.min())
    max_x = int(x.max())
    min_y = int(y.min())
    max_y = int(y.max())
    xrange = max_x - min_x +1
    yrange = max_y - min_y +1
    H, xedges, yedges = np.histogram2d(x, y, bins=[xrange,yrange], range=[[min_x,max_x],[min_y,max_y]])

    H_flat=H.flatten()
    x_=[]
    y_=[]
    for i in range(min_x,max_x):
        for a in range(min_y,max_y):
            x_.append(i)
            y_.append(a)

    data=pd.DataFrame({'x':x_,'y':y_,'hist':H_flat})
    source=ColumnDataSource(data=data)

    wheelZoomTool=WheelZoomTool(dimensions='width')
    hoverTool=HoverTool(tooltips=[('Temp','@x°C'),('Relative Humidity','@y%'),('Count','@hist')])
    tools=[hoverTool,SaveTool(),wheelZoomTool,ResetTool(),PanTool(),BoxSelectTool()]
    print(max_y)
    #tools for hist
    hoverTool_y=HoverTool(tooltips=[('RH','@left%'),('Count','@occur')])
    tools_y=[hoverTool_y,SaveTool(),ResetTool(),PanTool()]

    hoverTool_x=HoverTool(tooltips=[('Temp','@left{0.0}°C'), ('Count','@occur')])
    tools_x=[hoverTool_x,SaveTool(),ResetTool(),PanTool()]

    factors_x = [min_x,max_x]
    factors_y = [min_y,max_y]
    print(factors_y)
    mapper_main = LinearColorMapper(palette=Turbo256, low=H.min(), high=H.max())

    f5=figure(height =550, width = 800, x_axis_label='Dry-Bulb Temperature (C)', y_axis_label='Relative Humidity (%)',
            x_range=factors_x, y_range=factors_y,tools=tools,toolbar_location='above')
    f5.rect(x='x',y='y',width=1,width_units='data', height=1,fill_color={'field': 'hist', 'transform': mapper_main},source=source)


    #1d histogram y
    hist_y, edges_y = np.histogram(y, bins = yrange, range = [min_y,max_y])
    rh_hist_data = pd.DataFrame({'occur': hist_y, 
                        'left': edges_y[:-1], 
                        'right': edges_y[1:]})
    zeros_y = np.zeros(len(edges_y)-1)

    source_y = ColumnDataSource(rh_hist_data)
    mapper_y = LinearColorMapper(palette=Turbo256,low=0 ,high=max(hist_y))
    fv = figure(height = f5.height, width = 200, toolbar_location=None, y_range=f5.y_range,y_axis_location="right",tools=tools_y)
    fv1 = fv.quad(left=0, right='occur', top='left', bottom='right', fill_color={'field': 'occur', 'transform': mapper_y}, alpha = 1, line_color='black', source=source_y)
    fv2 = fv.quad(left=0, right='occur', top='left', bottom='right', fill_color={'field': 'occur', 'transform': mapper_y}, alpha = 0.5, line_color='black', source=source_y)

    #1d histogram x
    hist_x, edges_x = np.histogram(x,bins = xrange, range = [min_x,max_x])
    temps_hist_data = pd.DataFrame({'occur': hist_x, 
                        'left': edges_x[:-1], 
                        'right': edges_x[1:]})

    zeros_x = np.zeros(len(edges_x)-1)

    source_x = ColumnDataSource(temps_hist_data)
    mapper_x = LinearColorMapper(palette=Turbo256,low=0 ,high=max(hist_x))
    fh = figure(height = 200, width = f5.width, toolbar_location=None, x_range=f5.x_range, tools= tools_x)
    fh1 = fh.quad(bottom=0, top='occur', left='left', right='right', fill_color={'field': 'occur', 'transform': mapper_x}, alpha = 1, line_color='black',source=source_x)
    fh2 = fh.quad(bottom=0, top='occur', left='left', right='right', fill_color={'field': 'occur', 'transform': mapper_x}, alpha = 0.5, line_color='black',source=source_x)

    source.selected.js_on_change('indices', CustomJS(args = dict(s = source, sx = source_x, sy = source_y), code = """
            const inds = cb_obj.indices;
            const d1 = s1.data;
            // let d2 = {'x': []}
            let d2 = {'y1': [],'y2': []}

            if (inds.length == 0)
                return;

            // for (let i = 0; i < inds.length; i++) {
            //     d2['x'].push(d1['x'][inds[i]])
            // }
            for (let i = 0; i < inds.length; i++) {
                if (d1['x'][inds[i]] <0.5) {
                    d2['y1'].push(d1['x'][inds[i]])
                } else {
                    d2['y2'].push(d1['x'][inds[i]])
                }
            }
            // console.log(d2['x'].length)
            // s2.data['x1'] = [d2['x'].length,d2['x'].length]
            s2.data['x1'] = [d2['y1'].length,d2['y2'].length]

            s1.change.emit();
            s2.change.emit();  """))

    layout = gridplot([[f5, fv], [fh, None]], merge_tools=True)
    
    return layout