"""
Description: Validation script for actuarial model
Author: Akshay Kale
Date: August 9th, 2022
"""
import json
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.figure_factory as ff

from tqdm import tqdm
from collections import defaultdict
from collections import Counter
from actuarial_functions import *

def test1():
    """
    driver function
    """
    ages = [ 0,
             1,
             2,
             3,
             4,
             5,
             6,
             7,
             8,
             9,
             10,
             11]

    population = [48283,
                  47195,
                  48140,
                  50017,
                  49189,
                  49543,
                  49951,
                  49758,
                  49728,
                  49909,
                  49051,
                  49233]

    death = [136,
             8,
             3,
             5,
             2,
             6,
             6,
             2,
             2,
             3,
             2,
             1]

    age_list, P, D, m, q, p, l, L, T, e = compute_periodic_life_table(ages,
                               population,
                               death,
                               end_age=11)

    df = pd.DataFrame({'a': age_list[:-1],
                       'P - (Population)': P[:-1],
                       'D - (Death)': D[:-1],
                       'm - (Death Rate)': m[:-1],
                       'q - (Cond. Prob. Death) ': q[:-1],
                       'p - (Cond. Prob. Survival)': p[:-1],
                       'L - (Life lived)': L,
                       'T - (Total time)': T,
                       'E - (life expectancy)': e
    })
    return df


def main():
    """
    Driver function
    """
    study_window_years = [[1992, 1998],
                          [1996, 2002],
                          [1998, 2004],
                          [2002, 2006],
                          [2004, 2008],
                          [2006, 2010],
                          [2008, 2012],
                          [2010, 2014],
                          [2012, 2016]]

    path = '../data/gravel-nebraska.json'
    data = read_json(path)
    age_condition_ratings_dict = age_condition_distribution(data)

    # Convert this into the condition ratings
    age_list = []
    min_list = []
    max_list = []

    for index in range(1, 100):
        min_val, max_val = age_condition_ratings_dict.get(index)
        age_list.append(index)
        min_list.append(min_val)
        max_list.append(max_val)

    df_apple = pd.DataFrame({'age':age_list,
                             'min': min_list,
                             'max': max_list})

    bridge_data = simulation_bridge_life_cycle(1000,
                                               1992,
                                               2022,
                                               age_condition_ratings_dict)

    dfs, mRates, ages = compute_life_table_utility(bridge_data,
                               study_window_years,
                               '',
                               'Repair')
    total_length = len(mRates)
    cols_values = []
    mrate_dict = defaultdict()
    mrate_dict['age'] = list(range(1, len(mRates[0])+1))

    for extra_col in range(0, total_length):
        suffix = extra_col + 1
        col_name = 'study window ' + str(extra_col)
        mrate_dict[col_name] = mRates[extra_col]
    df_mrates = pd.DataFrame(mrate_dict)

    median_mrates = list()
    for row in df_mrates.itertuples():
        new_list = list(row)
        median_mrates.append(np.median(new_list[2:]))

    yNames= [
        '1992 - 1998',
        '1996 - 2002',
        '1998 - 2004',
        '2002 - 2006',
        '2004 - 2008',
        '2006 - 2010',
        '2008 - 2012',
        '2010 - 2014',
        '2012 - 2016',
    ]

    yNames = ['median']
    title = "Simulation"
    mRates = [median_mrates]

    plot_line(ages, mRates, yNames, title)
    plot_heatmap(ages, mRates, yNames, title)
    #plot_line(ages, mRates, yNames, title)
    #plot_heatmap(ages, mRates, yNames, title)
    #for df, study_window in zip(dfs, yNames):
    #    df.columns = ['Age',
    #                  'Population (P)',
    #                  'Death (D)',
    #                  'Death rate (m)',
    #                  'Conditional Prob. Death (q)',
    #                  'Conditional Prob. Survival (p)',
    #                  'Person year lived (L)',
    #                  'Total year lived (T)',
    #                  'Life expectancy (E)']
    #    plot_table(df, study_window)

if __name__ == '__main__':
    main()
