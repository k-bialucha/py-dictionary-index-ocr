'''
App's main module.
'''
from input import parse_main_arguments
from processing import process_image


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

    paths = map('./input/{}.png'.format, names)

    for image_path in paths:
        processing_result = process_image(image_path, preprocess_mode, language, debug, config_name)
        print("==========\nResults:\n")
        print(processing_result)

if __name__ == "__main__":
    main()
