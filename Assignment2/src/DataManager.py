from DataImporter import DataImporter
import statistics as st
import scipy.stats as scipstat
import math

class DataManager:

    def __init__(self, import_file_path, output_file_path):
        print("Initializing Data Manager")
        self.import_path = import_file_path
        self.output_path = output_file_path
        self.dataImport = DataImporter()

        # Variables specific to application
        self.energy_variables = []
        self.energy_data = {}
        self.airfoil_data = {}
        self.airfoil_stats = {}
        self.airfoil_var_names = ['Frequency (Hz)', 'Angle of Attack (degrees)', 'Chord Length (m)', 'Free-stream Velocity (m/s)', 'Suction Side Displacement Thickness (m)']

    def importEnergyData(self, fileName):
        # Import data from file
        file_name = self.import_path + fileName
        raw_data = self.dataImport.readCSVFile(file_name)

        # Sort and convert data
        self.energy_variables = raw_data[1]
        point_id = 1
        for key, value in raw_data.items():
            if key > 1:
                data_point = []
                for i in range(len(value)):
                    if i == 0:
                        # Dates to be stored as string
                        data_point.append(value[i])
                    else:
                        # Variable values to be stored float
                        data_point.append(float(value[i]))

                # Store data point array in dictionary
                self.energy_data[point_id] = data_point
                point_id += 1

    def importAirfoilData(self, fileName):
        # Import data from file
        file_name = self.import_path + fileName
        raw_data = self.dataImport.readDATFile(file_name)

        # Sort and convert data
        point_id = 1
        for key, value in raw_data.items():
            data_point = []
            for point in value:
                # Variable values to be stored float
                data_point.append(float(point))

            # Store data point array in dictionary
            self.airfoil_data[point_id] = data_point
            point_id += 1

        self.airfoil_stats = self.computeGeneralStatistics(self.airfoil_data)

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
        varID = 0
        for key, value in column_data.items():
            stats_dict[0].append(st.mean(value))
            stats_dict[1].append(st.stdev(value))
            stats_dict[2].append(st.median(value))
            stats_dict[3].append(scipstat.kurtosis(value))
            stats_dict[4].append(scipstat.skew(value))
            stats_dict[5].append([min(value), max(value)])
            #
            # print("Variable:\t" + self.airfoil_var_names[varID])
            # print("Mean: \t" + st.mean(value))
            # print("Std: \t" + st.stdev(value))
            # print("Median: \t" +st.median(value))
            # print("Kurtosis: \t" + scipstat.kurtosis(value))
            # print("Skewness: \t" + scipstat.skew(value))
            # print("Range: \t" + min(value) + "," + max(value))
            varID += 1
        return stats_dict
