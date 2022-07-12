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

    # select features:
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

    # Select states:
    states = ['31'] # Nebraska

    # years:
    years = [year for year in range(1992, 2020)]

    # Query
    individual_records = query(fields, states, years, collection)
    #individual_records = sample_records()

    # Fixing geo-coordinate by reformating the default values
    individual_records = fix_coordinates(individual_records)
    individual_records = compute_deck_age(individual_records)
    individual_records = compute_age_1(individual_records)
    individual_records = compute_adt_cat(individual_records)
    paved_ind_rec, gravel_ind_rec = filter_gravel_paved(individual_records)

    #individual_records = paved_ind_rec

    # Group records and segmentize
    groupedRecords = group_records(individual_records, fields)
    #groupedRecords = segmentize(groupedRecords)
    #groupedRecords = reorganize_segmented_data(groupedRecords)
    groupedRecords = compute_intervention(groupedRecords,
                                          from_to_matrix_kent)

    groupedRecords = compute_intervention(groupedRecords,
                                          from_to_matrix_kent,
                                          component='substructure')

    groupedRecords = compute_intervention(groupedRecords,
                                          from_to_matrix_kent,
                                          component='superstructure')


    #pp.pprint(groupedRecords)
    individual_records = create_individual_records(groupedRecords)

    # Create a function to identify paved bridges and gravel bridges
    #print(individual_records)

    # Compute baseline difference score:
    groupedRecords, baselineDeck = compute_bds_score(groupedRecords,
                                                     component='deck')

    groupedRecords, baselineSubstructure = compute_bds_score(groupedRecords,
                                                             component='substructure')

    groupedRecords, baselineSuperstructure = compute_bds_score(groupedRecords,
                                                               component='superstructure')
    ### Creating BDS map
    deckBDSMap = create_map(groupedRecords, column='deckBDSScore')
    substructureBDSMap = create_map(groupedRecords, column='substructureBDSScore')
    superstructureBDSMap = create_map(groupedRecords, column='superstructureBDSScore')

    ### Compute slope
    groupedRecords = compute_deterioration_slope(groupedRecords, component='deck')
    #groupedRecords = compute_deterioration_slope(groupedRecords, component='substructure')
    #groupedRecords = compute_deterioration_slope(groupedRecords, component='superstructure')

    ### Creating slope map
    deckSlopeMap = create_map(groupedRecords, column='deckDeteriorationScore')
    #substructSlopeMap = create_map(groupedRecords, column='substructureDeteriorationScore')
    #superstructureSlopeMap = create_map(groupedRecords, column='superstructureDeteriorationScore')

    with open('deck-slope-ne.csv', 'w') as f:
        f.write("StructureNumber, Slope")
        for key in deckSlopeMap.keys():
            f.write("%s, %s\n" % (key, deckSlopeMap[key]))

    # TODO: Integration is the problem
    # Create an individual Record 
    indivudal_records = integrate_ext_dataset_list(deckBDSMap,
                                                  individual_records,
                                                   'deckBDSScore')

    individual_records = integrate_ext_dataset_list(substructureBDSMap,
                                                   individual_records,
                                                   'substructureBDSScore')

    individual_records = integrate_ext_dataset_list(superstructureBDSMap,
                                                   individual_records,
                                                   'superstructureBDSScore')

    individual_records = integrate_ext_dataset_list(deckSlopeMap,
                                                   individual_records,
                                                   'deckDeteriorationScore')

    #individual_records = integrate_ext_dataset_list(substructureSlopeMap,
    #                                               individual_records,
    #                                               'substructureDeteriorationScore')

    #individual_records = integrate_ext_dataset_list(superstructureSlopeMap,
    #                                               individual_records,
    #                                               'superstructureDeteriorationScore')

    ### Save to the file
    csvfile = 'nebraska-1992-2020-deck.csv'
    tocsv_list(individual_records, csvfile)
    create_df(baselineDeck, baselineSubstructure, baselineSuperstructure)

main()
