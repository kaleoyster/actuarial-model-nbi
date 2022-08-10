"""
Description:
    This is a script to run the actuarial model.

Author:
    Akshay Kale

Credits:
   The idea and implementation of this project was first initiated by O'Brien Chin.
Notes:
    1. Exposures is the same as count_dictionary
    compute counts can be renamed as exposures.

    2. Adjust the study windows to mimic bridges born during the same year.
        - Done

    3. Re-create the life table. [ Done ]
        - Some of the bridges  appear in the later time but do not appear in the earlier timeline.
        - Look for bridges that do not appear at all in the later time line.

Date:
    29th June, 2022
"""

import json
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from tqdm import tqdm
from collections import defaultdict
from collections import Counter

def create_dummy_data():
    """
    Description:
        returns dummy nbi data
    """
    data = [
        [1992, 1993, 1994, 1995], # year
        [1934, 1934, 1934, 1934], # year built
        [9, 9, 9, 8], # condition rating (deck)
        [1954, 1954, 1994, 1994], # condition rating (deck)
    ]
    return data

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
        # There must be a new function for windowed data
        windowed_dataset = data[from_year: to_year]
        new_data.append(windowed_dataset)
    return new_data

def leaves(list_count, list_age):
    """
    Description:
        The number of bridges that leave the study at age x.
    """
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
    exposures_dict = defaultdict()
    for age, count in zip(list_age, list_count):
        exposures_dict[age] = count
    return exposures_dict

def compute_hazard_score(list_count, list_age):
    """
    Description:
        returns a computed hazard score.
        based on the leave and exposure

    Args:
        list_count
        list_age

    Return: hazard_dictionary (dictionary)
    """
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
    probabilities_dict = defaultdict()
    for age, hr in hazard_dictionary.items():
        probabilities_dict[age] = 1 - hr
    return probabilities_dict

def read_json(path):
    """
    Description:
       reads json file
    Args:
        path (string)
    Returns:
        dictionary
    """
    file_obj = open(path)
    data = json.load(file_obj)
    file_obj.close()
    return data

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

def compute_life_table(data,
                       study_window_years,
                       intervention_type,
                       end_age=70):
    """
    Description:
        computes period life table based on the period
    """
    # Initial population
    initial_population = 100000
    intervention_type = 'Repair'

    # Get data from study
    new_data = study_window(data, study_window_years)
    age_intervention = defaultdict(list)
    age_count = defaultdict()

    # Compute age_intervention dictionary
    for bridge, record in new_data.items():
        ages = record['age']
        interventions = record['intervention']
        for age, intervention in zip(ages, interventions):
            age_intervention[age].append(intervention)

    age_list = []
    population_list = []
    mortality_rate_list = []

    for age in range(1, end_age):
        total_number_bridges = len(age_intervention[age])
        counter_intervention = Counter(age_intervention[age])
        # For every age -> Counter({Interventions: Intervention number})

        # TODO: A separate function that takes population and death and outputs all statistics
        # Population = Bridges alive
        # Death (D) = Bridges died (Intervened)
        
        # computation of mortality rate
        try:
            mortality_rate = counter_intervention[intervention_type] / total_number_bridges
        except:
            mortality_rate = 0.0

        death = initial_population * mortality_rate
        death = round(death)

        # Append all computed statistics to the list
        age_list.append(age)
        population_list.append(initial_population)
        mortality_rate_list.append(mortality_rate)
        initial_population = initial_population - death

        # Create the dataframes
        df = pd.DataFrame({'Age':age_list,
                           'Population':population_list,
                           'Mortality rate':mortality_rate_list})
    return df

def plot_line(ages, mRates, yNames):
    """
    Description:
        plot line graph
    args:
        ages
        mrates
    return:
        plot
    """
    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    # Add traces
    for index, mrates in enumerate(mRates):
        fig.add_trace(
            go.Scatter(
                   x=ages,
                   y=mrates,
                   name=yNames[index]),
        )

    # Add figure title
    fig.update_layout(
        title_text="Mortality rates of Bridges across age 1 to 100"
    )

    # Set x-axis title
    fig.update_xaxes(title_text="Age")

    # Set y-axes titles
    fig.update_yaxes(title_text="<b>Mortality Rates</b> ", secondary_y=False)
    #fig.update_yaxes(title_text="<b>secondary</b> yaxis title", secondary_y=True)

    fig.show()

def plot_heatmap(ages, mrates, yNames):
    """
    Description:
    """
    fig = go.Figure(data=go.Heatmap(
                z=mrates,
                x=ages,
                y=yNames))
    fig.show()

def compute_life_table_utility(categoryTemp, study_window_years, category, intervention):
    tempValues = []
    for window in tqdm(study_window_years):
        csv_file = 'life-table-'+ str(window[0]) + '-' + str(window[1]) + '-' + category + '.csv'
        tempDf = compute_life_table(categoryTemp, window, intervention)
        ages = list(tempDf['Age'])
        tempValues.append(list(tempDf['Mortality rate']))
        tempDf.to_csv(csv_file)
    return tempValues, ages

def compute_categorical_lifetable(data, study_window_years, field, category):
    """
    Description:
        Create categorical life tables

    Args:
        data

    Returns:
        study window years
    """

    intervention = 'Repair'
    # Prepare dataset for only category 
    categoryTemp = defaultdict()
    for key, record in data.items():
        cat = record['adt category']
        if cat[-1] == category:
            categoryTemp[key] = record

    tempValues, ages = compute_life_table_utility(categoryTemp,
                                            study_window_years,
                                            category,
                                            intervention)

    return tempValues

def main():
    # Path of the Nebraska
    path = '../data/nebraska.json'
    data = read_json(path)
    study_window_years = [[1992, 1996],
                          [1996, 2000],
                          [2000, 2004],
                          [2004, 2008],
                          [2008, 2012],
                          [2012, 2016]]

    # Overall rates <- baseline
    mRates, ages = compute_life_table_utility(data,
                               study_window_years,
                               '',
                               'Repair')
    yNames = ['1992-1996',
              '1996-2000',
              '2000-2004',
              '2004-2008',
              '2008-2012',
              '2012-2016']
    plot_line(ages, mRates, yNames)
    plot_heatmap(ages, mRates, yNames)

    # Average daily traffic
    field = 'adt category'
    yNames = ['Ultra Light',
              'Very Light',
              'Light',
              'Moderate',
              'High']

    heatmaps = []
    for category in yNames:
        rates = compute_categorical_lifetable(data,
                                          study_window_years,
                                          field,
                                          category)
        heatmaps.append(rates[0])
    plot_heatmap(ages, heatmaps, yNames)

    # Owner
    field = 'owner'
    yNames = ['1', '2', '3', '4']
    heatmaps = []
    for category in yNames:
        rates = compute_categorical_lifetable(data,
                                          study_window_years,
                                          field,
                                          category)
        heatmaps.append(rates[0])
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
