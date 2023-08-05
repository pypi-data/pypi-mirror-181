# -*- coding: utf-8 -*-
"""
Indago utility functions
"""

import indago
import numpy as np
import time
from rich.table import Table
from rich.console import Console


""" shorthand one-line API for running an optimization """
def minimize(evaluation_function, 
             dimensions, 
             lb, 
             ub, 
             optimizer_name, 
             optimize_seed=None,
             **kwargs):

    assert optimizer_name in indago.optimizers_name_list, \
        f'Unknown optimizer name "{optimizer_name}". Use one of the following names: {", ".join(indago.optimizers_name_list)}.'

    # initialize optimizer
    opt = indago.optimizers_dict[optimizer_name]()
    
    # pass parameters
    opt.evaluation_function = evaluation_function
    opt.dimensions = dimensions
    opt.lb = lb
    opt.ub = ub
    for kw, val in kwargs.items():
        setattr(opt, kw, val)
        # print(f'{kw=}: {val=}')
    
    # run
    result = opt.optimize(seed=optimize_seed)
    
    # return
    if opt.objectives == 1 and opt.constraints == 0:
        return result.X, result.f
    else:
        return result.X, result.f, result.O, result.C


""" exhaustive minimizing with exploring optimizer parameters """
def minimize_exhaustive(evaluation_function, 
                        dimensions, 
                        lb, 
                        ub, 
                        optimizer_name, 
                        params_ranges_dict,
                        hyper_optimizer_name='PSO',
                        runs=100,
                        epochs=100,
                        optimize_seed=None,
                        **kwargs):
    """ 
    params_ranges_dict = 
    {'param_name': [lb, ub], ...}
    """

    assert optimizer_name in indago.optimizers_name_list, \
        f'Unknown optimizer name "{optimizer_name}". Use one of the following names: {", ".join(indago.optimizers_name_list)}.'

    assert hyper_optimizer_name in indago.optimizers_name_list, \
        f'Unknown hyper-optimizer name "{hyper_optimizer_name}". Use one of the following names: {", ".join(indago.optimizers_name_list)}.'
    
    # defaults for params_ranges_dict
    if optimizer_name == 'PSO':
        params_ranges_dict_default = {'swarm_size': [5, 100],
                                      'inertia': [0.5, 1],
                                      'cognitive_rate': [0, 2],
                                      'social_rate': [0, 2]}
    elif optimizer_name == 'FWA':
        params_ranges_dict_default = {'n': [5, 100],
                                      'm1': [3, 50],
                                      'm2': [3, 50]}
    elif optimizer_name == 'FWA':
        params_ranges_dict_default = {'acorn_tree_attraction': [0, 1]}
    elif optimizer_name == 'DE':
        params_ranges_dict_default = {'initial_population_size': [20, 1000],
                                      'external_archive_size_factor': [1, 5],
                                      'historical_memory_size': [3, 10],
                                      'p_mutation': [0.05, 0.3]}
    elif optimizer_name == 'BA':
        params_ranges_dict_default = {'bat_swarm_size': [5, 100],
                                      'loudness': [0.1, 1],
                                      'pulse_rate': [0.1, 1],
                                      'alpha': [0.1, 1],
                                      'gamma': [0.1, 1]}
    elif optimizer_name == 'EFO':
        params_ranges_dict_default = {'population_size': [5, 100],
                                      'R_rate': [0.1, 4],
                                      'Ps_rate': [0.1, 4],
                                      'P_field': [0.05, 0.1],
                                      'N_field': [0.4, 0.5]}
    elif optimizer_name == 'MRFO':
        params_ranges_dict_default = {'manta_population': [5, 100]}
        
    # check params_ranges_dict and load defaults if needed
    if params_ranges_dict is None:
        params_ranges_dict = params_ranges_dict_default
    while True:
        for key in params_ranges_dict:
            if key not in params_ranges_dict_default:
                print(f"Warning: param '{key}' in params_ranges_dict not available for tuning, ignoring.")
                break
        else:
            break
        params_ranges_dict.pop(key)
    for key, val in params_ranges_dict.items():
        if val is None:
            params_ranges_dict[key] = params_ranges_dict_default[key]
    
    # monitoring the inner optimization makes no sense
    kwargs_inner = kwargs.copy()
    if 'monitoring' in kwargs_inner:
        kwargs_inner.pop('monitoring')
    
    def hyper_evaluation_function(params_values):
        params = {key: val for (key, val) \
                  in zip(params_ranges_dict.keys(), params_values)}
        fs = np.empty(runs)
        for r in range(runs):
            res = indago.minimize(evaluation_function,
                                  dimensions,
                                  lb,
                                  ub,
                                  optimizer_name,
                                  optimize_seed=optimize_seed,
                                  params=params,
                                  **kwargs_inner)
            fs[r] = res[1]
        return np.median(fs)
    
    # hyper-optimize
    best_param_values, _ = \
        indago.minimize(hyper_evaluation_function,
                        len(params_ranges_dict),
                        [val[0] for val in params_ranges_dict.values()],
                        [val[1] for val in params_ranges_dict.values()],
                        hyper_optimizer_name,
                        optimize_seed=optimize_seed,
                        monitoring=kwargs['monitoring'] if 'monitoring' in kwargs else 'none',
                        iterations=epochs)

    # final optimization
    best_res = None
    best_f = np.inf
    optimal_params = {key: val for (key, val) \
                      in zip(params_ranges_dict.keys(), best_param_values)}
    for r in range(runs):
        res = indago.minimize(evaluation_function,
                              dimensions,
                              lb,
                              ub,
                              optimizer_name,
                              optimize_seed=optimize_seed,
                              params=optimal_params,
                              **kwargs_inner)
        if res[1] < best_f:
            best_res = res
    
    # return
    return best_res, optimal_params


