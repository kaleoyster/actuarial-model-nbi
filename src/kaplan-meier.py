"""
Description:
    Script to run the actuarial model.

Author:
    Akshay Kale

Credits:
   The idea and implementation of this project was first initiated by O'Brien Chin.

Date:
    29th June, 2022
"""
import json
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import kaplanmeier as km
import matplotlib.pyplot as plt
from tqdm import tqdm
from collections import defaultdict
from collections import Counter
from actuarial_functions import *
from plotly.subplots import make_subplots

def study_window(data, study_window_year):
    """
    Description:
        Return data by filtering study_window

    Args:
        study_window_year

    Return:
        data
    """
    new_data = defaultdict()
    starting_year, ending_year = study_window_year
    for bridge, record in data.items():
        years = record['year']
        ages = record['age']
        interventions = record['deck intervention']
        new_years = []
        new_ages = []
        new_interventions = []
        try:
            start_index = years.index(starting_year)
            end_index = years.index(ending_year)
            new_years = years[start_index:end_index]
            new_ages = ages[start_index:end_index]
            new_interventions = interventions[start_index:end_index]
            temp_dict = {
                'year':new_years,
                'age':new_ages,
                'intervention':new_interventions
            }
            new_data[bridge] = temp_dict
        except:
            pass
    return new_data

def main():
    # Path of the Nebraska
    #path = '../data/gravel-nebraska.json'
    path = '../data/nebraska_sample.json'
    data = read_json(path)

    age_condition_dict = age_condition_distribution(data)
    study_window_years = [[1992, 1998],
                          [1996, 2002],
                          [1998, 2004],
                          [2002, 2006],
                          [2004, 2008],
                          [2006, 2010],
                          [2008, 2012],
                          [2010, 2014],
                          [2012, 2016]]

    # Overall rates <- baseline
    dataframes, mRates, ages = compute_life_table_utility(data,
                               study_window_years,
                               '',
                               'Repair')

    temp_dfs = []
    for df, study_window in zip(dataframes, study_window_years):
        year = '-'.join([str(num) for num in study_window])
        df['group'] = [year]*len(df)
        temp_dfs.append(df)

    tdf = pd.concat(temp_dfs)
    #print(tdf['group'].unique())

    # import example data
    #df = km.example_data()

    ## Data
    time_event = tdf['Age']
    censoring = tdf['D']
    y = tdf['group']

    ## Compute survival
    results = km.fit(time_event, censoring, y)
    print(results)

    ## Plot
    km.plot(results)
    plt.show()

if __name__=='__main__':
    main()

