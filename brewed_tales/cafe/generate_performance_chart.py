import pandas as pd
import os
from plotly.graph_objs import Scatter
from plotly.offline import plot

def generate_performance_chart(results_csv='performance_results.csv', output_file='performance_chart.html'):
    # Завантаження результатів
    df = pd.read_csv(results_csv)

    # Створення графіка
    scatter_chart = Scatter(x=df['num_processes'], y=df['execution_time'], mode='lines+markers', name='Execution Time')
    layout = dict(title='Execution Time vs. Number of Processes',
                  xaxis=dict(title='Number of Processes'),
                  yaxis=dict(title='Execution Time (seconds)'))

    # Генерація HTML
    output_path = os.path.join('static', 'charts', output_file)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plot(dict(data=[scatter_chart], layout=layout), filename=output_path, auto_open=False)

    print(f"Графік збережено у {output_path}")


if __name__ == '__main__':
    generate_performance_chart()
