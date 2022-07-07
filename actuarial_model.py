"""
Description:
    This is a script to run the actuarial model

Author:
    Akshay Kale

Credit:
    O'Brien Chin

Date:  29th June, 2022
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

def compute_hazard_score(count, age):
    """
    Description:
        returns a computed hazard score.
        based on the leave, exposure, and

    Args:
        from_year
        to_year

    Return:
        new_data (list)
    """
    leave = leaves(count, age)
    exposure = exposures(count, age)
    hazard = leave / exposure
    return hazard

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
        The number of bridges in the study at age 𝑥.
    """
    exposures_dict = defaultdict()
    for age, count in zip(list_age, list_count):
        exposures_dict[age] = count
    return exposures_dict

def main():
    age = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    count = [100, 88, 67, 55, 67, 70, 72, 78, 65, 78]
    print(exposures(count, age))
    #nbi = create_dummy_data()
    print("Hello world")


if __name__=='__main__':
    main()
