from ImageAnalyzer import ImageAnalyzer

DATA_DIR = '/Users/herbert/Code/ME592X/Group_REPO/data/Oxford_RobotCar/'
DEPS_DIR = '/Users/herbert/Code/ME592X/Dependencies/robotcar-dataset-sdk-2.1/'
OUTPUT_DIR = '/Users/herbert/Code/ME592X/Group_REPO/output/Assignment2/'

def main():
    print("***** Assignment 2 Initiated")
    analyzer = ImageAnalyzer(DATA_DIR, DEPS_DIR, OUTPUT_DIR)

    # ------------------------------------------------------------------------------------------------------------------
    # ---------------------------  SET PATH AND NAMES FOR ALL IMAGE TYPES
    # ------------------------------------------------------------------------------------------------------------------
    print("***** Importing and Undistorting/Demoscaicing Raw Images")
    image_names = []
    image_names.append(['mono_left', 'mono_left'])
    # image_names.append(['mono_rear', 'mono_rear'])
    # image_names.append(['mono_right', 'mono_right'])
    # image_names.append(['stereo/centre', 'stereo'])
    # image_names.append(['stereo/left', 'stereo'])
    # image_names.append(['stereo/right', 'stereo'])
    for name in image_names:
        analyzer.undistortImages(name[0], name[1])

    # ------------------------------------------------------------------------------------------------------------------
    # --------------------------- SAVE IMAGES
    # ------------------------------------------------------------------------------------------------------------------
    print("***** Saving Undistorted/Demoscaiced Images")
    # analyzer.saveImages()

    # ------------------------------------------------------------------------------------------------------------------
    # --------------------------- GENERATE 3D POINT CLOUDS FOR ENTIRE TIME PERIOD
    # ------------------------------------------------------------------------------------------------------------------
    print("***** Generating 3D Point Cloud")
    ptcloud_names = []
    ptcloud_names.append(['lms_front', 'gps/ins.csv'])
    ptcloud_names.append(['lms_rear', 'gps/ins.csv'])
    ptcloud_names.append(['ldmrs', 'gps/ins.csv'])
    # for name in ptcloud_names:
    #     analyzer.buildLidarPointCloud(name[0], name[1])

    # ------------------------------------------------------------------------------------------------------------------
    # ---------------------------  SAVE 3D POINT CLOUDS
    # ------------------------------------------------------------------------------------------------------------------
    print("***** Saving 3D Point Clouds")
    analyzer.saveRawLidarPointClouds()

    # ------------------------------------------------------------------------------------------------------------------
    # ---------------------------  PROJECT POINT CLOUDS ONTO IMAGES AND SAVE FIGURE
    # ------------------------------------------------------------------------------------------------------------------
    print("***** Projecting Point Clouds On Images")
    for cloud_type in ptcloud_names:
        for img_type in image_names:
            analyzer.showPointCloudsOnImages(img_type[0], cloud_type[0], cloud_type[1])

    print("***** Assignment 2 Complete")

if __name__ == "__main__":
    main()
