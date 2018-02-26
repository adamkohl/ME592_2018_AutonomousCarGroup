import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class ImageViewer:

    def __init__(self, output_dir):
        print("Constructing Image Viewer")
        self.output_dir = output_dir

    def showImages(self, name, images):
        # Create folder for images
        img_dir = os.path.join(self.output_dir, 'undistorted_images')
        img_type_dir = os.path.join(img_dir, name)
        if not os.path.exists(img_type_dir):
            os.makedirs(img_type_dir)

        # Plot images
        for img in images:
            fig = plt.imshow(img[1])
            plt.xlabel(img[0])
            plt.title(name)
            plt.xticks([])
            plt.yticks([])
            img_filename = os.path.join(img_type_dir, str(img[2]) + '.png')
            plt.savefig(img_filename)

    def plot3DPointCloud(self, name, pointcloud, reflectance):
        # Create folder for figures
        img_dir = os.path.join(self.output_dir, '3d_point_clouds')
        if not os.path.exists(img_dir):
            os.makedirs(img_dir)

        # Figure name
        img_filename = os.path.join(img_dir, name + '.png')

        if reflectance is not None:
            colours = (reflectance - reflectance.min()) / (reflectance.max() - reflectance.min())
            colours = 1 / (1 + np.exp(-10 * (colours - colours.mean())))
        else:
            colours = 'gray'

        x = np.ravel(pointcloud[0, :])
        y = np.ravel(pointcloud[1, :])
        z = np.ravel(pointcloud[2, :])

        xmin = x.min()
        ymin = y.min()
        zmin = z.min()
        xmax = x.max()
        ymax = y.max()
        zmax = z.max()
        xmid = (xmax + xmin) * 0.5
        ymid = (ymax + ymin) * 0.5
        zmid = (zmax + zmin) * 0.5

        max_range = max(xmax - xmin, ymax - ymin, zmax - zmin)
        x_range = [xmid - 0.5 * max_range, xmid + 0.5 * max_range]
        y_range = [ymid - 0.5 * max_range, ymid + 0.5 * max_range]
        z_range = [zmid - 0.5 * max_range, zmid + 0.5 * max_range]

        # Plot the figure
        fig = plt.figure(figsize=[16,9])
        ax = fig.gca(projection='3d')
        # ax.set_aspect('equal')
        ax.scatter(-y, -x, -z, marker=',', s=1, c=colours, cmap='gray', edgecolors='none')
        ax.set_xlim(-y_range[1], -y_range[0])
        ax.set_ylim(-x_range[1], -x_range[0])
        ax.set_zlim(-z_range[1], -z_range[0])
        plt.savefig(img_filename)

    def showPointCloudOnImage(self, key_ptcld, img_type, image, uv, depth):
        # Create folder for images
        img_dir = os.path.join(self.output_dir, 'ptcloud_img_projections')
        img_type_dir = os.path.join(img_dir, img_type)
        img_type_ptcld_dir = os.path.join(img_type_dir, key_ptcld)
        if not os.path.exists(img_type_ptcld_dir):
            os.makedirs(img_type_ptcld_dir)

        # Plot the figure
        fig = plt.imshow(image[1])
        plt.scatter(np.ravel(uv[0, :]), np.ravel(uv[1, :]), s=2, c=depth, edgecolors='none', cmap='jet')
        plt.xlim(0, image[1].shape[1])
        plt.ylim(image[1].shape[0], 0)
        plt.xticks([])
        plt.yticks([])

        # Figure name
        img_filename = os.path.join(img_type_ptcld_dir, str(image[2]) + '.png')
        plt.savefig(img_filename)