import os
from plotly.graph_objs import Bar, Pie, Scatter, Line
from plotly.offline import plot

def generate_top_customers_bar_chart(df, output_file='top_customers_bar_chart.html'):
    if df.empty:
        print("No data available")
        return

    output_path = os.path.join('static', 'charts', output_file)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    df['full_name'] = df['first_name'] + ' ' + df['last_name']
    bar_chart = Bar(x=df['full_name'], y=df['total_orders'], name='Orders')
    layout = dict(title='Top Customers by Orders', xaxis=dict(title='Customers'), yaxis=dict(title='Total Orders'))

    plot(dict(data=[bar_chart], layout=layout), filename=output_path, auto_open=False)


def generate_most_popular_books_pie_chart(df, output_file='most_popular_books_pie_chart.html'):
    if df.empty:
        print("No data available")
        return

    output_path = os.path.join('static', 'charts', output_file)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    pie_chart = Pie(labels=df['title'], values=df['total_sold'])
    layout = dict(title='Most Popular Books by Total Sold')

    plot(dict(data=[pie_chart], layout=layout), filename=output_path, auto_open=False)


def generate_top_drinks_bar_chart(df, output_file='top_drinks_bar_chart.html'):
    if df.empty:
        print("No data available")
        return

    output_path = os.path.join('static', 'charts', output_file)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    bar_chart = Bar(x=df['item_name'], y=df['average_price'], name='Average Price')
    layout = dict(title='Top Drinks by Average Price', xaxis=dict(title='Drinks'), yaxis=dict(title='Average Price'))

    plot(dict(data=[bar_chart], layout=layout), filename=output_path, auto_open=False)


def generate_customers_scatter_chart(df, output_file='customers_scatter_chart.html'):
    if df.empty:
        print("No data available")
        return

    output_path = os.path.join('static', 'charts', output_file)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    scatter_chart = Scatter(x=df['full_name'], y=df['total_books'], mode='markers', name='Books Ordered')
    layout = dict(title='Customers with Large Book Orders', xaxis=dict(title='Customers'), yaxis=dict(title='Total Books'))

    plot(dict(data=[scatter_chart], layout=layout), filename=output_path, auto_open=False)


def generate_recent_orders_line_chart(df, output_file='recent_orders_line_chart.html'):
    if df.empty:
        print("No data available")
        return

    output_path = os.path.join('static', 'charts', output_file)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    line_chart = Line(x=df['order_date'], y=df['total'], name='Recent Orders')
    layout = dict(title='Recent Orders', xaxis=dict(title='Date'), yaxis=dict(title='Total Amount'))

    plot(dict(data=[line_chart], layout=layout), filename=output_path, auto_open=False)


from plotly.graph_objs import Heatmap, Bar

def generate_orders_with_books_and_drinks_chart(df, output_file='orders_with_books_and_drinks_chart.html'):
    if df.empty:
        print("No data available")
        return

    # Формуємо повний шлях до файлу
    output_path = os.path.join('static', 'charts', output_file)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Перевірка наявності необхідних колонок
    if {'book__title', 'cafe_item__item_name', 'quantity'}.issubset(df.columns):
        # Групована стовпчикова діаграма
        grouped_bar_chart = [
            Bar(name='Books', x=df['book__title'], y=df['quantity'], marker=dict(color='blue')),
            Bar(name='Drinks', x=df['cafe_item__item_name'], y=df['quantity'], marker=dict(color='orange'))
        ]

        layout = dict(
            title='Orders with Books and Drinks',
            xaxis=dict(title='Items'),
            yaxis=dict(title='Quantity'),
            barmode='group'
        )

        # Генерація графіка
        plot(dict(data=grouped_bar_chart, layout=layout), filename=output_path, auto_open=False)
    else:
        print("Required columns not found in the DataFrame.")
