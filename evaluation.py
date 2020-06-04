'''
Main module for app's performance evaluation.
'''
import pandas as pd
from os import path

from input import parse_arguments


def evaluate():
    '''
    Execute full recognition process
    '''
    args = parse_arguments()

    image_path = args['image'][0]

    base_name = path.basename(image_path).split('.')[0]

    processing_result = pd.read_csv("./results/{}.csv".format(base_name))
    reference_data = pd.read_csv("./reference_data/{}.csv".format(base_name))

    compare(processing_result, reference_data)


empty_df = pd.DataFrame(
    columns=['left', 'top', 'width', 'height', 'conf', 'text'])

# define tolerance for matches [pixels]
X_TOL = 7
Y_TOL = 12

MATCH_QUERY = 'left > {} and left < {} and top > {} and top < {}'


def compare(actual_data, reference_data):
    '''
    Performs comparison between actual and reference data.
    '''
    true_positives_act = empty_df.copy()
    true_positives_ref = empty_df.copy()
    false_negatives = empty_df.copy()
    false_positives = empty_df.copy()

    # check reference data for matches with actual data
    # and false negatives
    for _, row in reference_data.iterrows():
        x_pos = row['left']
        y_pos = row['top']

        query = MATCH_QUERY.format(
            x_pos-X_TOL, x_pos+X_TOL, y_pos-Y_TOL, y_pos+Y_TOL)
        matching = actual_data.query(query)

        results_count = len(matching.index)

        if results_count == 1:
            true_positives_ref = true_positives_ref.append(row)
        elif results_count == 0:
            false_negatives = false_negatives.append(row)
        else:
            print('WRONG RESULTS COUNT:', results_count)
            raise SystemExit('evaluation/compare: invalid result count')

    # check actual data for matches with reference data
    # and false positives
    for _, row in actual_data.iterrows():
        x_pos = row['left']
        y_pos = row['top']

        query = MATCH_QUERY.format(
            x_pos-X_TOL, x_pos+X_TOL, y_pos-Y_TOL, y_pos+Y_TOL)
        matching = reference_data.query(query)

        results_count = len(matching.index)

        if results_count == 1:
            true_positives_act = true_positives_act.append(row)
        elif results_count == 0:
            false_positives = false_positives.append(row)
        else:
            print('WRONG RESULTS COUNT:', results_count)
            raise SystemExit('evaluation/compare: invalid result count')

    print('============\nRESULTS:')
    print(true_positives_ref)
    print(true_positives_act)
    print(false_negatives)
    print(false_positives)


if __name__ == "__main__":
    evaluate()
