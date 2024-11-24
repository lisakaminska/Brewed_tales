import pandas as pd
from plotly.graph_objs import Bar, Pie, Scatter, Line, Histogram, Box
from plotly.offline import plot


# Стовпчастий графік
from django.conf import settings
import os

import pandas as pd
from plotly.graph_objs import Bar
from plotly.offline import plot
import os

def generate_top_customers_bar_chart(df, output_file='top_customers_bar_chart.html'):
    if df.empty:
        print("No data available")
        return

    # Формуємо повний шлях до файлу
    output_path = os.path.join('static', 'charts', output_file)
    # Переконуємося, що каталог існує
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    df['full_name'] = df['first_name'] + ' ' + df['last_name']
    bar_chart = Bar(x=df['full_name'], y=df['total_orders'], name='Orders')
    layout = dict(title='Top Customers by Orders', xaxis=dict(title='Customers'), yaxis=dict(title='Total Orders'))

    # Генеруємо графік та зберігаємо файл у вказаному шляху
    plot(dict(data=[bar_chart], layout=layout), filename=output_path, auto_open=False)
