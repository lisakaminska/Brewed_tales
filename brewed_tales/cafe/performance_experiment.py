import argparse
import multiprocessing
import time
import pandas as pd
import random

def simulate_database_query(query_id):
    time.sleep(random.uniform(0.1, 0.5))  # Імітація часу запиту

def measure_execution_time(num_processes, num_queries):
    queries = list(range(num_queries))
    start_time = time.time()

    with multiprocessing.Pool(num_processes) as pool:
        pool.map(simulate_database_query, queries)

    execution_time = time.time() - start_time
    return execution_time

def run_experiments(num_of_queries):
    results = []

    for num_processes in range(1, 11):  # Від 1 до 10 процесів
        execution_time = measure_execution_time(num_processes, num_of_queries)
        results.append({'num_processes': num_processes, 'execution_time': execution_time})

    return pd.DataFrame(results)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run performance experiments.')
    parser.add_argument('--queries', type=int, required=True, help='Number of queries to simulate.')

    args = parser.parse_args()

    results_df = run_experiments(args.queries)
    print(results_df)