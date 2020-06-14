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

    image_paths = args['image']
    preprocess_mode = args['preprocess']
    debug = args['debug']
    language = args['lang']

    for image_path in image_paths:
        processing_result = process_image(image_path, preprocess_mode, language, debug)
        print("==========\nResults:\n")
        print(processing_result)

if __name__ == "__main__":
    main()
