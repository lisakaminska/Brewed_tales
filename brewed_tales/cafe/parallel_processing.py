from concurrent.futures import ThreadPoolExecutor
import multiprocessing
from time import time
import matplotlib.pyplot as plt

from io import BytesIO
import base64
from cafe.repositories import BrewerContext


# Функція для виконання репозиторної функції
def execute_repo_function(repo_function, *args):
    """
    Виконує функцію репозиторію та повертає час виконання.
    """
    start_time = time()
    result = repo_function(*args)
    execution_time = time() - start_time
    return execution_time

# Паралельне виконання репозиторних функцій (багатопотоково)
def run_parallel_with_threads(repo_functions, num_threads):
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        results = list(executor.map(lambda func: execute_repo_function(func[0], *func[1]), repo_functions))
    return sum(results)

# Паралельне виконання репозиторних функцій (багатопроцесно)
def run_parallel_with_processes(repo_functions, num_processes):
    with multiprocessing.Pool(processes=num_processes) as pool:
        results = pool.map(lambda func: execute_repo_function(func[0], *func[1]), repo_functions)
    return sum(results)

# Побудова графіка результатів
def plot_results(results):
    threads = list(results.keys())
    times = list(results.values())

    plt.figure(figsize=(10, 6))
    plt.plot(threads, times, marker='o', color='b', label='Час виконання')
    plt.title('Час виконання функцій в залежності від кількості потоків/процесів')
    plt.xlabel('Кількість потоків/процесів')
    plt.ylabel('Час виконання (сек)')
    plt.grid(True)
    plt.legend()

    # Збереження графіка у форматі base64
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    graphic = base64.b64encode(image_png).decode('utf-8')
    return graphic

# Проведення експерименту
def perform_experiment():
    """
    Виконує експерименти з різною кількістю потоків/процесів і повертає графік результатів.
    """
    # Створюємо контекст
    context = BrewerContext()

    # Визначаємо функції для виконання
    repo_functions = [
        (context.order_repo.get_total_orders, []),
        (context.cafe_item_repo.get_average_price, []),
        (context.customer_repo.get_customers_by_last_name_starting_with, ['A']),
    ] * 10  # Повторюємо для навантаження

    results = {}

    # Експерименти з різною кількістю потоків
    for num_threads in range(1, 9):  # Від 1 до 8 потоків
        results[num_threads] = run_parallel_with_threads(repo_functions, num_threads)

    return plot_results(results)
