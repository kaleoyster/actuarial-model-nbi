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
from tqdm import tqdm
from collections import defaultdict
from collections import Counter
from actuarial_functions import *
from plotly.subplots import make_subplots

def identify_windows(from_year, to_year, data):
    """
    Description:
        returns windows and segments the data accordingly

    Args:
        from_year
        to_year

    Return:
        new_data (list)
    """
    new_data = []
    for bridge in data:
        windowed_dataset = data[from_year: to_year]
        new_data.append(windowed_dataset)
    return new_data

def leaves(list_count, list_age):
    """
    Description:
        The number of bridges that leave the study at age x.
    """
    # TODO: Do not need 
    leaves_dict = defaultdict()
    for index in range(0, len(list_count)):
        if index - 1 >= 0:
            prev_count = list_count[index-1]
            current_count = list_count[index]
            leaves_count = current_count - prev_count
            leaves_dict[list_age[index]] = leaves_count
    return leaves_dict

def exposures(list_count, list_age):
    """
    Description:
        The number of bridges in the study at age x.
    """
    # TODO: Do not need 
    exposures_dict = defaultdict()
    for age, count in zip(list_age, list_count):
        exposures_dict[age] = count
    return exposures_dict

def compute_hazard_score(list_count, list_age):
    """
    TODO: Do Not need
    Description:
        returns a computed hazard score.
        based on the leave and exposure

    Args:
        list_count
        list_age

    Return: hazard_dictionary (dictionary)
    """

    # TODO: Do not need 
    # intiate dictionaries
    hazard_dictionary = defaultdict()
    survival_dictionary = defaultdict()

    # compute leaves and exposure
    leave_dict = leaves(list_count, list_age)
    exposure_dict = exposures(list_count, list_age)

    # compute hazard rate
    for age in range(2, 10):
        leave = leave_dict[age]
        exposure = exposure_dict[age]
        exposure_next = exposure_dict[age + 1]
        hazard_rate = exposure_next / exposure
        hazard_dictionary[age] = hazard_rate

    # compute survival rate
    for age in range(2, 10):
        hazard_rate = hazard_dictionary[age]
        survival_rate = 1 - hazard_rate
        survival_dictionary[age] = survival_rate
    return hazard_dictionary, survival_dictionary

def compute_probabilities(hazard_dictionary):
    """
    Description:
        Returns compute probability of survival
        given hazard rates
    """
    # TODO: Do not need 
    probabilities_dict = defaultdict()
    for age, hr in hazard_dictionary.items():
        probabilities_dict[age] = 1 - hr
    return probabilities_dict

def compute_counts(data):
    """
    Description:
        read data and
        compute the number of bridges per age
    Args:
        path
    Returns:
        data
    """
    count_dictionary = defaultdict()
    ages = [value['age'] for value in data.values()]
    for age_list in ages:
        for age in age_list:
            if count_dictionary.get(age) is None:
                count_dictionary[age] = 1
            else:
                count_dictionary[age] = count_dictionary[age] + 1
    return count_dictionary

def age_counter(ages, dictionary):
    """
    Description:
        return a list of counts
    for each age

    Args:
        ages (list)
        dictionary (dictionary):

    Returns:
        list_of_counts
    """
    list_of_counts = []
    for age in ages:
       list_of_counts.append(dictionary[age])
    return list_of_counts

def filter_data(data, column, val):
    """
    Description:
        returns filtered data
    Args:
        data (JSON)
        column (list)
        val (list)
    Returns
        filtered_data (JSON)
    """
    filtered_data = defaultdict()
    for key, value in data.items():
        if value[column][-1] == val:
            filtered_data[key] = value
    return filtered_data

def compute_table(year_total_bridge):
    """
    Description:
        Return a computed table
    Args:
        year_total_bridge (dict)
    Returns:
        year_list (list)
        total_bridge_list (list)
        percentages_list (list)
    """
    year_list = list()
    total_bridge_list = list()
    percentages_list = list()
    for year, total_bridges in year_total_bridge.items():
        if year > 1992:
            lookup_year = year - 1
            lookup_total_bridges = year_total_bridge[lookup_year]
            try:
                percentage = (lookup_total_bridges - total_bridges) / lookup_total_bridges
                year_list.append(year)
                total_bridge_list.append(total_bridges)
                percentages_list.append(percentage)
            except:
                pass
        else:
            year_list.append(year)
            total_bridge_list.append(total_bridges)
            percentages_list.append(0.0)
    return year_list, total_bridge_list, percentages_list

