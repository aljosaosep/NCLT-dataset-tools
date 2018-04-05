"""
Undistorts all images and stores them in a new dir.
Author: Aljosa Osep (osep@vision.rwth-aachen.de)

To use:

    python undistort_sequences.py /media/osep/NCLT/images /media/osep/NCLT/ladybug3_calib
"""

import numpy as np
import cv2
import matplotlib.pyplot as plt
import argparse
import re
import os
import glob

import undistort as undis


def main():
    parser = argparse.ArgumentParser(description="Undistort images")
    parser.add_argument('image_dir', metavar='img', type=str, help='image dir')
    parser.add_argument('map_dir', metavar='map', type=str, help='undistortion maps dir')
    args = parser.parse_args()

    camera_list = ['Cam%d'%x for x in range(6)]

    # Get all dirs in image dir
    img_dirs_list = os.walk(args.image_dir).next()[1]

    for dir_name in img_dirs_list:
        print ('Processing seq. dir: %s'%dir_name)

        for cam_name in camera_list:
            print ('Processing cam: %s'%cam_name)
            map_path = os.path.join(args.map_dir, 'D2U_%s_1616X1232.txt'%cam_name)
            undistort = undis.Undistort(map_path)
            print 'Loaded camera calibration'
            curr_dir = os.path.join(args.image_dir, dir_name, 'lb3', cam_name)
            img_this_seq_cam_dir = os.path.join(curr_dir, '*.tiff')
            print ('Processing: %s'%img_this_seq_cam_dir)

            # Get all images in the image dir
            all_imgs = glob.glob(img_this_seq_cam_dir)
            all_imgs.sort()
            for file in all_imgs:

                # Call undistort on all images
                im = cv2.imread(file)
                im_undistorted = undistort.undistort(im)

                # Save to %IMG_DIR%/undistorted/*.png
                path_dir, path_name = os.path.split(file)
                name, ext = os.path.splitext(path_name)
                dir_out = os.path.join(path_dir, 'undistored')
                if not os.path.exists(dir_out): # Make sure output dir is there
                    os.makedirs(dir_out)
                path_out = os.path.join(dir_out, '%s.png'%name)
                cv2.imwrite(path_out, im_undistorted)

if __name__ == "__main__":
    main()
