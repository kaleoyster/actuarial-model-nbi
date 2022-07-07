"""
Description:
    This is a script to run the actuarial model
Author:
    Akshay Kale
Credits:
    This project for first initiated by O'Brien Chin
Date: 29th June, 2022
"""
from collections import defaultdict

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

def main():
    age = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    count = [100, 88, 67, 55, 67, 70, 72, 78, 65, 78]
    hazard, survival = compute_hazard_score(count, age)
    probabilities = compute_probabilities(hazard)
    print(hazard)
    print(probabilities)
    #nbi = create_dummy_data()


if __name__=='__main__':
    main()
