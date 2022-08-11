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



def compute_periodic_life_table(intervention_type, age_intervention, end_age=51):
    """
    Description
        Compute a periodic lifetable
    """
    age_list = []
    list_P_x = []
    list_D_x = []
    list_m_x = []
    list_q_x = []
    list_p_x = []
    list_l_x = []
    list_L_x = []
    list_T_x = []
    list_e_x = []
    initial_population = 100000

    for age in range(1, end_age):
        total_number_bridges = len(age_intervention[age])
        counter_intervention = Counter(age_intervention[age])

        P_x = total_number_bridges
        D_x = counter_intervention[intervention_type]
        m_x = D_x / P_x
        q_x = (D_x / (P_x + (0.5 * D_x)))
        p_x = 1 - q_x
        l_x = initial_population * p_x

        list_P_x.append(P_x)
        list_D_x.append(D_x)
        list_m_x.append(m_x)
        list_q_x.append(q_x)
        list_p_x.append(p_x)
        list_l_x.append(l_x)

        # Append all computed statistics to the list
        age_list.append(age)

    # Calculate L_x
    for i in range(0, (len(list_l_x) - 1)):
        L_x = (list_l_x[i] + list_l_x[i+1]) / 2
        list_L_x.append(L_x)

    # Calculate T_x
    for i in range(0, len(list_L_x)):
        T_x = sum(list_L_x[i:])
        list_T_x.append(T_x)

    # Calculate e_x
    for i in range(0, len(list_T_x)):
        e_x = list_T_x[i] / list_l_x[i]
        list_e_x.append(e_x)

    return age_list, list_P_x, list_D_x, list_m_x, list_q_x, list_p_x, list_L_x, list_T_x, list_e_x


def compute_life_table(data,
                       study_window_years,
                       intervention_type,
                       end_age=51):
    """
    Description:
        computes period life table based on the period
    """
    # Initial population
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

    age_list, P, D, m, q, p, L, T, e = compute_periodic_life_table(intervention_type, age_intervention, end_age=51)


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


