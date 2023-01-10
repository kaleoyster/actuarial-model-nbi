"""
Description: A custom script to create a dataset
for actuarial model

Author:
    Akshay Kale

Date:
    July 11 , 2022

TODO:
NOTES:
"""

__author__ = 'Akshay Kale'
__copyright__ = "GPL"
__email__ = "akale@unomaha.edu"

import csv
import pprint
from query import *
from maps import *

pp = pprint.PrettyPrinter(indent=3)

def main():
    """
    Config file
    """
    nbiDB = get_db()
    collection = nbiDB['nbi']

    # Select features
    fields = {
                "_id":0,
                "year":1,
                "structureNumber":1,
                "yearBuilt":1,
                "yearReconstructured":1,
                "averageDailyTraffic":1,
                "avgDailyTruckTraffic":1,
                "deck":1,
                "substructure":1,
                "superstructure":1,
                "owner":1,
                "maintainanceResponsibility":1,
                "designLoad":1,
                "deckWidthOutToOut":1,
                "operatingRating":1,
                "structureLength":1,
                "numberOfSpansInMainUnit":1,
                "scourCriticalBridges":1,
                "yearReconstructed":1,
                "structureType":"$structureTypeMain.typeOfDesignConstruction",
                "material":"$structureTypeMain.kindOfMaterialDesign",
                "structureType":"$structureTypeMain.typeOfDesignConstruction",
                "wearingSurface":"$wearingSurface/ProtectiveSystem.typeOfWearingSurface",
                "coordinates":"$loc.coordinates"
            }

    # Select states
    states = ['31'] # Nebraska

    # Years
    years = [year for year in range(1992, 2021)]

    # Query
    individual_records = query(fields, states, years, collection)

    # Fixing geo-coordinate by reformating the default values
    individual_records = fix_coordinates(individual_records)
    individual_records = compute_deck_age(individual_records)
    individual_records = compute_age_1(individual_records)
    individual_records = compute_adt_cat(individual_records)
    #paved_ind_rec, gravel_ind_rec = filter_gravel_paved(individual_records)
    #individual_records = gravel_ind_rec

    # Group records and segmentize
    groupedRecords = group_records(individual_records, fields)

    groupedRecords = compute_intervention(groupedRecords,
                                          from_to_matrix_kent)

    groupedRecords = compute_intervention(groupedRecords,
                                          from_to_matrix_kent,
                                          component='substructure')

    groupedRecords = compute_intervention(groupedRecords,
                                          from_to_matrix_kent,
                                          component='superstructure')

    json_dictionary = {}
    # TODO: Add attributes - Materials, States
    for record in groupedRecords.values():

        structure_number = record['structureNumber'][0]
        owner = record['owner']
        year = record['year']
        year_built = record['yearBuilt']
        deck =  record['deck']
        age = record['age']
        deck_age = record['deckAge']
        substructure  =  record['substructure']
        superstructure  =  record['superstructure']
        deck_intervention = record['deckIntervention']
        sub_intervention = record['substructureIntervention']
        sup_intervention = record['superstructureIntervention']
        sup_no_intervention = record['superstructureNumberOfInterventions']
        sub_no_intervention = record['substructureNumberOfInterventions']
        deck_no_intervention = record['deckNumberOfInterventions']
        adt_category = record['adtCategory']
        material = record['material']

        values = {
            'year': year,
            'year built': year_built,
            'age': age,
            'deck age': deck_age,
            'deck': deck,
            'substructure': substructure,
            'superstructure': superstructure,
            'deck intervention': deck_intervention,
            'substructure intervention': sub_intervention,
            'superstructure intervention': sup_intervention,
            'superstructure intervention num': sup_no_intervention,
            'substructure intervention num': sub_no_intervention,
            'deck intervention num': deck_no_intervention,
            'adt category': adt_category,
            'owner': owner,
            'material': material,
        }

        json_dictionary[structure_number] = values
    output_file = open("../../data/nebraska_sample.json", "w")
    json.dump(json_dictionary, output_file, indent=3)
    output_file.close()

if __name__ == '__main__':
    main()
