from bokeh.models import HoverTool
from bokeh.palettes import Spectral11
from bokeh.io import show
from bokeh.layouts import column
from bokeh.plotting import figure
from bokeh.palettes import Category20c
from bokeh.transform import cumsum
import numpy as np

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



from bokeh.palettes import Category20


def generate_most_popular_books_pie_chart(df):
    # Перетворення даних для кругової діаграми
    df['angle'] = df['orders'] / df['orders'].sum() * 2 * np.pi  # Розрахунок кутів для pie chart
    num_colors = len(df)
    color_palette = Category20[num_colors] if num_colors <= 20 else Category20[
        20]  # Використовуємо палітру для кількості елементів

    df['color'] = color_palette[:num_colors]  # Вибір кольорів відповідно до кількості

    # Створення фігури
    p = figure(title="Most Popular Books", toolbar_location="above", tools="hover,save,pan,box_zoom,reset")

    # Додавання секцій кругової діаграми
    p.wedge(x=0, y=1, radius=0.4,
            start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
            line_color="white", fill_color='color', legend_field='book_title', source=df)

    # Додавання HoverTool для відображення підказок
    hover = HoverTool()
    hover.tooltips = [("Book", "@book_title"), ("Orders", "@orders")]
    p.add_tools(hover)

    # Налаштування зовнішнього вигляду
    p.axis.visible = False  # Приховати ось
    p.grid.visible = False  # Приховати сітку
    p.y_range.start = 0  # Початок осі Y
    p.x_range.start = -1  # Початок осі X

    return p
