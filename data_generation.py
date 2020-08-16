'''
Module for getting results for multiple parameters
'''
import glob
import itertools
from os import path
import pandas as pd

from evaluation import EMPTY_RESULTS_DF, EMPTY_DATA_DF, evaluate_page, create_results, print_results, add_to_evaluation_summary
from processing import get_page_index, process_image

PREPORCESS = list(['none', 'blur', 'thresh'])
LANGS = list(['frk', 'deu', 'pol', 'frk+deu', 'frk+deu+pol', 'pol+deu+frk'])
METHODS = list([1, 2])
NAMES = list(['p0045', 'p0089', 'p0138', 'p0154',
              'p0289', 'p0394', 'p0513', 'p0515',
              'p0569', 'p0657', 'p0730', 'p0788'])


def generate_data():
    '''
    Execute data generation for multiple parameters
    '''
    paths_base = map('./input/{}.png'.format, NAMES)
    paths_globbed = map(glob.glob, paths_base)
    paths = list(itertools.chain.from_iterable(paths_globbed))

    for preprocess in PREPORCESS:
        for lang in LANGS:
            for method in METHODS:
                config_name = '{}__{}__{}'.format(preprocess, lang, method)

                for image_path in paths:
                    page_index = get_page_index(image_path)

                    base_name = image_path[-9:-4]

                    has_result = path.isfile(
                        './results/{}/{}.csv'.format(config_name, base_name))

                    if has_result:
                        print(
                            '\nresult file for "{}" already exists, skipping...'.format(base_name))
                    else:
                        process_image(image_path, preprocess, lang,
                                      method, False, config_name)

                        print(
                            "==========\nProcessing p.{} done!\n".format(page_index))


def generate_evaluation_data():
    '''
    Execute evaluation data generation for multiple parameters
    '''
    for preprocess in PREPORCESS:
        for lang in LANGS:
            for method in METHODS:
                config_name = '{}__{}__{}'.format(preprocess, lang, method)
                all_true_pos = EMPTY_DATA_DF.copy()
                all_false_neg = EMPTY_DATA_DF.copy()
                all_false_pos = EMPTY_DATA_DF.copy()

                results_df = EMPTY_RESULTS_DF.copy()

                for name in NAMES:
                    (true_positives, false_negatives,
                     false_positives, results) = evaluate_page(name, False, config_name)

                    all_true_pos = pd.concat([all_true_pos, true_positives])
                    all_false_neg = pd.concat([all_false_neg, false_negatives])
                    all_false_pos = pd.concat([all_false_pos, false_positives])

                    results_df.loc[len(results_df.index)] = results

                total_results = create_results(
                    all_true_pos, all_false_neg, all_false_pos, "total")
                results_df.loc[len(results_df.index)] = total_results

                print_results(total_results)
                results_df.to_csv(
                    './results/{}/evaluation.csv'.format(config_name), index=False)

                add_to_evaluation_summary(total_results, config_name)


if __name__ == "__main__":
    generate_data()
    # generate_evaluation_data()
