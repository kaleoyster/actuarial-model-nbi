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
                          [2000, 2006],
                          [2004, 2010],
                          [2008, 2014],
                          [2010, 2016]]

    condition_ratings = {
                        0:  [9, 9],
                        1:  [9, 9],
                        2:  [8, 9],
                        3:  [8, 9],
                        4:  [8, 9],
                        5:  [8, 9],
                        6:  [8, 9],
                        7:  [8, 9],
                        8:  [8, 9],
                        9:  [7, 9],
                        10: [7, 9],
                        11: [7, 9],
                        12: [7, 9],
                        13: [7, 9],
                        14: [7, 9],
                        15: [7, 9],
                        16: [7, 9],
                        17: [7, 9],
                        18: [7, 9],
                        19: [7, 9],
                        20: [7, 9],
                        21: [6, 9],
                        22: [6, 9],
                        23: [6, 9],
                        24: [6, 9],
                        25: [6, 9],
                        26: [6, 9],
                        27: [6, 9],
                        28: [6, 9],
                        29: [6, 9],
                        30: [6, 9],
                        31: [5, 9],
                        32: [5, 9],
                        33: [5, 9],
                        34: [5, 9],
                        35: [5, 9],
                        36: [5, 9],
                        37: [5, 9],
                        38: [5, 9],
                        39: [5, 9],
                        40: [4, 9],
                        41: [4, 9],
                        42: [4, 9],
                        43: [4, 9],
                        44: [4, 9],
                        45: [4, 9],
                        46: [4, 9],
                        47: [4, 9],
                        48: [4, 9],
                        49: [4, 9],
                        50: [3, 9],
                        51: [3, 9],
                        52: [3, 9],
                        53: [3, 9],
                        54: [3, 9],
                        55: [3, 9],
                        56: [3, 9],
                        57: [3, 9],
                        58: [3, 9],
                        59: [3, 9],
                        60: [3, 9],
                        61: [3, 6],
                        62: [3, 6],
                        63: [3, 6],
                        64: [3, 5],
                        65: [3, 5],
                        66: [3, 5],
                        67: [3, 5],
                        68: [3, 5],
                        69: [3, 5],
                        70: [3, 5],
                        71: [3, 6],
                        72: [3, 6],
                        73: [3, 6],
                        74: [3, 5],
                        75: [3, 5],
                        76: [3, 5],
                        77: [3, 5],
                        78: [3, 5],
                        79: [3, 5],
                        80: [3, 5],
                        81: [3, 6],
                        82: [3, 6],
                        83: [3, 6],
                        84: [3, 5],
                        85: [3, 5],
                        86: [3, 5],
                        87: [3, 5],
                        88: [3, 5],
                        89: [3, 5],
                        90: [3, 5],
                        91: [3, 6],
                        92: [3, 6],
                        93: [3, 6],
                        94: [3, 5],
                        95: [3, 5],
                        96: [3, 5],
                        97: [3, 5],
                        98: [3, 5],
                        99: [3, 5],
                        100: [3, 5],
                    }

