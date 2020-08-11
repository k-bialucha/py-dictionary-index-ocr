'''
Module for getting results for multiple parameters
'''
import glob
import itertools

from processing import get_page_index, process_image

PREPORCESS = list(['none', 'blur', 'thresh'])
LANGS = list(['frk', 'deu', 'pol', 'frk+deu', 'frk+deu+pol', 'pol+deu+frk'])
METHODS = list([1, 2])
NAMES = list(['p0045', 'p0089', 'p0138', 'p0154', 'p0289', 'p0513', 'p0515'])


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

                    process_image(image_path, preprocess, lang,
                                  method, False, config_name)

                    print("==========\nProcessing p.{} done!\n".format(page_index))


if __name__ == "__main__":
    generate_data()
