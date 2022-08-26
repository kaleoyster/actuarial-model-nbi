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
    #study_window_years = [[1992, 2022]]
    study_window_years = [[1992, 1998],
                          [1996, 2002],
                          [1998, 2004],
                          [2002, 2006],
                          [2004, 2008],
                          [2006, 2010],
                          [2008, 2012],
                          [2010, 2014],
                          [2012, 2016]]

    bridge_data = simulation_bridge_life_cycle(1000, 1992, 2022)

    df, mRates, ages = compute_life_table_utility(bridge_data,
                               study_window_years,
                               '',
                               'Repair')
    #yNames = ['Simulation']
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
    plot_line(ages, mRates, yNames)
    plot_heatmap(ages, mRates, yNames)

    df.columns = ['Age',
                  'Population (P)',
                  'Death (D)',
                  'Death rate (m)',
                  'Conditional Prob. Death (q)',
                  'Conditional Prob. Survival (p)',
                  'Person year lived (L)',
                  'Total year lived (T)',
                  'Life expectancy (E)']

    fig = go.Figure(data=[go.Table(
        header=dict(values=list(df.columns),
                fill_color='paleturquoise',
                align='left'),

                cells=dict(values=[df['Age'],
                           df['Population (P)'],
                           df['Death (D)'],
                           df['Death rate (m)'],
                           df['Conditional Prob. Death (q)'],
                           df['Conditional Prob. Survival (p)'],
                           df['Person year lived (L)'],
                           df['Total year lived (T)'],
                           df['Life expectancy (E)']
                          ],

               fill_color='lavender',
               align='left'))
        ])

    fig.show()
    print(df)



if __name__ == '__main__':
    main()
