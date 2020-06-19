'''
Main module for app's performance evaluation.
'''
from statistics import mean
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
    true_positives = EMPTY_DF.copy()
    true_positives.insert(len(true_positives.columns), 'text_ref', [], True)
    true_positives.insert(len(true_positives.columns), 'sim', [], True)

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
            pass
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
            text_act = row['text']
            text_ref = matching.iloc[0]['text']

            row['text_ref'] = text_ref
            row['sim'] = calculate_word_similarity(text_act, text_ref)

            true_positives = true_positives.append(row)
        elif results_count == 0:
            false_positives = false_positives.append(row)
        else:
            print('WRONG RESULTS COUNT:', results_count)
            raise SystemExit('evaluation/compare: invalid result count')

    return (true_positives, false_negatives, false_positives)


def calculate_levenshtein_distance(word_base, word_comp):
    '''
    Calculate Levenshtein distance between 2 words.
    '''
    size_m = len(word_base)
    size_n = len(word_comp)

    results = [[None for x in range(size_n + 1)]
               for y in range(size_m + 1)]

    for i in range(size_m + 1):
        results[i][0] = i
    for j in range(size_n + 1):
        results[0][j] = j

    for i in list(map((lambda x: x+1), range(size_m))):
        for j in list(map((lambda x: x+1), range(size_n))):
            if word_base[i - 1] == word_comp[j - 1]:
                letter_change_cost = 0
            else:
                letter_change_cost = 1

            deletion_cost = results[i - 1][j] + 1
            insertion_cost = results[i][j - 1] + 1
            replacement_cost = results[i - 1][j - 1] + letter_change_cost

            results[i][j] = min(
                deletion_cost, insertion_cost, replacement_cost)

    return results[size_m][size_n]


def calculate_word_similarity(word_act: str, word_ref: str):
    '''
    Calculate similarity between 2 words.
    '''
    len_act = len(word_act)
    len_ref = len(word_ref)

    distance = calculate_levenshtein_distance(word_act, word_ref)

    similarity = round(1 - distance / len_ref, 3)

    return similarity


def calculate_ranking(true_pos_count: int, false_neg_count: int, false_pos_count: int, similarity_mean: float):
    '''
    Calculates the ranking based on TP/FN/FP count.
    '''
    all_positives_count = true_pos_count + false_neg_count
    adjusted_positives_count = true_pos_count * similarity_mean + false_neg_count

    return (adjusted_positives_count * POS_WEIGHT - false_neg_count * FN_WEIGHT -
            false_pos_count * FP_WEIGHT) / (all_positives_count)


def print_ranking(true_positives, false_negatives, false_positives, title=None):
    '''
    Prints a summary of entered data and calculated ranking.
    '''
    true_pos_count = len(true_positives.index)
    false_neg_count = len(false_negatives.index)
    false_pos_count = len(false_positives.index)

    similarity_mean = mean(true_positives['sim'])

    ranking = calculate_ranking(
        true_pos_count, false_neg_count, false_pos_count, similarity_mean)

    if title is not None:
        print('\n{}'.format(title))

    print('[ TP: {:3} | FN: {:3} | FP: {:3} | ranking: {:6.3f} ]'.format(
        true_pos_count, false_neg_count, false_pos_count, round(ranking, 3)))


def evaluate_page(base_name, debug):
    '''
    Execute an evaluation process per one picture
    '''
    image_path = "./input/{}.png".format(base_name)
    processing_result = pd.read_csv("./results/{}.csv".format(base_name))
    reference_data = pd.read_csv("./reference_data/{}.csv".format(base_name))

    (true_positives, false_negatives, false_positives) = compare(
        processing_result, reference_data)

    if debug:
        image_manipulator = ImageManipulator(image_path)

        for _, row in true_positives.iterrows():
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

    print_ranking(true_positives, false_negatives, false_positives, base_name)

    return (true_positives, false_negatives, false_positives)


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
        (true_positives, false_negatives,
         false_positives) = evaluate_page(name, debug)

        all_true_pos = pd.concat([all_true_pos, true_positives])
        all_false_neg = pd.concat([all_false_neg, false_negatives])
        all_false_pos = pd.concat([all_false_pos, false_positives])

    print_ranking(all_true_pos, all_false_neg, all_false_pos, "TOTAL RESULT")


if __name__ == "__main__":
    evaluate_all()
