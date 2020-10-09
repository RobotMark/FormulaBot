import random
import math
import copy
#import matplotlib.pyplot as plt
from enum import Enum
from sklearn.metrics import mean_absolute_error, mean_squared_error
from tqdm import tqdm
#from jupyterplot import ProgressPlot



class Solution:
    
    
    class Operator(Enum):
        ADD      = 1
        MINUS    = 2
        MULTIPLY = 3
        DIVIDE   = 4
        ABS_SQRT = 5
        NEG      = 6
        SIN      = 7
        COS      = 8
        TAN      = 9
        IF_GT    = 10
        IF_LT    = 11
        IF_EQ    = 12


    def __init__(self, parameters, operations_size, operands_size):
        """
        parameters:  a list of the function inputs
        operations_size:  how many operations to include in the solution
        operands_size:  how many operands to include for each operator
        """
        self.params_size = len(parameters)
        self.ops_size = len(parameters) + operations_size
        self.ops = [(p,[]) for p in parameters]
        self.operands_size = operands_size
        
        idx = self.params_size
        for _ in range(operations_size):
            operator = random.randint(1, len(self.Operator))
            operands = []
            
            for _ in range(operands_size):
                operands.extend([random.randint(0, idx - 1)])
            
            self.ops.append((operator, operands))
        
            idx = idx + 1


    def compute(self, values):
        # reset calc tape
        calc_tape = [None] * self.ops_size

        for i, _ in enumerate(self.ops):

            # handle terminals
            if len(self.ops[i][1]) == 0:
                calc_tape[i] = values[self.ops[i][0]]

            # handle operations
            else:
                #print(self.ops[i][1][0],  '>> ', self.ops[i][1][1])
                if self.Operator(self.ops[i][0]).name == 'ADD':
                    calc_tape[i] = calc_tape[self.ops[i][1][0]] + calc_tape[self.ops[i][1][1]]
                elif self.Operator(self.ops[i][0]).name == 'MINUS':
                    calc_tape[i] = calc_tape[self.ops[i][1][0]] - calc_tape[self.ops[i][1][1]]
                elif self.Operator(self.ops[i][0]).name == 'MULTIPLY':
                    calc_tape[i] = calc_tape[self.ops[i][1][0]] * calc_tape[self.ops[i][1][1]]
                elif self.Operator(self.ops[i][0]).name == 'DIVIDE':
                    try:
                        calc_tape[i] = calc_tape[self.ops[i][1][0]] / calc_tape[self.ops[i][1][1]]
                    except ZeroDivisionError:
                        calc_tape[i] = 0.
                elif self.Operator(self.ops[i][0]).name == 'ABS_SQRT':
                    calc_tape[i] = math.sqrt(abs(calc_tape[self.ops[i][1][0]]))        
                elif self.Operator(self.ops[i][0]).name == 'NEG':
                    calc_tape[i] = -1. * calc_tape[self.ops[i][1][0]]   
                elif self.Operator(self.ops[i][0]).name == 'SIN':
                    calc_tape[i] = math.sin(calc_tape[self.ops[i][1][0]])        
                elif self.Operator(self.ops[i][0]).name == 'COS':
                    calc_tape[i] = math.cos(calc_tape[self.ops[i][1][0]])        
                elif self.Operator(self.ops[i][0]).name == 'TAN':
                    calc_tape[i] = math.tan(calc_tape[self.ops[i][1][0]])
                elif self.Operator(self.ops[i][0]).name == 'IF_GT':
                    if calc_tape[self.ops[i][1][0]] > calc_tape[self.ops[i][1][1]]:
                        calc_tape[i] = calc_tape[self.ops[i][1][2]]
                    else:
                        calc_tape[i] = calc_tape[self.ops[i][1][3]]
                elif self.Operator(self.ops[i][0]).name == 'IF_LT':
                    if calc_tape[self.ops[i][1][0]] < calc_tape[self.ops[i][1][1]]:
                        calc_tape[i] = calc_tape[self.ops[i][1][2]]
                    else:
                        calc_tape[i] = calc_tape[self.ops[i][1][3]]
                elif self.Operator(self.ops[i][0]).name == 'IF_EQ':
                    if calc_tape[self.ops[i][1][0]] == calc_tape[self.ops[i][1][1]]:
                        calc_tape[i] = calc_tape[self.ops[i][1][2]]
                    else:
                        calc_tape[i] = calc_tape[self.ops[i][1][3]]

        return(calc_tape[i])


    def print_pretty(self):
        print('--------------------------------------------------------------------')
        for idx, x in enumerate(self.ops[:self.params_size]):
            print(f'{idx:4d}. {x[0]:10}')
        print('--------------------------------------------------------------------')
        for idx, x in enumerate(self.ops[self.params_size:], start=self.params_size):
            print(f'{idx:4d}. {self.Operator(x[0]).name:10} {x[1]}') 
        print('--------------------------------------------------------------------')
        print("LaTex: ", self.to_latex_string())
        print('--------------------------------------------------------------------')

    def to_latex_string(self):
        formulas = [None]*self.ops_size

        for i, op in enumerate(self.ops):
            if len(op[1]) > 1:
                if self.Operator(op[0]).name == "ADD":
                    formulas[i] = r"(" + str(formulas[op[1][0]]) + "+" + str(formulas[op[1][1]]) + ")"
                elif self.Operator(op[0]).name == "MINUS":
                    formulas[i] = r"(" + str(formulas[op[1][0]]) + "-" + str(formulas[op[1][1]]) + ")"
                elif self.Operator(op[0]).name == "MULTIPLY":
                    formulas[i] = r"(" + str(formulas[op[1][0]]) + r"\cdot " + str(formulas[op[1][1]]) + ")"
                elif self.Operator(op[0]).name == "DIVIDE":
                    formulas[i] = r"\frac{" + str(formulas[op[1][0]]) + "}{" + str(formulas[op[1][1]]) + "}"
                elif self.Operator(op[0]).name == "ABS_SQRT":
                    formulas[i] = r"\sqrt{\lvert " + str(formulas[op[1][0]]) + r"\lvert }"
                elif self.Operator(op[0]).name == "NEG":
                    formulas[i] = r"-(" + str(formulas[op[1][0]]) + ")"  
                elif self.Operator(op[0]).name == "SIN":
                    formulas[i] = r"\sin (" + str(formulas[op[1][0]]) + ")"
                elif self.Operator(op[0]).name == "COS":
                    formulas[i] = r"\cos (" + str(formulas[op[1][0]]) + ")"     
                elif self.Operator(op[0]).name == "TAN":
                    formulas[i] = r"\tan (" + str(formulas[op[1][0]]) + ")"
                elif self.Operator(op[0]).name == "IF_GT":
                    formulas[i] = r"\big [ \big (" + str(formulas[op[1][0]]) + ">" + str(formulas[op[1][1]]) + r"\big )" + r"\rightarrow " + r"\big (" + str(formulas[op[1][2]]) + r"\big ) ? \big (" + str(formulas[op[1][3]]) + r"\big ) \big ]"
                elif self.Operator(op[0]).name == "IF_LT":
                    formulas[i] = r"\big [ \big (" + str(formulas[op[1][0]]) + "<" + str(formulas[op[1][1]]) + r"\big )" + r"\rightarrow " + r"\big (" + str(formulas[op[1][2]]) + r"\big ) ? \big (" + str(formulas[op[1][3]]) + r"\big ) \big ]"
                elif self.Operator(op[0]).name == "IF_EQ":
                    formulas[i] = r"\big [ \big (" + str(formulas[op[1][0]]) + "==" + str(formulas[op[1][1]]) + r"\big )" + r"\rightarrow " + r"\big (" + str(formulas[op[1][2]]) + r"\big ) ? \big (" + str(formulas[op[1][3]]) + r"\big ) \big ]"

            else:
                formulas[i] = str(op[0])

        return formulas[-1]


    def mutate(self):
        
        row = random.randint(self.params_size, self.ops_size-1)    
        new_operands = copy.deepcopy(self.ops[row][1])
        new_operator = self.ops[row][0]

        # randomly decide if operands should be modified
        if bool(random.getrandbits(1)):            
            new_operands[random.randint(0,self.operands_size-1)] = random.randint(0,row-1)

        # randomly decide if operands should be split and recombined
        if bool(random.getrandbits(1)):
            ptr = random.randint(0,self.operands_size-1)
            new_operands = new_operands[ptr:] + new_operands[:ptr]

        # randomly decide if changing operator should be modified
        if bool(random.getrandbits(1)):
            new_operator = random.randint(1, len(self.Operator))
            
        self.ops[row] = (new_operator, new_operands)


