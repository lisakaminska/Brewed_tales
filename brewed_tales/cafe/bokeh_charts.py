
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

def generate_most_popular_books_bar_chart(df):
    p = figure(x_range=df['book_title'], title="Most Popular Books", toolbar_location=None, tools="")
    p.vbar(x=df['book_title'], top=df['sold'], width=0.9)
    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    return p

def generate_top_drinks_by_average_price_chart(df):
    p = figure(x_range=df['item_name'], title="Top Drinks by Average Price", toolbar_location=None, tools="")
    p.vbar(x=df['item_name'], top=df['average_price'], width=0.9)
    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    return p


def generate_customers_with_large_book_orders_chart(df):
    p = figure(x_range=df['customer'], title="Customers with Large Book Orders", toolbar_location=None, tools="")
    p.vbar(x=df['customer'], top=df['total_books'], width=0.9)
    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    return p


def generate_orders_with_books_and_drinks_chart(df):
    p = figure(x_range=df['order_id'], title="Orders with Books and Drinks", toolbar_location=None, tools="")
    p.vbar(x=df['order_id'], top=df['quantity'], width=0.9, legend_label="Books & Drinks", color="green")
    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    return p

def generate_recent_orders_chart(df):
    p = figure(x_range=df['order_date'], title="Recent Orders", toolbar_location=None, tools="")
    p.vbar(x=df['order_date'], top=df['order_count'], width=0.9)
    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    return p