def compute_bridge_count(study_window, data):
    """
    Descriptions:
        Computes the count of the bridges at each year
    Args:
        study_window (years)
        data (JSON)
    Returns:
        year_total_bridge (dictionary)
    """
    total_bridge = len(data.keys())
    bridge_last_year = defaultdict()
    year_total_bridge = defaultdict()

    for bridge, record in data.items():
        last_year = record['year'][-1]
        if bridge_last_year.get(last_year) is None:
            bridge_last_year[last_year] = 1
        else:
            bridge_last_year[last_year] = bridge_last_year[last_year] + 1

    for year in range(study_window[0], study_window[1]):
        lookup_year = year - 1
        if bridge_last_year.get(lookup_year) is not None:
            total_bridge = total_bridge - bridge_last_year[lookup_year]
        year_total_bridge[year] = total_bridge
    return year_total_bridge

def compute_window_statistics(data_new, year_built):
    """
    Description:
        compute the life table statistics for each study window

    Args:
        data_new: (list of list)
        year_built: (list of years)
    """
    saving_indexes = []
    for bridge, record in data_new.items():
        intervention = record['deck intervention']
        year = record['year built']
        if np.mean(year) == year_built:
            try:
                saved_index = intervention.index('Repair')
                saving_indexes.append(saved_index)
            except:
                saved_index = -1

    total_indexes = len(saving_indexes)
    total_data = len(data_new)
    percent_intervention_data = (total_indexes / total_data) * 100
    min_intervention = np.min(saving_indexes)
    max_intervention = np.max(saving_indexes)
    median_intervention = np.median(saving_indexes)
    mean_intervention = np.mean(saving_indexes)

    stats = {
              'total bridges': total_data,
              'total no of bridges with intervention': total_indexes,
              'percentage of bridge with intervention': percent_intervention_data,
              'mean time before intervention': mean_intervention,
              'min time before intervention': min_intervention,
              'max time before intervention': max_intervention,
              'median time before intervention': median_intervention
            }
    return stats

def get_yLabels(study_window_years):
    """
    Description:
        Get study window years and return string y-labels
    """
    yNames = []
    for year in study_window_years:
        string = str(year[0]) + '-' + str(year[1])
        yNames.append(string)
    return yNames

