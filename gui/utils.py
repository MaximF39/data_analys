import os


class PathStringShorter:

    max_directory_name_length: int = 20
    """ Maximum length of a directory name in the path
        filepath = "D:\Python_work\very_long_directory_name\show\me\your\love\love.py"

        "very_long_directory_name" will be shorten by max_directory_name_length value to
        "very_long_direc..\"
    """

    max_filename_length: int = 20
    """ Same behaviour as max_directory_name_length """

    file_name_short_sign: str = "../."
    """ Sign that will be placed before extention of the file """

    def shorten_directory_name(self, dir_name: str) -> str:
        """ Short a dir_name according to  max_directory_name_length """
        if len(dir_name) > self.max_directory_name_length:
            dir_name = dir_name[:self.max_directory_name_length] + "..\\"
        return dir_name

    def shorten_file_name_by_filepath(self, filepath:str) -> str:
        """ Short a filename according to max_directory_name_length """
        filename = self.__get_filename(filepath)
        return self.__short_it(filename)

    def shorten_file_name_by_filename(self, filename:str) -> str:
        """ Short a filename according to max_directory_name_length """
        return self.__short_it(filename)
    
    def __short_it(self, filename:str) -> str:
        if len(filename) > self.max_filename_length:
            ext = filename.split('.')[-1]
            filename = filename[:self.max_filename_length-7] + self.file_name_short_sign + ext
        return filename

    def __get_filename(self, filepath:str) -> str:
        return os.path.split(filepath)[-1]
    
    def splited_filepath(self, path_to_file: str) -> list:
        """ Split the path to the file into directory names  """
        signs = ['\\', '/']
        for sign in signs:
            if path_to_file.count(sign) > 0:
                return path_to_file.split(sign)
