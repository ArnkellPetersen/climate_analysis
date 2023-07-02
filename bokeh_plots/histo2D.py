import pandas as pd
import numpy as np
from bokeh.layouts import gridplot
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, SaveTool, WheelZoomTool, HoverTool, ResetTool, PanTool, BoxSelectTool, CustomJS
from bokeh.models.mappers import LinearColorMapper
from bokeh.palettes import Turbo256
from bokeh.models import CustomJS

col_names=['Year','Month','Day','Hour','Seconds','Datasource','DryBulb','DewPoint','RelativeHumidity','AtmPressure','ExtHorzRad','ExtDirRad','HorzIRSky', 'GlobalHorizontalRadiation', 'DirectNormalRadiation','DiffuseHorizontalRadiation','GloHorzIllum','DirNormIllum','DifHorzIllum','ZenLum','WindDir','WindSpeed','TotSkyCvr','OpaqSkyCvr','Visibility','CeilingHgt','PresWeathObs,PresWeathCodes','PrecipWtr','AerosolOptDepth','SnowDepth','DaysLastSnow','Albedo','Rain','RainQuantity','-']
units = ["YYYY","MM","DD","HH","s","","°C","°C","%","Pa","Wh/m2","Wh/m2","Wh/m2","Wh/m2","Wh/m2","Wh/m2","lux","lux","lux","Cd/m2","°","m/s","","","km","m","","","mm","thousandths","cm","","","mm","hr"]
options = ['DryBulb','RelativeHumidity','DewPoint','WindSpeed','GlobalHorizontalRadiation','DirectNormalRadiation','DiffuseHorizontalRadiation']
bins = [1,1,1,1,10,10,10]
vars_rescale = ['GlobalHorizontalRadiation','DirectNormalRadiation','DiffuseHorizontalRadiation']

def histo2D(df, variables):
    var1 = variables[0]
    var2 = variables[1]

    units_idx = [col_names.index(x)for x in variables]
    vars_units = [units[x] for x in units_idx]
    bins_idx = [options.index(x)for x in variables]
    vars_bins = [bins[x] for x in bins_idx]

    #2d histogram
    min_x = int(df[var1].min())
    max_x = int(df[var1].max())
    min_y = int(df[var2].min())
    max_y = int(df[var2].max())
    xrange = int((max_x - min_x)/vars_bins[0])
    yrange = int((max_y - min_y)/vars_bins[1])

    if var1 in vars_rescale:
            mask = df[var1]>10 
            x = df[var1][mask]
            y = df[var2][mask]
    elif var2 in vars_rescale:
            mask = df[var2]>10 
            x = df[var1][mask]
            y = df[var2][mask]
    else:
        x = df[var1]
        y = df[var2]

    H, xedges, yedges = np.histogram2d(x, y, bins=[xrange,yrange], range=[[min_x,max_x],[min_y,max_y]])

    H_df = pd.DataFrame(H)
    H_flat = H.flatten()
    x_ = []
    y_ = []

    x_bins = [min_x+x*vars_bins[0] for x in range(xrange)]
    y_bins = [min_y+y*vars_bins[1] for y in range(yrange)]

    for i in x_bins:
        for a in y_bins:
            x_.append(i)
            y_.append(a)

    data=pd.DataFrame({'x':x_,'y':y_,'hist':H_flat,'percent':H_flat/len(x)*100})
    source=ColumnDataSource(data=data)

    wheelZoomTool=WheelZoomTool(dimensions='width')
    hoverTool=HoverTool(tooltips=[(variables[0],'@'+'x'+'{0.0}'+vars_units[0]),(variables[1],'@'+'y'+'{0.0}'+vars_units[1]),('Percentage','@percent{0.0}%')])
    tools=[hoverTool,SaveTool(),wheelZoomTool,ResetTool(),PanTool(),BoxSelectTool()]

    factors_x = [min_x,max_x]
    factors_y = [min_y,max_y]

    mapper_main = LinearColorMapper(palette=Turbo256, low=min(H_flat), high=max(H_flat))

    f5=figure(width=700,height=450,x_axis_label=variables[0]+" "+vars_units[0], y_axis_label=variables[1]+" "+vars_units[1],
            x_range=factors_x, y_range=factors_y,tools=tools,toolbar_location='above')
    f5.rect(x='x',y='y',line_color='white',line_alpha=0.2,width=vars_bins[0],width_units='data',height=vars_bins[1],fill_color={'field': 'hist', 'transform': mapper_main},source=source)

    #tools for hist
    hoverTool_y=HoverTool(tooltips=[(var2,'@left{0.0}'+vars_units[1]),('Percentage','@percent{0.0}%')])
    tools_y=[hoverTool_y,SaveTool(),ResetTool(),PanTool()]

    hoverTool_x=HoverTool(tooltips=[(var1,'@left{0.0}'+vars_units[0]), ('Percentage','@percent{0.0}%')])
    tools_x=[hoverTool_x,SaveTool(),ResetTool(),PanTool()]

    #1d histogram y
    hist_y, edges_y = np.histogram(y,bins=yrange, range=[min_y,max_y])
    rh_hist_data = pd.DataFrame({'occur': hist_y, 
                        'left': edges_y[:-1], 
                        'right': edges_y[1:],
                        'percent': hist_y/len(y)*100})
    zeros_y = np.zeros(len(edges_y)-1)

    source_y = ColumnDataSource(rh_hist_data)
    mapper_y = LinearColorMapper(palette=Turbo256,low=min(hist_y) ,high=max(hist_y))
    # y_range = Range1d(f5.y_range.start+vars_bins[1]/2,f5.y_range.end+vars_bins[1]/2)
    fv = figure(height = f5.height, width = 150, toolbar_location=None, y_range=f5.y_range,y_axis_location="right",tools=tools_y)
    fv1 = fv.quad(left=0, right='occur', top='left', bottom='right', fill_color={'field': 'occur', 'transform': mapper_y}, alpha = 1, line_color='white', source=source_y)
    # fv2 = fv.quad(left=0, right='occur', top='left', bottom='right', fill_color={'field': 'occur', 'transform': mapper_y}, alpha = 0.5, line_color='white', source=source_y)

    #1d histogram x
    hist_x, edges_x = np.histogram(x,bins = xrange, range = [min_x,max_x])
    temps_hist_data = pd.DataFrame({'occur': hist_x, 
                        'left': edges_x[:-1], 
                        'right': edges_x[1:],
                        'percent': hist_x/len(x)*100})

    zeros_x = np.zeros(len(edges_x)-1)

    source_x = ColumnDataSource(temps_hist_data)
    mapper_x = LinearColorMapper(palette=Turbo256,low=min(hist_x) ,high=max(hist_x))
    # x_range = Range1d(f5.x_range.start+vars_bins[0]/2,f5.x_range.end+vars_bins[0]/2)
    fh = figure(height = 150, width = f5.width, toolbar_location=None, x_range=f5.x_range, tools= tools_x)
    fh1 = fh.quad(bottom=0, top='occur', left='left', right='right', fill_color={'field': 'occur', 'transform': mapper_x}, alpha = 1, line_color='white',source=source_x)
    # fh2 = fh.quad(bottom=0, top='occur', left='left', right='right', fill_color={'field': 'occur', 'transform': mapper_x}, alpha = 0.5, line_color='white',source=source_x)

    layout = gridplot([[f5, fv], [fh, None]], merge_tools=True)
    return layout
