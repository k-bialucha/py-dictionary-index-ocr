'''
Module for managing debug output.
'''
from datetime import datetime
from pathlib import Path

class DebugHandler:
    '''
    Handles outputting debug data to a file
    '''
    __debug_tag = None
    __debug_file = None

    def __init__(self, filename):
        Path("./debug").mkdir(parents=True, exist_ok=True)

        filename_no_ext = filename.split('.')[0]

        self.__debug_tag = datetime.now().strftime('%y%m%d_%H%M%S') + '_' + filename_no_ext
        self.__debug_file = open('./debug/{}_debug-info.md'.format(self.__debug_tag), 'x')

        self.__debug_file.writelines('# Debug Info - {}\n\n'.format(filename))
        self.__debug_file.writelines('Original file: [{0}](../examples/{0})\n'.format(filename))

        debug_filename = '{}_debug-image.jpg'.format(self.__debug_tag)
        self.__debug_file.writelines('Debug output: [{0}](./{0})\n'.format(debug_filename))

        all_words_filename = '{}_all-words.csv'.format(self.__debug_tag)
        self.__debug_file.writelines('All words output: [{0}](./{0})\n'.format(all_words_filename))

        words_filename = '{}_words.csv'.format(self.__debug_tag)
        self.__debug_file.writelines(
            'Dictionary words output: [{0}](./{0})\n'.format(words_filename))

        self.__debug_file.close()

    def get_debug_tag(self):
        '''
        Returns single processing identifier
        '''
        return self.__debug_tag

    def export_df_to_csv(self, data_frame, name):
        '''
        Exports DataFrame to CSV with current debug tag
        '''
        data_frame.to_csv('./debug/{}_{}.csv'.format(self.__debug_tag, name))
