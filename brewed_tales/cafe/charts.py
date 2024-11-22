

import pandas as pd
from plotly.graph_objs import Bar, Pie, Scatter
from plotly.offline import plot
def generate_top_customers_chart(data, output_file='top_customers_bar_chart.html'):
    df = pd.DataFrame(data)
    df['full_name'] = df['first_name'] + ' ' + df['last_name']

    bar_chart = Bar(x=df['full_name'], y=df['total_orders'], name='Orders')
    layout = dict(title='Top Customers by Orders', xaxis=dict(title='Customers'), yaxis=dict(title='Total Orders'))
    plot(dict(data=[bar_chart], layout=layout), filename=output_file)


def generate_most_popular_books_pie_chart(data, output_file='most_popular_books_pie_chart.html'):
    df = pd.DataFrame(data, columns=['title', 'total_sold'])

    pie_chart = Pie(labels=df['title'], values=df['total_sold'], name='Book Sales')
    layout = dict(title='Most Popular Books')
    plot(dict(data=[pie_chart], layout=layout), filename=output_file)
#

def generate_books_and_drinks_chart(data, output_file='books_and_drinks_bar_chart.html'):
    # Преобразування data в DataFrame
    df = pd.DataFrame(data, columns=['book__title', 'cafe_item__item_name', 'quantity'])

    # Групуємо дані по книгах і підсумовуємо кількість
    grouped = df.groupby('book__title').agg({'quantity': 'sum'}).reset_index()

    bar_chart = Bar(x=grouped['book__title'], y=grouped['quantity'], name='Books and Drinks')
    layout = dict(title='Books with Drinks', xaxis=dict(title='Books'), yaxis=dict(title='Total Quantity'))
    plot(dict(data=[bar_chart], layout=layout), filename=output_file)


def generate_recent_orders_chart(data, output_file='recent_orders_line_chart.html'):
    # Преобразування data в DataFrame
    df = pd.DataFrame(data, columns=['order_date', 'id'])

    # Перетворюємо стовпець з датою на datetime формат
    df['order_date'] = pd.to_datetime(df['order_date'])

    # Групуємо за датою і рахуємо кількість замовлень
    df = df.groupby('order_date').size().reset_index(name='order_count')

    line_chart = Scatter(x=df['order_date'], y=df['order_count'], mode='lines+markers', name='Orders')
    layout = dict(title='Recent Orders', xaxis=dict(title='Date'), yaxis=dict(title='Order Count'))
    plot(dict(data=[line_chart], layout=layout), filename=output_file)


def generate_top_drinks_by_price_chart(data, output_file='top_drinks_by_price_bar_chart.html'):
    # Преобразування data в DataFrame
    df = pd.DataFrame(data, columns=['item_name', 'average_price'])

    bar_chart = Bar(x=df['item_name'], y=df['average_price'], name='Drinks')
    layout = dict(title='Top Drinks by Average Price', xaxis=dict(title='Drink'), yaxis=dict(title='Average Price'))
    plot(dict(data=[bar_chart], layout=layout), filename=output_file)


def generate_large_book_orders_chart(data, output_file='large_book_orders_chart.html'):
    # Преобразування data в DataFrame
    df = pd.DataFrame(data, columns=['first_name', 'last_name', 'total_books'])

    # Додати колонку для повного імені
    df['full_name'] = df['first_name'] + ' ' + df['last_name']

    bar_chart = Bar(x=df['full_name'], y=df['total_books'], name='Books')
    layout = dict(title='Large Book Orders', xaxis=dict(title='Customers'), yaxis=dict(title='Total Books'))
    plot(dict(data=[bar_chart], layout=layout), filename=output_file)