""" benchmarking default-set methods on a goal function """
def inspect(evaluation_function, 
            dimensions, 
            lb, 
            ub, 
            objectives=1,
            constraints=0,
            evaluations=None, 
            optimizers_name_list=None, 
            runs=10,
            xtol=1e-4,
            number_of_processes=1,
            printout=True):

    if not evaluations:
        evaluations = 1000 * dimensions
    if not optimizers_name_list:
        optimizers_name_list = indago.optimizers_name_list
        
    TABLE = {}
    
    f_best_min = np.inf
    opt_f_best_min = None
    f_avg_min = np.inf
    opt_f_avg_min = None
    
    X_best = None
    
    for opt_name in optimizers_name_list:
        
        f_best = np.inf
        O_best = None
        C_best = None
        fs = np.empty(runs)
        times = []
        unique_X_list = []
        
        for r in range(runs):
            
            time_start = time.time()
            
            res = indago.minimize(evaluation_function,
                                  dimensions,
                                  lb,
                                  ub,
                                  opt_name,
                                  objectives=objectives,
                                  constraints=constraints,
                                  iterations=10**10,
                                  maximum_evaluations=evaluations,
                                  number_of_processes=number_of_processes)
            
            O, C = None, None
            if objectives == 1 and constraints == 0:
                X, fs[r] = res
            else:
                X, fs[r], O, C = res
            
            times.append(time.time() - time_start)
            
            if fs[r] < f_best:
                f_best = fs[r]
                if O is not None:
                    O_best = O
                if C is not None:
                    C_best = C
                X_best = np.copy(X)
            
            unique = True
            for unique_X in unique_X_list:
                if ((np.abs(X - unique_X)) / (ub - lb) < xtol).all():
                    unique = False
            if unique:
                unique_X_list.append(np.copy(X))
            
        TABLE[opt_name] = {'time_avg': np.average(times), 
                           'f_avg': np.average(fs), 
                           'f_std': np.std(fs),
                           'f_best': f_best}
        if O is not None:
            TABLE[opt_name]['O_best'] = O_best
        if C is not None:
            TABLE[opt_name]['C_best'] = C_best
        TABLE[opt_name]['unique_X_share'] = len(unique_X_list) / runs
        
        if np.average(fs) < f_avg_min:
            f_avg_min = np.average(fs)
            opt_f_avg_min = opt_name
        
        if f_best < f_best_min:
            f_best_min = f_best
            opt_f_best_min = opt_name
    
    if printout:    
    
        table = Table(title=f'Indago inspect results ({runs} runs of {evaluations} evaluations)')
        
        table.add_column('Algorithm', justify='left', style='magenta')
        table.add_column('Avg run time (s)', justify='left', style='cyan')
        table.add_column('Fitness (avg +/- std)', justify='left', style='cyan')
        table.add_column('Best fitness', justify='left', style='cyan')       
        if not (objectives == 1 and constraints == 0):
            table.add_column('Best objectives', justify='left', style='cyan')
            table.add_column('Best constraints', justify='left', style='cyan')
        table.add_column('Unique X share (%)', justify='left', style='cyan')    
        
        for opt_name, data in TABLE.items():
            if objectives == 1 and constraints == 0:
                table.add_row(opt_name, f"{data['time_avg']:.2}", 
                              f"{data['f_avg']:e} +/- {data['f_std']:e}",
                              f"{data['f_best']:e}", 
                              f"{data['unique_X_share']:.0%}",
                              style='bold' if opt_name in (opt_f_avg_min, opt_f_best_min) else None)
            else:
                table.add_row(opt_name, f"{data['time_avg']:.2}", 
                              f"{data['f_avg']:e} +/- {data['f_std']:e}",
                              f"{data['f_best']:e}", 
                              f"{data['O_best']}", f"{data['C_best']}",
                              f"{data['unique_X_share']:.0%}",
                              style='bold' if opt_name in (opt_f_avg_min, opt_f_best_min) else None)
        
        Console().print(table)
        Console().print(f'[bold][magenta]Best X: [cyan]{X_best}')
    
    return TABLE, X_best
    

