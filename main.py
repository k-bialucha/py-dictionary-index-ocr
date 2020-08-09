'''
App's main module.
'''
import glob
import itertools

from input import parse_main_arguments
from processing import get_page_index, process_image


def main():
    '''
    Execute full recognition process
    '''
    args = parse_main_arguments()

    names = args['names']
    preprocess_mode = args['preprocess']
    config_name = args['config_name']
    debug = args['debug']
    language = args['lang']

    paths_base = map('./input/{}.png'.format, names)
    paths_globbed = map(glob.glob, paths_base)
    paths = list(itertools.chain.from_iterable(paths_globbed))

    for image_path in paths:
        page_index = get_page_index(image_path)

        processing_result = process_image(
            image_path, preprocess_mode, language, debug, config_name)
        print("==========\nResults p.{}:\n".format(page_index))
        print(processing_result)


if __name__ == "__main__":
    main()
