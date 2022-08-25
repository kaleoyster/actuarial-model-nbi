"""
Description:
    Validation script for actuarial model

Author:
    Akshay Kale

Date:
     August 9th, 2022
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
    ages = [
        0,
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
        11
    ]
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
                  49233
                 ]

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

    df = pd.DataFrame({'Age': age_list[:-1],
                       'P': P[:-1],
                       'D': D[:-1],
                       'm': m[:-1],
                       'q': q[:-1],
                       'p': p[:-1],
                       'L': L,
                       'T': T,
                       'E': e
    })

    print(df)

def main():
    """
    Driver function
    """
    study_window_years = [[1992, 2022]]
    bridge_data = simulation_bridge_life_cycle(1000, 1992, 2022)
    df, mRates, ages = compute_life_table_utility(bridge_data,
                               study_window_years,
                               '',
                               'Repair')
    yNames = ['Apple']
    plot_line(ages, mRates, yNames)
    plot_heatmap(ages, mRates, yNames)
    print(df)



if __name__ == '__main__':
    main()
