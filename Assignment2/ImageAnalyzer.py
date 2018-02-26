from ImageWarehouse import ImageWarehouse
from ImageViewer import ImageViewer

class ImageAnalyzer:

    def __init__(self, data_dir, deps_dir, output_dir):
        print("Constructing Image Analyzer")
        self.warehouse = ImageWarehouse(data_dir, deps_dir)
        self.viewer = ImageViewer(output_dir)

    def undistortImages(self, path, name):
        self.warehouse.importImages(path, name)

    def buildLidarPointCloud(self, path, name):
        self.warehouse.build3DPointCloud(path, name)

    def saveImages(self):
        for key, value in self.warehouse.images_dict.iteritems():
            self.viewer.showImages(key, value[0])

    def saveRawLidarPointClouds(self):
        for key, value in self.warehouse.ptcloud_dict.iteritems():
            self.viewer.plot3DPointCloud(key, value[0], value[1])

    def showPointCloudsOnImages(self, img_key, ptcld_key, poses_path):
        [images, camera_model] = self.warehouse.images_dict[img_key]
        for img in images:
            [uv, depth] = self.warehouse.buildPtCloudOnImage(img, camera_model, ptcld_key, poses_path)
            self.viewer.showPointCloudOnImage(ptcld_key, img_key, img, uv, depth)
