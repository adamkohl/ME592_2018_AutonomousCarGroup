from DataManager import DataManager
from TimeSeriesProcessor import TimeSeriesProcessor

DATA_DIR = "/Users/herbert/Code/ME592X/Assignment_1/data/"
OUTPUT_DIR = "/Users/herbert/Code/ME592X/Assignment_1/output/"


def main():
    # --------------- Problem 2.2 -------------------------------
    print("Starting Assignment 1 Application Execution")
    print("Executing Problem 2.2")

    # Import data
    dataMan = DataManager(DATA_DIR, OUTPUT_DIR)
    dataMan.importEnergyData("energydata_complete.csv")

    # Store and process time-series data
    tseriesProcesser = TimeSeriesProcessor()
    tseriesProcesser.setData(dataMan.energy_data)
    tseriesProcesser.setVariableInfo(dataMan.energy_variables)

    # --------------- Problem 2.2.1 -----------------------------
    print("Executing Problem 2.2.1")
    tseriesProcesser.analyzeEntireTimePeriod()
    tseriesProcesser.analyzeWeek()

    # --------------- Problem 2.2.2 & 2.2.3 ---------------------
    print("Executing Problem 2.2.2 and 2.2.3")
    tseriesProcesser.analyzeEnergyConsumption()

    # --------------- Problem 2.2.4 -----------------------------
    print("Executing Problem 2.2.4")

    # --------------- Problem 2.2.5 -----------------------------
    print("Executing Problem 2.2.5")
    # tseriesProcesser.analyzePressureImpact()

    # --------------- Problem 2.2.6 -----------------------------
    print("Executing Problem 2.2.6")

    # --------------- Problem 2.3 -------------------------------
    print("Executing Problem 2.3")
    # Import data
    dataMan.importAirfoilData("airfoil_self_noise.dat")
    print("stop")


if __name__ == "__main__":
    main()
