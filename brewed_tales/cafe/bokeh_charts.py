
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.resources import CDN
from bokeh.layouts import column
import pandas as pd
from bokeh.models import HoverTool
from bokeh.palettes import Spectral11

def generate_top_customers_bar_chart(df):
    # Перевірка колонок
    print(df.columns)

    p = figure(x_range=df['customer'], title="Top Customers by Orders", toolbar_location="above", tools="pan,box_zoom,reset,hover,save")

    # Додавання стовпців
    p.vbar(x=df['customer'], top=df['orders'], width=0.9, color=Spectral11[0])

    # Налаштування інструментів
    hover = HoverTool()
    hover.tooltips = [("Customer", "@customer"), ("Orders", "@orders")]
    p.add_tools(hover)

    # Налаштування зовнішнього вигляду
    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    p.xaxis.major_label_orientation = 1  # Поворот етикеток на осі X

    # Налаштування відображення
    p.yaxis.axis_label = 'Number of Orders'
    p.xaxis.axis_label = 'Customer'

    return p