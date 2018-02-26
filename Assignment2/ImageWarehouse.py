from robotcar_deps.camera_model import CameraModel
from robotcar_deps.image import load_image
from robotcar_deps.build_pointcloud import build_pointcloud
from robotcar_deps.transform import build_se3_transform
from datetime import datetime as dt
import numpy as np
import re
import os


class ImageWarehouse:

    def __init__(self, data_dir, deps_dir):
        print("Initializing Image Warehouse")
        self.data_dir = data_dir
        self.models_dir = deps_dir + 'models/'
        self.extrinsics_dir = deps_dir + 'extrinsics/'
        self.time_delta = 1000000
        self.images_dict = {}   # key - 'image path' | value - [[datetime, image, timestamp], camera model]
        self.ptcloud_dict = {}  # key - 'lidar path' | value - [3D point cloud, reflectance]

    def importImages(self, image_path, image_name):
        # Images directory and corresponding timestamps
        images_dir = os.path.join(self.data_dir, image_path)
        timestamps_path = os.path.join(self.data_dir, image_name + '.timestamps')

        # Load camera model
        model = CameraModel(self.models_dir, images_dir)

        # Loading, demosaicing, undistoring images
        images = []
        current_chunk = 0
        timestamps_file = open(timestamps_path)
        for line in timestamps_file:
            tokens = line.split()
            datetime = dt.utcfromtimestamp(int(tokens[0]) / self.time_delta)
            chunk = int(tokens[1])
            filename = os.path.join(images_dir, tokens[0] + '.png')
            if not os.path.isfile(filename):
                if chunk != current_chunk:
                    print("Chunk " + str(chunk) + " not found")
                    current_chunk = chunk
                continue

            current_chunk = chunk
            img = load_image(filename, model)
            images.append([datetime, img, tokens[0]])

        self.images_dict[image_path] = [images, model]
        print("Finished importing " + image_path + " images")

    def build3DPointCloud(self, lidar_path, poses_path):
        # Load timestamps file to obtain start time
        timestamps_path = os.path.join(self.data_dir, lidar_path + '.timestamps')
        lidar_dir = os.path.join(self.data_dir, lidar_path)
        poses_dir = os.path.join(self.data_dir, poses_path)
        with open(timestamps_path) as timestamps_file:
            start_time = int(next(timestamps_file).split(' ')[0])

        end_time = start_time + 2e7

        # Construct the 3D point cloud
        ptcloud, reflectance = build_pointcloud(lidar_dir, poses_dir, self.extrinsics_dir, start_time, end_time)
        self.ptcloud_dict[lidar_path] = [ptcloud, reflectance]
        print("Finished generating " + lidar_path + " 3D point cloud")

    def buildPtCloudOnImage(self, image, model, lidar_path, poses_path):
        timestamps_path = os.path.join(self.data_dir, lidar_path + '.timestamps')
        lidar_dir = os.path.join(self.data_dir, lidar_path)
        poses_dir = os.path.join(self.data_dir, poses_path)
        extrinsics_path = os.path.join(self.extrinsics_dir, model.camera + '.txt')
        with open(extrinsics_path) as extrinsics_file:
            extrinsics = [float(x) for x in next(extrinsics_file).split(' ')]

        G_camera_vehicle = build_se3_transform(extrinsics)
        G_camera_posesource = None

        poses_type = re.search('(vo|ins)\.csv', poses_dir).group(1)
        if poses_type == 'ins':
            with open(os.path.join(self.extrinsics_dir, 'ins.txt')) as extrinsics_file:
                extrinsics = next(extrinsics_file)
                G_camera_posesource = G_camera_vehicle * build_se3_transform([float(x) for x in extrinsics.split(' ')])
        else:
            # VO frame and vehicle frame are the same
            G_camera_posesource = G_camera_vehicle

        # Generate point cloud with respect to timestamp
        # timestamp = 0
        # with open(timestamps_path) as timestamps_file:
        #     for i, line in enumerate(timestamps_file):
        #         if i == args.image_idx:
        #             timestamp = int(line.split(' ')[0])
        timestamp = float(image[2])
        pointcloud, reflectance = build_pointcloud(lidar_dir, poses_dir, self.extrinsics_dir,
                                                   timestamp - 1e7, timestamp + 1e7, timestamp)

        pointcloud = np.dot(G_camera_posesource, pointcloud)
        uv, depth = model.project(pointcloud, image[1].shape)
        return [uv, depth]
