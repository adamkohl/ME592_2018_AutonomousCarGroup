from DataImporter import DataImporter
import statistics as st
import scipy.stats as scipstat

class DataManager:

    def __init__(self, import_file_path, output_file_path):
        print("Initializing Data Manager")
        self.import_path = import_file_path
        self.output_path = output_file_path
        self.dataImport = DataImporter()

    def computeGeneralStatistics(self, dataDict):
        # Initialize variable and statistic dictionary
        column_data = {}
        stats_dict = {}
        for i in range(len(dataDict.values()[0])):
            column_data[i] = []
            stats_dict[i] = []

        # Sort data by variable type
        for key, value in dataDict.items():
            for i in range(len(value)):
                column_data[i].append(value[i])

        # Stats array contains - [mean, std, median, kurtosis, skewness, range[min, max]]
        var_id = 0
        for key, value in column_data.items():
            stats_dict[0].append(st.mean(value))
            stats_dict[1].append(st.stdev(value))
            stats_dict[2].append(st.median(value))
            stats_dict[3].append(scipstat.kurtosis(value))
            stats_dict[4].append(scipstat.skew(value))
            stats_dict[5].append([min(value), max(value)])
            var_id += 1
        return stats_dict