""" benchmarking fully prepared optimizers """
def inspect_optimizers(prepared_optimizers_dict, 
                       runs=10, 
                       xtol=1e-4,
                       printout=True):
    """ 
    prepared_optimizers_dict = 
    {'opt1 description': opt1, 'opt2 description': opt2, ...}
    """
     
    TABLE = {}
    
    f_best_min = np.inf
    opt_f_best_min = None
    f_avg_min = np.inf
    opt_f_avg_min = None
    
    X_best = None
    
    for opt_desc, opt in prepared_optimizers_dict.items():
        
        f_best = np.inf
        O_best = None
        C_best = None
        fs = np.empty(runs)
        times = []
        unique_X_list = []
        
        for r in range(runs):
            
            time_start = time.time()
            
            res = opt.optimize()
            fs[r] = res.f
            
            times.append(time.time() - time_start)
            
            if fs[r] < f_best:
                f_best = fs[r]
                if opt.objectives > 1:
                    O_best = res.O
                if opt.constraints != 0:
                    C_best = res.C
                X_best = np.copy(res.X)
                
            unique = True
            for unique_X in unique_X_list:
                if ((np.abs(res.X - unique_X)) / (opt.ub - opt.lb) < xtol).all():
                    unique = False
            if unique:
                unique_X_list.append(np.copy(res.X))
        
        TABLE[opt_desc] = {'time_avg': np.average(times), 
                           'f_avg': np.average(fs), 
                           'f_std': np.std(fs),
                           'f_best': f_best, 
                           'O_best': O_best,
                           'C_best': C_best,
                           'unique_X_share': len(unique_X_list) / runs}
        
        if np.average(fs) < f_avg_min:
            f_avg_min = np.average(fs)
            opt_f_avg_min = opt_desc
        
        if f_best < f_best_min:
            f_best_min = f_best
            opt_f_best_min = opt_desc
            
    if printout:    
        
        table = Table(title=f'Indago inspect_optimizers results ({runs} runs)')
        
        table.add_column('Optimizer', justify='left', style='magenta')
        table.add_column('Avg run time (s)', justify='left', style='cyan')
        table.add_column('Fitness (avg +/- std)', justify='left', style='cyan')
        table.add_column('Best fitness', justify='left', style='cyan')
        table.add_column('Best objectives', justify='left', style='cyan')
        table.add_column('Best constraints', justify='left', style='cyan')
        table.add_column('Unique X share (%)', justify='left', style='cyan')      
        
        for opt_desc, data in TABLE.items():
            table.add_row(opt_desc, f"{data['time_avg']:.2}", 
                          f"{data['f_avg']:e} +/- {data['f_std']:e}",
                          f"{data['f_best']:e}", 
                          f"{data['O_best']}", f"{data['C_best']}",
                          f"{data['unique_X_share']:.0%}",
                          style='bold' if opt_desc in (opt_f_avg_min, opt_f_best_min) else None)
        
        Console().print(table) 
        Console().print(f'[bold][magenta]Best X: [cyan]{X_best}')
        
    return TABLE, X_best
        
    