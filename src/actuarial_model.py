"""
Description:
    This is a script to run the actuarial model

Author:
    Akshay Kale

Credits:
    This project for first initiated by O'Brien Chin

Notes:
    1. Exposures is the same as count_dictionary
    compute counts can be renamed as exposures.

    2. Adjust the study windows to mimic bridges born during the same year.
        - Done

    3. Re-create the life table.
        - Some of the bridges  appear in the later time but do not appear in the earlier timeline.
        - Look for bridges that do not appear at all in the later time line.

Date: 29th June, 2022
"""

from collections import defaultdict
from collections import Counter
import json

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
    filtered_data = defaultdict()
    for key, value in data.items():
        if value[column][-1] == val:
            filtered_data[key] = value
    return filtered_data

def main():
    path = '../data/nebraska.json'
    data = read_json(path)

    # TODO: filter data, get bridges built only 1992
    study_window = (1992, 1998)
    data = filter_data(data, 'year built', 1992)

    #bridge_records = defaultdict(list)
    #for bridge, record in data.items():
    #    survey_year = record['year']
    #    count_obj = Counter(survey_year)
    #    for year, value in count_obj.items():
    #        if bridge_counter.get(year) is None:
    #            bridge_counter[year] = value
    #        else:
    #            bridge_counter[year] = bridge_counter[year] + value
    #print(len(data))
    #print(bridge_counter)

    bridge_last_year = defaultdict()
    for bridge, record in data.items():
        last_year = record['year'][-1]
        if bridge_last_year.get(last_year) is None:
            bridge_last_year[last_year] = 1
        else:
            bridge_last_year[last_year] = bridge_last_year[last_year] + 1
    print(bridge_last_year)

## TODO: Create this life table
## Note: length of the list for each bridge can be decided by repair criteria
    ## 1992  33  0
    ## 1993  33  0
    ## 1994  33  0
    ## 1995  33  0.1818
    ## 1996  27  0.037
    ## 1997  26  0.038
    ## 1998  25  0.04
    ## 1999  25  0
    ## 2000  25  0
    ## 2001  25  0.086
    ## 2002  23  0
    ## 2003  23  0
    ## 2004  23  0
    ## 2005  23  0
    ## 2006  23  0
    ## 2007  23  0
    ## 2008  23  0
    ## 2009  23  0
    ## 2010  23  0
    ## 2011  23  0
    ## 2012  23  0
    ## 2013  23  0
    ## 2014  23  0
    ## 2015  23  0
    ## 2016  23  0
    ## 2017  23  0
    ## 2018  21  0.0952 
    ## 2018  0   1


    #count_dictionary = compute_counts(data)
    #ages = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    #counts = age_counter(ages, count_dictionary)
    #hazard, survival = compute_hazard_score(counts, ages)
    #probabilities = compute_probabilities(hazard)




if __name__=='__main__':
    main()
