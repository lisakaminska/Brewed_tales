from bokeh.plotting import figure, output_file, save
from bokeh.models import ColumnDataSource
from bokeh.layouts import column
from bokeh.io import curdoc
from bokeh.models.widgets import DataTable, TableColumn

import pandas as pd
import os

# Директрія для збереження графіків
CHART_DIR = 'static/charts_bokeh'
os.makedirs(CHART_DIR, exist_ok=True)


def generate_top_customers_bar_chart_bokeh(df):
    source = ColumnDataSource(df)
    p = figure(x_range=df['full_name'], title="Top Customers by Orders", x_axis_label='Customers', y_axis_label='Orders')
    p.vbar(x='full_name', top='total_orders', source=source, width=0.5, color="blue")

    output_path = os.path.join(CHART_DIR, 'top_customers_bar_chart_bokeh.html')
    output_file(output_path)
    save(p)
    return p


def generate_most_popular_books_pie_chart_bokeh(df):
    df['angle'] = df['total_sold'] / df['total_sold'].sum() * 2 * 3.14159
    df['color'] = ["#f7a072", "#a0c4ff", "#ffa7a5", "#caffbf", "#ffb5e8"]

    source = ColumnDataSource(df)
    p = figure(title="Most Popular Books", toolbar_location=None, tools="hover", tooltips="@title: @total_sold")
    p.wedge(x=0, y=0, radius=0.4, start_angle='angle', end_angle='angle', color='color', source=source)

    output_path = os.path.join(CHART_DIR, 'most_popular_books_pie_chart_bokeh.html')
    output_file(output_path)
    save(p)
    return p


def generate_top_drinks_by_price_bar_chart_bokeh(df):
    source = ColumnDataSource(df)
    p = figure(y_range=df['item_name'], title="Top Drinks by Average Price", x_axis_label='Average Price', y_axis_label='Drinks')
    p.hbar(y='item_name', right='average_price', source=source, height=0.5, color="green")

    output_path = os.path.join(CHART_DIR, 'top_drinks_by_price_bar_chart_bokeh.html')
    output_file(output_path)
    save(p)
    return p


def generate_recent_orders_scatter_chart_bokeh(df):
    source = ColumnDataSource(df)
    p = figure(title="Recent Orders", x_axis_label='Date', y_axis_label='Total Amount', x_axis_type='datetime')
    p.scatter(x='order_date', y='total', source=source, size=10, color="orange")

    output_path = os.path.join(CHART_DIR, 'recent_orders_scatter_chart_bokeh.html')
    output_file(output_path)
    save(p)
    return p


def generate_customers_with_large_orders_line_chart_bokeh(df):
    source = ColumnDataSource(df)
    p = figure(title="Customers with Large Book Orders", x_axis_label='Customers', y_axis_label='Total Books')
    p.line(x='full_name', y='total_books', source=source, line_width=2, color="red")

    output_path = os.path.join(CHART_DIR, 'customers_large_orders_line_chart_bokeh.html')
    output_file(output_path)
    save(p)
    return p


def generate_orders_with_books_and_drinks_table_bokeh(df):
    source = ColumnDataSource(df)
    columns = [
        TableColumn(field="customer_name", title="Customer"),
        TableColumn(field="book_title", title="Book"),
        TableColumn(field="cafe_item", title="Drink"),
        TableColumn(field="price", title="Price"),
        TableColumn(field="quantity", title="Quantity"),
    ]
    data_table = DataTable(source=source, columns=columns, width=800, height=280)

    return data_table