class Population:
    
    def __init__(self, population_size, parameters, operations_size, operands_size, 
                 epochs, crossover_rate, mutation_rate, kill_rate, error_calc, inputs, outputs):
        """ The Population is the collection of Solution objects.  Operations against the Solutions
            are performed through the Population class

        The Population is structured as an iterable collection of Solutions.  Common GP operations
        on the Solutions are executed by the Population class.  Metrics on the population can be
        retrieved from this class as well.

        Args:
            population_size (int):      The number of solutions to initialize.
            parameters (list<str>):     A list of the function inputs
            operations_size (int):      How many operations to include in the solution
            operands_size (int):        How many operands to include for each operator
            epochs (int):               How many generations to use when training
            crossover_rate (float):     A percentage of the solutions to use for creating child 
                                        solutions in each epoch
            mutation_rate (float):      A percentage of the solutions to mutate in each epoch
            kill_rate (float):          A percentage of the solutions to kill in each epoch. A new 
                                        solution will replace the dead Solution
            error_calc (func):          The method of error calculation to perform
            inputs (list<dict>):        A list of dictionaries representing the model inputs for training
                                        and testing
            outputs (list):             A list of results to test the model against
        """
        self.pop_size = population_size
        self.parameters = parameters
        self.ops_size = operations_size
        self.operands_size = operands_size
        self.epochs = epochs
        self.crossovers = int(population_size * crossover_rate)
        self.mutations = int(population_size * mutation_rate)
        self.kills = int(population_size * kill_rate)

        if error_calc == 'mae':
            self.fitness_calc = mean_absolute_error
        elif error_calc == 'mse':
            self.fitness_calc = mean_squared_error
        else:
            self.fitness_calc = mean_absolute_error
        
        self.inputs = inputs
        self.outputs = outputs
        self.i = -1
        self.solutions = []
        
        with tqdm(total=self.pop_size, desc="Initialize Solutions") as pbar:
            for _ in range(self.pop_size):
                self.solutions.append(Solution(self.parameters, self.ops_size, self.operands_size))    
                pbar.update(1)

        self.scores = [None] * self.pop_size

        self.update_scores()


    def add_solution(self, s):
        self.solutions.append(s)


    def get_best_score(self):
        return min(self.scores)


    def get_best_score_index(self):
        return self.scores.index(self.get_best_score())


    def get_avg_score(self):
        return sum(self.scores) / self.pop_size


    def get_best_solution(self):
        return self.solutions[self.scores.index(self.get_best_score())]


    def update_score(self, idx):
        pred = [m for m in map(self.solutions[idx].compute, self.inputs)]
        self.scores[idx] = self.fitness_calc(self.outputs, pred)
        return self.scores[idx]


    def update_scores(self):
        with tqdm(total=self.pop_size, desc="Initialize Scores   ") as pbar:    
            for x in range(self.pop_size):
                self.update_score(x)
                pbar.update(1)


    def run_epochs(self, plot_nb=False):
        #if plot_nb:
        #    #pp = ProgressPlot(x_lim=[0, self.epochs], line_names=["Population Avg.", "Best Solution"])
        #    #pp = ProgressPlot(x_lim=[0, self.epochs], line_names=["Best Solution"])
        
        with tqdm(total=self.epochs, desc="Epochs") as pbar:
            for _ in range(self.epochs):
                self.crossover_many()
                self.mutate_many()
                self.kill_many()

                pbar.update(1)

                #if plot_nb:
                #    #pp.update([[self.get_avg_score(), self.get_best_score()]])
                #    #pp.update([[self.get_best_score()]])
        
                if len(set(self.scores)) == 1:
                    print("Convergence!")
                    break

                #if round(self.get_best_score(), 6) == 0.0:
                if self.get_best_score() == 0.0:
                    print("Optimal Solution Found!")
                    break

        #if plot_nb:
        #    pp.finalize()


    def get_rand_solution(self):
        return self.solutions[random.randint(0,self.pop_size-1)]


    def create_child(self):
        parents = random.sample(self.solutions, k=2)
        child = copy.deepcopy(parents[0])
        splice = random.randint(0,self.ops_size)
        child.ops[:splice] = parents[1].ops[:splice]
        return (child, self.fitness_calc(self.outputs, [m for m in map(child.compute, self.inputs)]))


    def crossover_one(self):
        c, s = self.create_child()
        
        if s < max(self.scores):
            idx_max = self.scores.index(max(self.scores))
            self.solutions[idx_max] = c
            self.scores[idx_max] = s
    

    def crossover_many(self):
        for _ in range(self.crossovers):
            if len(set(self.scores)) > 1:
                self.crossover_one()
            else:
                break


    def kill_one(self):
        s = self.get_rand_solution()
        idx = self.solutions.index(s)

        if self.scores.index(self.get_best_score()) != idx:
        #if self.get_best_score_index != idx:
            self.solutions[idx] = Solution(self.parameters, self.ops_size, self.operands_size)
            self.update_score(idx)


    def kill_many(self):
        for _ in range(self.kills):
            self.kill_one()


    def mutate_one(self):
        s = self.get_rand_solution()
        idx = self.solutions.index(s)
        
        if self.scores.index(self.get_best_score()) != idx:
        #if self.get_best_score_index != idx:
            s.mutate()
            self.update_score(idx)


    def mutate_many(self):
        for _ in range(self.mutations):
            self.mutate_one()


    # def plot_predictions(self, size=100):
    #     result_cnt = size
    #     fig, ax = plt.subplots()

    #     x = [x for x in range(result_cnt)]
    #     y = [m for m in map(self.get_best_solution().compute, self.inputs[:result_cnt])]
    #     ax.scatter(x, y, label='model', alpha=0.3, edgecolor='black', s=300, c='blue')

    #     x = [x for x in range(result_cnt)]
    #     y = self.outputs[:result_cnt]
    #     ax.scatter(x, y, label='actual', alpha=0.8, edgecolor='black', s=50, c='red')

    #     ax.legend()
    #     ax.grid(True)

    #     return plt


    def __iter__(self):
        return self


    def __next__(self):
        if self.i < self.pop_size - 1:
            self.i += 1
            return self.solutions[self.i]
        
        self.i = -1
        raise StopIteration()
     