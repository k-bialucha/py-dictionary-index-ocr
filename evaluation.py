'''
Main module for app's performance evaluation.
'''
import pandas as pd
from os import path

from input import parse_arguments
from processing import process_image, OutputFormat


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


def compare(actual_data, reference_data):
    '''
    Performs comparison between actual and reference data.
    '''
    true_positives = empty_df.copy()
    false_negatives = empty_df.copy()
    false_positives = empty_df.copy()

    # check reference data for matches with actual data
    # and false negatives
    for _, row in reference_data.iterrows():
        x_pos = row['left']
        y_pos = row['top']

        query = 'left > {} and left < {} and top > {} and top < {}'.format(
            x_pos-7, x_pos+7, y_pos-12, y_pos+12)
        matching = actual_data.query(query)

        results_count = len(matching.index)

        if results_count == 1:
            true_positives = true_positives.append(row)
        elif results_count == 0:
            false_negatives = false_negatives.append(row)
        else:
            print('WRONG RESULTS COUNT:', results_count)
            raise SystemExit('evaluation/compare: invalid result count')

    # check actual data for matches with reference data
    # and false positives
    for index, row in actual_data.iterrows():
        print(row['text'], row['left'], row['top'])

    print('============\nRESULTS:')
    print(true_positives)
    print(false_negatives)
    print(false_positives)


if __name__ == "__main__":
    evaluate()