def main():
    # Path of the Nebraska
    #path = '../data/gravel-nebraska.json'
    path = '../data/nebraska_sample.json'
    data = read_json(path)

    age_condiion_dict = age_condition_distribution(data)
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
    df, mRates, ages = compute_life_table_utility(data,
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
        # median_mrates.append(np.median(new_list[2:]))
        median_mrates.append(np.mean(new_list[2:]))

    title = 'Nebraska'
    yNames = get_yLabels(study_window_years)

    yNames = ['mean']
    mRates = [median_mrates]

    #plot_line(ages, mRates, yNames, title)
    #plot_heatmap(ages, mrates, ynames, title)

    new_study_window = []
    for window in study_window_years:
        transformed_study_window = str(window[0]) + ' - ' + str(window[1])
        new_study_window.append(transformed_study_window)

    study_window = new_study_window

    for dataframe, study_window in zip(df, study_window):
        dataframe.columns = ['Age',
                      'Population (P)',
                      'Death (D)',
                      'Death rate (m)',
                      'Conditional Prob. Death (q)',
                      'Conditional Prob. Survival (p)',
                      'Person year lived (L)',
                      'Total year lived (T)',
                      'Life expectancy (E)']
        #plot_table(dataframe, study_window)


    # Average daily traffic - compute life tables
    field = 'adt category'
    yNames = ['Ultra Light',
              'Very Light',
              'Light',
              'Moderate',
              'High']

    heatmaps = []
    life_expectancy = []
    for category in yNames:
        df, rates = periodic_lifetable_by_category(data,
                                          study_window_years,
                                          field,
                                          category)
        for adt_df in df:
            print(adt_df.columns)
            expectancy = adt_df['E']
        life_expectancy.append(expectancy)

    import plotly.graph_objects as go

    # Add data
    #month = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
    #         'August', 'September', 'October', 'November', 'December']

    # year
    age = df[0]['Age']
    ultra_adt = df[0]['q']
    very_adt = df[1]['q']
    light_adt = df[2]['q']
    moderate_adt = df[3]['q']
    high_adt = df[4]['q']
    fig = go.Figure()

    # Create and style traces
    fig.add_trace(go.Scatter(x=age, y=ultra_adt, name='Ultra ADT',
                             line=dict(color='firebrick', width=4)))
    fig.add_trace(go.Scatter(x=age, y=very_adt, name = 'Very Light ADT',
                             line=dict(color='royalblue', width=4)))
    fig.add_trace(go.Scatter(x=age, y=light_adt, name='light ADT',
                             line=dict(color='firebrick', width=4,
                                  dash='dash') # dash options include 'dash', 'dot', and 'dashdot'
    ))
    fig.add_trace(go.Scatter(x=age, y=moderate_adt, name='moderate ADT',
                             line = dict(color='royalblue', width=4, dash='dash')))
    fig.add_trace(go.Scatter(x=age, y=high_adt, name='High ADT',
                             line = dict(color='firebrick', width=4, dash='dot')))
    #fig.add_trace(go.Scatter(x=month, y=low_2000, name='Low 2000',
    #                         line=dict(color='royalblue', width=4, dash='dot')))

    # Edit the layout
    fig.update_layout(title='Life Expectancy of bridge w.r.t the average daily traffic',
                       xaxis_title='Age',
                       yaxis_title=' Death Rate (q)')


    fig.show()

    df = pd.DataFrame({'Age': age,
                       'Ultra Light ADT (E)': ultra_adt,
                       'Very Light ADT (E)': very_adt,
                       'Light ADT (E)': light_adt,
                       'Moderate ADT (E)': moderate_adt,
                       'High ADT (E)': high_adt,
                      })

    t_title = '<b>Life expectancy </b>'
    t_title =  t_title + ' -- ' + '<b>'+ study_window + '</b>'
    fig = go.Figure(data=[go.Table(
        header=dict(values=list(df.columns),
                fill_color='paleturquoise',
                align='left'),
                cells=dict(values=[df['Age'],
                           df['Ultra Light ADT (E)'],
                           df['Very Light ADT (E)'],
                           df['Light ADT (E)'],
                           df['Moderate ADT (E)'],
                           df['High ADT (E)'],
                          ],

               fill_color='lavender',
               align='left'))
        ])

    fig.update_layout(title_text=t_title)
    fig.show()


        #print("printing rates", rates)
        #heatmaps.append(rates[0])
    #plot_heatmap(ages, heatmaps, yNames)

    # Owner
    #field = 'owner'
    #yNames = ['1', '2', '3', '4']
    #heatmaps = []
    #for category in yNames:
    #    rates = compute_categorical_lifetable(data,
    #                                      study_window_years,
    #                                      field,
    #                                      category)
    #    heatmaps.append(rates[0])
    #plot_heatmap(ages, heatmaps, yNames)

    #for age, intervention in age_intervention.items():
    #    print(age, len(intervention))
    #print(len(data))
    #year = 1992
    #data_new = filter_data(data, 'year built', year)

    # Study window
    #for year in range(1992, 2010):
    #    data_new = filter_data(data, 'year built', year)
    #    print(year)
    #    print(compute_window_statistics(data_new, year))

    # Exists until maintenance
    # Absolutely no exisitance
    #year_total_bridge = compute_bridge_count(study_window, data)
    #year_list, total_bridge_list, percentages_list = compute_table(year_total_bridge)
    #df = pd.DataFrame({'Year': year_list,
    #                   'Total':total_bridge_list,
    #                   'Percentage':percentages_list})
    #print(df)

    #print(year_list, total_bridge_list, percentages_list)
    #count_dictionary = compute_counts(data)
    #ages = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    #counts = age_counter(ages, count_dictionary)
    #hazard, survival = compute_hazard_score(counts, ages)
    #probabilities = compute_probabilities(hazard)


if __name__=='__main__':
    main()
