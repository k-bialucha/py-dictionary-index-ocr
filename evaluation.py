'''
Main module for app's performance evaluation.
'''
from input import parse_arguments
from processing import process_image, OutputFormat


def evaluate():
    '''
    Execute full recognition process
    '''
    args = parse_arguments()

    image_path = args['image'][0]
    preprocess_mode = args['preprocess']
    debug = args['debug']
    language = args['lang']

    processing_result = process_image(
        image_path, preprocess_mode, language, debug, OutputFormat.data_frame_stripped)

    print("Result:")
    print(processing_result)


if __name__ == "__main__":
    evaluate()
