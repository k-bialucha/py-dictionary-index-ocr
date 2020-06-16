'''
Main module for app's performance evaluation.
'''
import pandas as pd

from imaging import ImageManipulator
from input import parse_evaluation_arguments

POS_WEIGHT = 100
FN_WEIGHT = 100
FP_WEIGHT = 60

# define tolerance for matches [pixels]
X_TOL = 15
Y_TOL = 25

MATCH_QUERY = 'left > {} and left < {} and top > {} and top < {}'

EMPTY_DF = pd.DataFrame(
    columns=['left', 'top', 'width', 'height', 'conf', 'text'])


def compare(actual_data, reference_data):
    '''
    Performs comparison between actual and reference data.
    '''
    true_positives_act = EMPTY_DF.copy()
    true_positives_ref = EMPTY_DF.copy()
    false_negatives = EMPTY_DF.copy()
    false_positives = EMPTY_DF.copy()

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

    return (true_positives_act, true_positives_ref, false_negatives, false_positives)


def calculate_ranking(true_pos_count, false_neg_count, false_pos_count):
    '''
    Calculates the ranking based on TP/FN/FP count.
    '''
    all_positives_count = true_pos_count + false_neg_count

    return (all_positives_count * POS_WEIGHT - false_neg_count * FN_WEIGHT -
            false_pos_count * FP_WEIGHT) / (all_positives_count)


def print_ranking(true_positives, false_negatives, false_positives):
    '''
    Prints a summary of entered data and calculated ranking.
    '''
    true_pos_count = len(true_positives.index)
    false_neg_count = len(false_negatives.index)
    false_pos_count = len(false_positives.index)

    ranking = calculate_ranking(
        true_pos_count, false_neg_count, false_pos_count)

    print('[TP: {}, FN: {}, FP: {}, ranking: {}]'.format(
        true_pos_count, false_neg_count, false_pos_count, round(ranking, 3)))


def evaluate_page(base_name, debug):
    '''
    Execute an evaluation process per one picture
    '''
    image_path = "./input/{}.png".format(base_name)
    processing_result = pd.read_csv("./results/{}.csv".format(base_name))
    reference_data = pd.read_csv("./reference_data/{}.csv".format(base_name))

    (true_positives_act, true_positives_ref, false_negatives,
     false_positives) = compare(processing_result, reference_data)

    if debug:
        image_manipulator = ImageManipulator(image_path)

        for _, row in true_positives_act.iterrows():
            print('Marking TP:', row['text'])
            image_manipulator.mark_word(row, line_color=(50, 180, 50))

        for _, row in false_negatives.iterrows():
            print('Marking FN:', row['text'])
            image_manipulator.mark_word(row, line_color=(180, 50, 50))

        for _, row in false_positives.iterrows():
            print('Marking FP:', row['text'])
            image_manipulator.mark_word(row, line_color=(50, 50, 180))

        # show image
        # TODO: save image
        image_manipulator.show(show_marked=True)

    print_ranking(true_positives_act, false_negatives, false_positives)

    return (true_positives_act, true_positives_ref, false_negatives, false_positives)


def evaluate_all():
    '''
    Run evaluation process for all specified file.
    '''
    args = parse_evaluation_arguments()

    names = args['names']
    debug = args['debug']

    all_true_pos = EMPTY_DF.copy()
    all_false_neg = EMPTY_DF.copy()
    all_false_pos = EMPTY_DF.copy()

    for name in names:
        (true_positives_act, _, false_negatives,
         false_positives) = evaluate_page(name, debug)

        all_true_pos = pd.concat([all_true_pos, true_positives_act])
        all_false_neg = pd.concat([all_false_neg, false_negatives])
        all_false_pos = pd.concat([all_false_pos, false_positives])

    print_ranking(all_true_pos, all_false_neg, all_false_pos)


if __name__ == "__main__":
    evaluate_all()
