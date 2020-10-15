import math
import numpy as np
import pandas as pd
import statistics
import time
import concurrent
import copy
import random
from concurrent.futures import ProcessPoolExecutor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split
from formulabot.mep import Solution, Population
from tqdm import tqdm


def main():

    source_data_path = r"C:\Users\markr\Projects\Software\FormulaBot\data\hypotenuse_01.csv"
    results_path = r"C:\Users\markr\Projects\Software\FormulaBot\data\hypotenuse_01_results.csv"
    scenarios_to_run = 2

    df = pd.read_csv(source_data_path)
    X = df[['X','Y']].to_dict(orient='records')
    Y = df['out'].tolist()
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.33)

    rng = np.arange(scenarios_to_run)

    d = {}
    results = []
    d['parms'] = list(df.columns[:-1])
    d['X_train'] = X_train 
    d['y_train'] = y_train
    d['X_test']  = X_test
    d['y_test']  = y_test

    with ProcessPoolExecutor() as executor:
        for _ in rng:
            d['population_size'] = random.randint(100,501)
            d['operations_size'] = random.randint(10,101)
            d['operands_size'] = random.randint(30,51)
            d['epochs'] = random.randint(400,1001)
            d['crossover_rate'] = random.randint(20, 81)/100.
            d['mutation_rate'] = random.randint(1, 31)/100.
            d['kill_rate'] = random.randint(1, 31)/100.

            results.append(executor.submit(run_scenario, copy.deepcopy(d)))

        for r in concurrent.futures.as_completed(results):   
            write_to_log(r, results_path) 
            print(f"pop:{r.result()['population_size']} | ops:{r.result()['operations_size']} | opr:{r.result()['operands_size']}")
            print(f"epochs: {r.result()['epochs']}, train: {r.result()['train_score']} | test: {r.result()['test_score']}")
            
            
def write_to_log(r, fp):
    with open(fp, 'a') as f:
        f.write(str(r.result()['population_size']))
        f.write(',')
        f.write(str(r.result()['operations_size']))
        f.write(',')
        f.write(str(r.result()['operands_size']))
        f.write(',')
        f.write(str(r.result()['epochs']))
        f.write(',')
        f.write(str(r.result()['crossover_rate']))
        f.write(',')
        f.write(str(r.result()['mutation_rate']))
        f.write(',')
        f.write(str(r.result()['kill_rate']))
        f.write(',')
        f.write(str(r.result()['train_score']))
        f.write(',')
        f.write(str(r.result()['test_score']))
        f.write(',')
        f.write(str(len(r.result()['X_train'])))
        f.write(',')
        f.write(str(len(r.result()['X_test'])))
        f.write(',')
        f.write(r.result()['latex_string'])
        f.write(',')
        f.write(str(r.result()['calc_time']))
        f.write(',')
        f.write(str(id(r.result)))
        f.write('\n')
            

def run_scenario(d):

    start = time.perf_counter()

    p = Population(population_size=d['population_size'], 
    parameters=list(d['parms']), 
    operations_size=d['operations_size'], 
    operands_size=d['operands_size'], 
    epochs=d['epochs'], 
    crossover_rate=d['crossover_rate'], 
    mutation_rate=d['mutation_rate'], 
    kill_rate=d['kill_rate'],
    error_calc=mean_squared_error,
    inputs=d['X_train'], 
    outputs=d['y_train'])

    # run epochs
    p.run_epochs(plot_nb=False)

    end = time.perf_counter()

    d['train_score'] = p.get_best_score()
    d['test_score'] = p.fitness_calc(d['y_test'], 
            [m for m in map(p.get_best_solution().compute, d['X_test'])])
    d['latex_string'] = p.get_best_solution().to_latex_string()
    d['calc_time'] = round(end - start, 2)

    return(d)


if __name__ == "__main__":
    main()
