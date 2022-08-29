"""
Description: This is a script contains actuarial functions
Author: Akshay Kale
Credits: O'Brien Chin
Date: 11th August, 2022
"""

import json
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import random
from tqdm import tqdm
from collections import defaultdict
from collections import Counter
from plotly.subplots import make_subplots

def periodic_lifetable_by_category(data, study_window_years, field, category):
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

    df, tempValues, ages = compute_life_table_utility(categoryTemp,
                                            study_window_years,
                                            category,
                                            intervention)
    return tempValues


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

def compute_periodic_life_table(ages,
                                total_number_of_bridges,
                                number_of_interventions,
                                end_age):
    """
    Description
        Compute a periodic lifetable

    Args:
        Total number of bridges (list): population
        number of intervention (list): death
    """
    age_list = []

    # Population
    list_P_x = []

    # Death
    list_D_x = []

    # Central death rate
    list_m_x = []

    # Conditional probability of death
    list_q_x = []

    # Conditional probability of survival
    list_p_x = []

    # Number surviving to age x
    list_l_x = []

    # Person year lived at age 1
    list_L_x = []

    # Total years lived from age X
    list_T_x = []

    # Total life expectancy e_x
    list_e_x = []

    # Initiation
    initial_population = 100000

    for i in range(1, end_age):
        age = ages[i]

        # Population
        P_x = total_number_of_bridges[i]

        # Number of intervention
        D_x =  number_of_interventions[i]

        # Death rate
        m_x = D_x / P_x

        # Conditional probability of death
        q_x = (D_x / (P_x + (0.5 * D_x)))

        # Condition probability of Survival 
        p_x = 1 - q_x

        # Number of surviving to age x
        l_x = initial_population * p_x
        #l_x = l_dict[2] / l_x

        age_list.append(age)
        list_P_x.append(P_x)
        list_D_x.append(D_x)
        list_m_x.append(m_x)
        list_q_x.append(q_x)
        list_p_x.append(p_x)
        list_l_x.append(l_x)

    # Calculate L_x (person year lived at age x)
    for i in range(0, (len(list_l_x) - 1)):
        L_x = (list_l_x[i] + list_l_x[i+1]) / 2
        list_L_x.append(L_x)

    # Calculate T_x: Total years lived from age x 
    for i in range(0, len(list_L_x)):
        T_x = sum(list_L_x[i:])
        list_T_x.append(T_x)

    # Calculate e_x: Life expectancy
    for i in range(0, len(list_T_x)):
        e_x = list_T_x[i] / list_l_x[i]
        list_e_x.append(e_x)

    return age_list, list_P_x, list_D_x, list_m_x, \
           list_q_x, list_p_x, list_l_x, list_L_x, list_T_x, list_e_x

def compute_life_table(data,
                       study_window_years,
                       intervention_type,
                       end_age=50):
    """
    Description:
        Computes period life table based on the period

    Args:
        study_window_years:
        Intervention_type:

    Returns:
        A life table
    """
    # Get data from study, by study_window_years
    new_data = study_window(data, study_window_years)
    age_intervention = defaultdict(list)
    age_count = defaultdict()

    # Compute age_intervention dictionary
    number_of_interventions = []
    total_number_of_bridges = []
    all_ages = []

    for bridge, record in new_data.items():
        ages = record['age']
        interventions = record['intervention']

        # TODO; all for all the interventions
        if 'Repair' in interventions:
            index_intervention = interventions.index('Repair')
            index_intervention = index_intervention + 1
            ages = ages[:index_intervention]
            interventions = interventions[:index_intervention]

        for age, intervention in zip(ages, interventions):
            age_intervention[age].append(intervention)

    for counter in range(0, end_age):
        all_ages.append(counter)
        interventions = age_intervention[counter]
        total_number_of_bridges.append(len(interventions))
        intervention_counter = Counter(interventions)
        if intervention_type == 'All':
            total_none_count = intervention_counter[None] \
                + intervention_counter['Insp. Variance']
            total_count = sum(intervention_counter.values())
            total_inter_count = total_count - total_none_count
            intervention = total_inter_count
        else:
           intervention = intervention_counter[intervention_type]
        number_of_interventions.append(intervention)

    age_list, P, D, m, q, p, l, L, T, e = compute_periodic_life_table(all_ages,
                                                                   total_number_of_bridges,
                                                                   number_of_interventions,
                                                                   end_age=50)

    df = pd.DataFrame({'Age': age_list[:-1],
                       'Population (p)': P[:-1],
                       'D': D[:-1],
                       'm': m[:-1],
                       'q': q[:-1],
                       'p': p[:-1],
                       'L': L,
                       'T': T,
                       'E': e
    })
    return df

