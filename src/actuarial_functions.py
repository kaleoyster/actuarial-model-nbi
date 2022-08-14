"""
Description:
    This is a script contains actuarial functions

Author:
    Akshay Kale

Credits:
    O'Brien Chin

Date:
    11th August, 2022
"""
import numpy as np
import pandas as pd
from tqdm import tqdm
from collections import defaultdict
from collections import Counter

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

    tempValues, ages = compute_life_table_utility(categoryTemp,
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

    return age_list, list_P_x, list_D_x, list_m_x, list_q_x, list_p_x, list_l_x, list_L_x, list_T_x, list_e_x


def compute_life_table(data,
                       study_window_years,
                       intervention_type,
                       end_age=51):
    """
    Description:
        computes period life table based on the period
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
        for age, intervention in zip(ages, interventions):
            age_intervention[age].append(intervention)

    for counter in range(0, end_age):
        all_ages.append(counter)
        interventions = age_intervention[counter]
        total_number_of_bridges.append(len(interventions))
        intervention_counter = Counter(interventions)
        intervention = intervention_counter[intervention_type]
        number_of_interventions.append(intervention)

    age_list, P, D, m, q, p, l, L, T, e = compute_periodic_life_table(all_ages,
                                                                   total_number_of_bridges,
                                                                   number_of_interventions,
                                                                    end_age=51)
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
    return df

def compute_life_table_utility(categoryTemp, study_window_years, category, intervention):
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
    return tempValues, ages
