from random import random
from bokeh.models import CustomJS, ColumnDataSource, Row
from bokeh.plotting import figure 
from bokeh.io import curdoc
from bokeh.models.widgets import Button
import numpy as np

x = [random() for x in range(500)]
y = [random() for y in range(500)]

s1 = ColumnDataSource(data = dict(x = x, y = y))
p1 = figure(plot_width = 400, plot_height = 400, tools = "lasso_select", title = "Select Here")
p1.circle('x', 'y', source = s1, alpha = 0.6)

x_vbar = ['<0.5','>=0.5']
s2 = ColumnDataSource(data = dict(x1 = [0,0],x2 = x_vbar))
p2 = figure(plot_width = 400, plot_height = 400, x_range = x_vbar, title = "Watch Here")
p2.vbar(x='x2' ,top='x1',width=0.9, source = s2)

s1.selected.js_on_change('indices', CustomJS(args = dict(s1 = s1, s2 = s2), code = """
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

# s1.selected.js_on_change('indices', CustomJS(args = dict(s1 = s1, s2 = s2), code = """
#         var inds = cb_obj.indices;
#         var d1 = s1.data;
#         d2 = {'x': [], 'y': []}
#         for (var i = 0; i < inds.length; i++) {
#             d2['x'].push(d1['x'][inds[i]])
#             d2['y'].push(d1['y'][inds[i]])
#         }
#         s2.data = d2  """))

# s2.data['x1'] = [s1.data['x'][i] for i in indices]
# array = np.array(s2.data['x1'])
# less_05 = np.count_nonzero(array < 0.5)
# greater_05 = np.count_nonzero(array >= 0.5)
# x = ['<0.5','>=0.5']
# y = [less_05, greater_05]

curdoc().add_root(Row(p1, p2))