def compute_life_table_utility(categoryTemp,
                               study_window_years,
                               category,
                               intervention):
    """
    Description:
    Agrs:
    Return:
    """
    tempValues = []
    for window in tqdm(study_window_years):
        csv_file = 'life-table-'+ str(window[0]) + '-' + str(window[1]) + '-' + category + '.csv'
        tempDf = compute_life_table(categoryTemp, window, intervention)
        ages = list(tempDf['Age'])
        tempValues.append(list(tempDf['q']))
        tempDf.to_csv(csv_file)
        # TODO: store all the df's in a list 
    return tempDf, tempValues, ages


def generate_condition_rating(age):
    """
    Return a corresponding condition rating for the age
    """
    condition_ratings = {
                        1:  [9, 9],
                        2:  [7, 9],
                        3:  [6, 9],
                        4:  [6, 9],
                        5:  [6, 9],
                        6:  [6, 9],
                        7:  [6, 9],
                        8:  [6, 9],
                        9:  [6, 9],
                        10: [6, 8],
                        11: [6, 8],
                        12: [6, 8],
                        13: [6, 8],
                        14: [6, 8],
                        15: [5, 8],
                        16: [5, 8],
                        17: [5, 8],
                        18: [5, 8],
                        19: [5, 8],
                        20: [3, 7],
                        21: [3, 6],
                        22: [3, 6],
                        23: [3, 6],
                        24: [3, 5],
                        25: [3, 5],
                        26: [3, 5],
                        27: [3, 5],
                        28: [3, 5],
                        29: [3, 5],
                        30: [3, 5],
                        31: [3, 5],
                        32: [3, 6],
                        33: [3, 6],
                        34: [3, 5],
                        35: [3, 5],
                        36: [3, 5],
                        37: [3, 5],
                        38: [3, 5],
                        39: [3, 5],
                        40: [3, 5],
                        41: [6, 8],
                        42: [6, 8],
                        43: [6, 8],
                        44: [6, 8],
                        45: [5, 8],
                        46: [5, 8],
                        47: [5, 8],
                        48: [5, 8],
                        49: [5, 8],
                        50: [3, 7],
                        51: [3, 6],
                        52: [3, 6],
                        53: [3, 6],
                        54: [3, 5],
                        55: [3, 5],
                        56: [3, 5],
                        57: [3, 5],
                        58: [3, 5],
                        59: [3, 5],
                        60: [3, 5],
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

    low_rating, high_rating = condition_ratings[age]
    rating = np.random.uniform(low=low_rating,
                               high=high_rating)
    rating = round(rating)
    return rating

def compute_intervention_utility(condition_ratings):
    """
    Description:
        A utility function for computing possible intervention
    by taking into consideration changes in condition rating.
        The function implemented is based on
        Bridge Intervention Matrix by Tariq et al.

    Note:
         Check for the representation of condition ratings.
         Often the condition ratings are defined as a string,
         Then, these condition rating have to be transformed into interger

    Args:
        condition_ratings (list)

    Returns:
        interventions (list)
        count (int)
    """
    intervention_map = {
                   ('8', '9'):'Insp. Variance',
                   ('7', '9'):'Repair',
                   ('6', '9'):'Repair',
                   ('5', '9'):'Rehab',
                   ('4', '9'):'Replace',
                   ('3', '9'):'Replace',
                   ('2', '9'):'Replace',
                   ('1', '9'):'Not applicable',

                   ('7', '8'):'Insp. Variance',
                   ('6', '8'):'Repair',
                   ('5', '8'):'Repair',
                   ('4', '8'):'Replace',
                   ('3', '8'):'Replace',
                   ('2', '8'):'Replace',
                   ('1', '8'):'Not applicable',

                   ('6', '7'):'Insp. Variance',
                   ('5', '7'):'Repair',
                   ('4', '7'):'Rehab',
                   ('3', '7'):'Rehab',
                   ('2', '7'):'Rehab',
                   ('1', '7'):'Not applicable',

                   ('5', '6'):'Insp. Variance',
                   ('4', '6'):'Repair',
                   ('3', '6'):'Repair',
                   ('2', '6'):'Repair',
                   ('1', '6'):'Not applicable',

                   ('4', '5'):'Insp. Variance',
                   ('3', '5'):'Repair',
                   ('2', '5'):'Repair',
                   ('1', '5'):'Not applicable',

                   ('3', '4'):'Insp. Variance',
                   ('2', '4'):'Repair',
                   ('1', '4'):'Not applicable',

                   ('2', '3'):'Repair',
                   ('1', '3'):'Not applicable',

                   ('1', '2'):'Not applicable'
                  }

    i = 0
    interventions = list()
    interventions.append(None)
    for i in range(len(condition_ratings)-1):
       j = i + 1
       interv = intervention_map.get((str(condition_ratings[i]), str(condition_ratings[j])))
       interventions.append(interv)
    count = len([count for count in interventions if count !=None ])
    return interventions, count

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
        Plot a heat map for with
        respect to age and  mortality rates
    """
    # Convert into percentages
    new_mrates = []
    for mrate_cat in mrates:
        temp_mrate = []
        for mrate in mrate_cat:
            percent = mrate*100
            temp_mrate.append(percent)
        new_mrates.append(temp_mrate)

    # Figure
    fig = go.Figure(data=go.Heatmap(
                z=new_mrates,
                x=ages,
                y=yNames,
                colorbar=dict(title='Percentages')))

    # Add figure title
    fig.update_layout(
        title_text="<b>(Maintenance: Repair) Bridge categories vs. Age </b>"
    )

    fig.show()

def simulation_bridge_life_cycle(population,
                                 start_year,
                                 end_year):
    """
    Description:
        Simulate bridge life cycle of bridges with
        respect to condition ratings.
    """
    population = 100001
    start_age = 1
    #end_age = (end_year - start_year)
    end_age = 60

    bridge_dict = {}
    bridge_ages = []
    bridge_condition_ratings = []

    for bridge in range(1, population):
        bridge = 'bridge' + ' ' + str(bridge)
        temp_dict = {}
        temp_condition_ratings = []
        temp_ages = []
        temp_year = []

        # Periodic life table computation
        age = random.choice(range(start_age, end_age))
        start_year = random.choice(range(1992, 2023))

        # For the survey years from 1992 to 2023
        for year in range(start_year, end_year):
            rating = generate_condition_rating(age)
            temp_condition_ratings.append(rating)
            temp_ages.append(age)
            temp_year.append(year)
            age = age + 1

        temp_dict['age'] = temp_ages
        temp_dict['year'] = temp_year
        temp_dict['deck'] = temp_condition_ratings
        temp_deck_inter, count = compute_intervention_utility(temp_condition_ratings)
        temp_dict['deck intervention'] = temp_deck_inter
        bridge_dict[bridge] = temp_dict

    return bridge_dict
