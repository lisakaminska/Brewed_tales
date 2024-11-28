
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.resources import CDN
from bokeh.layouts import column
import pandas as pd

def generate_top_customers_bar_chart(df):
    p = figure(x_range=df['customer'], title="Top Customers by Orders", toolbar_location=None, tools="")
    p.vbar(x=df['customer'], top=df['orders'], width=0.9)
    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    return p

