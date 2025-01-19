from bokeh.plotting import figure
from bokeh.models import HoverTool
from bokeh.palettes import Spectral11

def generate_top_customers_bar_chart(df):
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
    df['total_books'] = df['total_books'].astype(float)
    df['customer'] = df['first_name'] + ' ' + df['last_name']  # Додаємо колону 'customer'
    p = figure(x_range=df['customer'], title="Customers with Large Book Orders", toolbar_location=None, tools="")
    p.vbar(x=df['customer'], top=df['total_books'], width=0.9)
    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    return p


def generate_orders_with_books_and_drinks_chart(df):
    df['quantity'] = df['quantity'].astype(float)  # Перетворення кількості на float
    p = figure(x_range=df['order_id'].astype(str), title="Orders with Books and Drinks", toolbar_location=None, tools="")
    p.vbar(x=df['order_id'].astype(str), top=df['quantity'], width=0.9, legend_label="Books & Drinks", color="green")
    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    return p


def generate_recent_orders_chart(df):
    df['order_count'] = df['order_count'].astype(float)
    order_dates = df['order_date'].dt.strftime('%Y-%m-%d %H:%M:%S').tolist()
    p = figure(x_range=order_dates, title="Recent Orders", toolbar_location=None, tools="")
    p.vbar(x=order_dates, top=df['order_count'], width=0.9)
    p.xgrid.grid_line_color = None
    p.y_range.start = 0

    p.xaxis.major_label_orientation = 1
    return p