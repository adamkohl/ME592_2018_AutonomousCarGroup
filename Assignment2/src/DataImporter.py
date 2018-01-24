import csv

class DataImporter:

    def __init__(self):
        print("Constructing Data Importer")

    @staticmethod
    def readCSVFile(filePath):
        # Open CSV File
        input_file = open(filePath)
        input_reader = csv.reader(input_file)

        # Initialize data dictionary
        data_dict = {}

        # Read file
        line_num = 1
        input_file.seek(0)
        for row in input_reader:
            # Store row in dictionary
            data_dict[line_num] = row
            line_num += 1

        input_file.close()
        return data_dict

    @staticmethod
    def readDATFile(filePath):
        input_file = open(filePath)
        input_reader = input_file.readlines()

        # Initialize data dictionary
        data_dict = {}

        # Read file
        line_num = 1
        for line in input_reader:
            data_dict[line_num] = line.rstrip().split("\t")
            line_num += 1

        input_file.close()
        return data_dict
