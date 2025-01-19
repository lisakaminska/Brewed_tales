from bokeh.palettes import Spectral11
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.transform import cumsum
from math import pi

def generate_top_customers_bar_chart(df):
    p = figure(x_range=df['customer'], title="Top Customers by Orders", toolbar_location="above", tools="pan,box_zoom,reset,hover,save")
    p.vbar(x=df['customer'], top=df['orders'], width=0.9, color=Spectral11[2])
    hover = HoverTool()
    hover.tooltips = [("Customer", "@customer"), ("Orders", "@orders")]
    p.add_tools(hover)
    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    p.xaxis.major_label_orientation = 1
    p.yaxis.axis_label = 'Number of Orders'
    p.xaxis.axis_label = 'Customer'
    return p

def generate_most_popular_books_pie_chart(df):
    df['angle'] = df['sold'] / df['sold'].sum() * 2 * pi
    df['color'] = ["#%06x" % (i * 0x654321 % 0xFFFFFF) for i in range(len(df))]
    df['percentage'] = (df['sold'] / df['sold'].sum() * 100).round(2)
    source = ColumnDataSource(df)
    p = figure(title="Most Popular Books (Interactive Pie Chart)", toolbar_location="above", tools="pan, wheel_zoom, box_zoom, reset", height=350, width=600)
    p.wedge(x=0, y=1, radius=0.4, start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'), line_color="white", fill_color='color', legend_field='book_title', source=source)
    hover = HoverTool(tooltips=[("Book Title", "@book_title"), ("Sold", "@sold"), ("Percentage", "@percentage%")])
    p.add_tools(hover)
    p.axis.axis_label = None
    p.axis.visible = False
    p.grid.grid_line_color = None
    p.legend.orientation = "vertical"
    p.legend.location = "center_right"
    p.legend.label_text_font_size = "10px"
    p.legend.border_line_color = None
    return p

def generate_top_drinks_by_average_price_pie_chart(df):
    df['angle'] = df['average_price'] / df['average_price'].sum() * 2 * pi
    df['color'] = ["#%06x" % (i * 0x654321 % 0xFFFFFF) for i in range(len(df))]
    df['percentage'] = (df['average_price'] / df['average_price'].sum() * 100).round(2)
    source = ColumnDataSource(df)
    p = figure(title="Top Drinks by Average Price (Interactive Pie Chart)", toolbar_location="above", tools="pan, wheel_zoom, box_zoom, reset", height=350, width=600)
    p.wedge(x=0, y=1, radius=0.4, start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'), line_color="white", fill_color='color', legend_field='item_name', source=source)
    hover = HoverTool(tooltips=[("Drink Name", "@item_name"), ("Average Price", "@average_price"), ("Percentage", "@percentage%")])
    p.add_tools(hover)
    p.axis.axis_label = None
    p.axis.visible = False
    p.grid.grid_line_color = None
    p.legend.orientation = "vertical"
    p.legend.location = "center_right"
    p.legend.label_text_font_size = "10px"
    p.legend.border_line_color = None
    return p

def generate_customers_with_large_book_orders_scatter_chart(df):
    df['total_books'] = df['total_books'].astype(float)
    df['customer'] = df['first_name'] + ' ' + df['last_name']
    source = ColumnDataSource(df)
    p = figure(title="Customers with Large Book Orders (Interactive Scatter Chart)", x_axis_label="Customer", y_axis_label="Total Books Ordered", tools="pan,wheel_zoom,box_zoom,reset", toolbar_location="above", height=400, width=700)
    p.scatter(x='index', y='total_books', size=10, color="navy", alpha=0.7, source=source)
    hover = HoverTool(tooltips=[("Customer", "@customer"), ("Total Books Ordered", "@total_books")])
    p.add_tools(hover)
    p.xaxis.visible = False
    p.y_range.start = 0
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_dash = [6, 4]
    return p


def generate_recent_orders_line_chart(df):
    df['order_count'] = df['order_count'].astype(float)
    df['order_date_str'] = df['order_date'].dt.strftime('%Y-%m-%d %H:%M:%S')
    source = ColumnDataSource(df)
    p = figure(title="Recent Orders (Interactive Line Chart)", x_axis_type="datetime", x_axis_label="Order Date", y_axis_label="Order Count", tools="pan,wheel_zoom,box_zoom,reset", toolbar_location="above", height=400, width=700)
    p.line(x='order_date', y='order_count', line_width=2, color="blue", source=source, legend_label="Order Trend")
    p.circle(x='order_date', y='order_count', size=8, color="red", source=source)
    hover = HoverTool(tooltips=[("Order Date", "@order_date_str"), ("Order Count", "@order_count")], mode="vline")
    p.add_tools(hover)
    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    p.legend.location = "top_left"
    p.legend.label_text_font_size = "10px"
    p.xaxis.major_label_orientation = 0.8
    return p
