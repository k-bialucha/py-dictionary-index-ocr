'''
App's main module.
'''
from input import parse_arguments
from processing import process_image


def main():
    '''
    Execute full recognition process
    '''
    args = parse_arguments()

    original_image_path = args['image']
    preprocess_mode = args['preprocess']
    language = args['lang']

    processing_result = process_image(original_image_path, preprocess_mode, language)

    print("==========\nResults:\n")
    print(processing_result)

if __name__ == "__main__":
    main()
