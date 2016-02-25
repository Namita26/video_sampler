from os import listdir, path
from os.path import isfile, join
import codecs
import json
import os


class FileUtil:
    """FileUtil: Utility functions to related to a file"""

    @staticmethod
    def readFile(filename, encoding="utf-8"):
        '''
        Reads a file and returns the text

        :param filename: Filename to be read
        :type filename: string
        :param encoding: default is 'utf-8'
        :type encoding: string
        '''
        with codecs.open(filename, "r", encoding) as f:
            return f.read()

    @staticmethod
    def readJson(filename, encoding="utf-8"):
        """readFile : Reads a JSON file and returns the JSON Object

        :param filename: Filename to be read
        :param encoding: default is 'utf-8'
        """
        with codecs.open(filename, "r", encoding) as f:
            return json.load(f)

    @staticmethod
    def writeFile(filename, data, encoding="utf-8"):
        """writeFile : Writes data to a file

        :param filename: File to be written
        :param data: Data to be written to a file
        :param encoding: default is 'utf-8'
        """
        FileUtil.check_and_create_dir(filename)
        if encoding:
            with codecs.open(filename, 'w', encoding) as outfile:
                outfile.write(data)
        else:
            with open(filename, 'w') as outfile:
                outfile.write(data)

    @staticmethod
    def appendFile(filename, data, encoding="utf-8"):
        """writeFile : Appends data to a file

        :param filename: File to be written
        :param data: Data to be written to a file
        :param encoding: default is 'utf-8'
        """
        FileUtil.check_and_create_dir(filename)
        if encoding:
            with codecs.open(filename, 'a', encoding) as outfile:
                outfile.write(data)
        else:
            with open(filename, 'a') as outfile:
                outfile.write(data)

    @staticmethod
    def writeJson(filename, data, encoding="utf-8"):
        """writeJson : Pretty print a json to a file

        defaults the indent to 4 and sorts the keys

        :param filename: Filename to be written
        :param data: Json to be written to a file.
        :param encoding: default is 'utf-8'
        """
        FileUtil.check_and_create_dir(filename)
        if encoding:
            with codecs.open(filename, 'w', encoding) as outfile:
                json.dump(data, outfile, indent=4, sort_keys=True)
        else:
            with open(filename, 'w') as outfile:
                json.dump(data, outfile, indent=4, sort_keys=True)

    @staticmethod
    def appendJson(filename, data, encoding="utf-8"):
        """writeJson : Pretty print a json to a file

        defaults the indent to 4 and sorts the keys

        :param filename: Filename to be written
        :param data: Json to be written to a file.
        :param encoding: default is 'utf-8'
        """
        FileUtil.check_and_create_dir(filename)
        if encoding:
            with codecs.open(filename, 'a', encoding) as outfile:
                json.dump(data, outfile, indent=4, sort_keys=True)
        else:
            with open(filename, 'a') as outfile:
                json.dump(data, outfile, indent=4, sort_keys=True)

    @staticmethod
    def readFileByLines(filename, encoding="utf-8"):
        """readFileByLines : Returns a list of lines in the file

        :param filename: Filename to be read
        :param encoding: default is 'utf-8'
        """
        with codecs.open(filename, "r", encoding) as f:
            return [line.replace("\n", "") for line in f.readlines()]

    @staticmethod
    def readColumn(filename, column_number=0, delimiter=' ', encoding="utf-8"):
        """readColumn : Reads a particular column in a file and returns a list

        This method reads all the lines in a file, splits it on the delimiter
        and returns the data in particular column

        :param filename: File to be read
        :param column_number: Column Number to be read (default 0)
        :param delimiter: Delimeter (default ' ')
        :param encoding: default is 'utf-8'
        """
        with codecs.open(filename, "r", encoding) as f:
            content = f.readlines()
            result = []
            for line in content:
                split = line.split(delimiter)
                if len(split) > column_number:
                    result.append(split[column_number])
            return result

    @staticmethod
    def get_all_files_in_folder(mypath):
        files = [join(mypath, f) for f in listdir(mypath) if
                 isfile(join(mypath, f))]
        return [filename for filename in files if filename[-1] != "~"]

    @staticmethod
    def is_file(filename):
        return isfile(filename)

    @staticmethod
    def create_dir_if_ne(directory):
        if not os.path.exists(directory):
            os.makedirs(directory)

    @staticmethod
    def check_and_create_dir(filename):
        directory = "/".join(filename.split("/")[:-1])
        FileUtil.create_dir_if_ne(directory)

    @staticmethod
    def get_absolute_path(filename, package_file):
        package_path = path.dirname(package_file)
        if package_path:
            package_path = package_path + "/"
        return package_path + filename