#    condition_ratings = {
#                        1:  [9, 9],
#                        2:  [9, 9],
#                        3:  [9, 9],
#                        4:  [9, 9],
#                        5:  [9, 9],
#                        6:  [8, 9],
#                        7:  [8, 9],
#                        8:  [8, 9],
#                        9:  [8, 9],
#                        10: [8, 9],
#                        11: [7, 9],
#                        12: [7, 9],
#                        13: [7, 9],
#                        14: [7, 9],
#                        15: [6, 8],
#                        16: [6, 8],
#                        17: [6, 8],
#                        18: [6, 8],
#                        19: [6, 8],
#                        20: [6, 8],
#                        21: [5, 8],
#                        22: [5, 8],
#                        23: [5, 8],
#                        24: [5, 8],
#                        25: [5, 8],
#                        26: [4, 8],
#                        27: [4, 8],
#                        28: [4, 8],
#                        29: [4, 8],
#                        30: [4, 8],
#                        31: [3, 7],
#                        32: [3, 7],
#                        33: [3, 7],
#                        34: [3, 7],
#                        35: [3, 7],
#                        36: [2, 7],
#                        37: [2, 7],
#                        38: [2, 7],
#                        39: [2, 7],
#                        40: [2, 7],
#                        41: [2, 7],
#                        42: [2, 7],
#                        43: [2, 7],
#                        44: [2, 7],
#                        45: [2, 7],
#                        46: [2, 6],
#                        47: [2, 6],
#                        48: [2, 6],
#                        49: [2, 6],
#                        50: [2, 6],
#                        51: [2, 6],
#                        52: [2, 6],
#                        53: [2, 6],
#                        54: [2, 6],
#                        55: [2, 5],
#                        56: [2, 5],
#                        57: [2, 5],
#                        58: [2, 5],
#                        59: [2, 5],
#                        60: [2, 5],
#                        61: [2, 6],
#                        62: [2, 6],
#                        63: [2, 6],
#                        64: [2, 5],
#                        65: [2, 5],
#                        66: [2, 5],
#                        67: [2, 5],
#                        68: [2, 5],
#                        69: [2, 5],
#                        70: [2, 5],
#                        71: [3, 6],
#                        72: [3, 6],
#                        73: [3, 6],
#                        74: [3, 5],
#                        75: [3, 5],
#                        76: [3, 5],
#                        77: [3, 5],
#                        78: [3, 5],
#                        79: [3, 5],
#                        80: [3, 5],
#                        81: [3, 6],
#                        82: [3, 6],
#                        83: [3, 6],
#                        84: [3, 5],
#                        85: [3, 5],
#                        86: [3, 5],
#                        87: [3, 5],
#                        88: [3, 5],
#                        89: [3, 5],
#                        90: [3, 5],
#                        91: [3, 6],
#                        92: [3, 6],
#                        93: [3, 6],
#                        94: [3, 5],
#                        95: [3, 5],
#                        96: [3, 5],
#                        97: [3, 5],
#                        98: [3, 5],
#                        99: [3, 5],
#                        100: [3, 5],
#                    }

    #path = '../data/gravel-nebraska.json'
    path = '../data/nebraska_sample.json'
    data = read_json(path)
    #age_condition_ratings_dict = age_condition_distribution(data)
    #print(age_condition_ratings_dict)
    #print(age_condition_ratings_dict)

    ## Convert this into the condition ratings
    #age_list = []
    #min_list = []
    #max_list = []

    #for index in range(1, 100):
    #    min_val, max_val = age_condition_ratings_dict.get(index)
    #    age_list.append(index)
    #    min_list.append(min_val)
    #    max_list.append(max_val)

    #df_apple = pd.DataFrame({'age':age_list,
    #                         'min': min_list,
    #                         'max': max_list})

    bridge_data = simulation_bridge_life_cycle(1000,
                                               1992,
                                               2022,
                                               condition_ratings)

    dfs, mRates, ages = compute_life_table_utility(bridge_data,
                               study_window_years,
                               '',
                               'Repair')
    for df in dfs:
        print(df.columns)
        print(df['Age'])
        print(df['q'])
        print(df['m'])

    fig = go.Figure()
    ## Create and style traces
    fig.add_trace(go.Scatter(x=df['Age'], y=df['q'], name='Simulated Data',
                             line=dict(color='firebrick', width=4)))
    #fig.add_trace(go.Scatter(x=age, y=very_adt, name = 'Very Light ADT',
    #                         line=dict(color='royalblue', width=4)))
    #fig.add_trace(go.Scatter(x=age, y=light_adt, name='light ADT',
    #                         line=dict(color='firebrick', width=4,
    #                              dash='dash') # dash options include 'dash', 'dot', and 'dashdot'
    #))
    #fig.add_trace(go.Scatter(x=age, y=moderate_adt, 
    #                                name='moderate ADT',
    #                         line = dict(color='royalblue', width=4, dash='dash')))
    #fig.add_trace(go.Scatter(x=age, y=high_adt, name='High ADT',
    #                         line = dict(color='firebrick', width=4, dash='dot')))
    #fig.add_trace(go.Scatter(x=month, y=low_2000, name='Low 2000',
    #                         line=dict(color='royalblue', width=4, dash='dot')))

    # Edit the layout
    fig.update_layout(title='Repair Rate (m) of Simulated Bridge',
                       xaxis_title='Age',
                       yaxis_title='Repair Rate (m)')


    fig.show()



    #total_length = len(mRates)
    #cols_values = []
    #mrate_dict = defaultdict()
    #mrate_dict['age'] = list(range(1, len(mRates[0])+1))

    #for extra_col in range(0, total_length):
    #    suffix = extra_col + 1
    #    col_name = 'study window ' + str(extra_col)
    #    mrate_dict[col_name] = mRates[extra_col]
    #df_mrates = pd.DataFrame(mrate_dict)

    #median_mrates = list()
    #for row in df_mrates.itertuples():
    #    new_list = list(row)
    #    median_mrates.append(np.median(new_list[2:]))

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

    #yNames = ['median']
    #title = "Simulation"
    #mRates = [median_mrates]

    #plot_line(ages, mRates, yNames, title)
    #plot_heatmap(ages, mRates, yNames, title)

    #new_study_window = []
    #for window in study_window_years:
    #    transformed_study_window = str(window[0]) + ' - ' + str(window[1])
    #    new_study_window.append(transformed_study_window)
    #study_window = new_study_window

    #for dataframe, study_window in zip(dfs, study_window):
    #    dataframe.columns = ['Age',
    #                  'Population (P)',
    #                  'Repair (D)',
    #                  'Repair rate (m)',
    #                  'Conditional Prob. Death (q)',
    #                  'Conditional Prob. Survival (p)',
    #                  'Bridge year lived (L)',
    #                  'Total year lived (T)',
    #                  'Life expectancy (E)']
    #plot_line(ages, mRates, yNames, title)
    #plot_heatmap(ages, mRates, yNames, title)
    for df, study_window in zip(dfs, yNames):
        df.columns = ['Age',
                      'Population (P)',
                      'Death (D)',
                      'Death rate (m)',
                      'Conditional Prob. Death (q)',
                      'Conditional Prob. Survival (p)',
                      'Person year lived (L)',
                      'Total year lived (T)',
                      'Life expectancy (E)']
        #plot_table(df, study_window)
        plot_table(df, '2012-2016')

if __name__ == '__main__':
    main()
