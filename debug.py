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

        self.__debug_tag = datetime.now().strftime('%y%m%d_%H%M%S')
        self.__debug_file = open('./debug/{}_debug-info.md'.format(self.__debug_tag), 'x')

        self.__debug_file.writelines('# Debug Info - {}\n\n'.format(filename))
        self.__debug_file.writelines('Original file: [{0}](../examples/{0})\n'.format(filename))

        debug_filename = '{}_debug-image.jpg)\n'.format(self.__debug_tag)
        self.__debug_file.writelines('Debug output: [{0}](./{0})'.format(debug_filename))

        self.__debug_file.close()

    def get_debug_tag(self):
        '''
        Returns single processing identifier
        '''
        return self.__debug_tag
