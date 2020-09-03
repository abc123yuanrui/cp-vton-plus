import os
import numpy as np
import cv2
from PIL import Image
import sys


(cv_major, _, _) = cv2.__version__.split(".")
if cv_major != '4' and cv_major != '3':
    print('doesnot support opencv version')
    sys.exit()


# @TODO this is too simple and pixel based algorithm
def cloth_detection(image):
#     # binary thresholding by blue ?
#     hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
#     lower_blue = np.array([0, 0, 120])
#     upper_blue = np.array([180, 38, 255])
#     mask = cv2.inRange(hsv, lower_blue, upper_blue)
#     result = cv2.bitwise_and(image, image, mask=mask)

#     # binary threshold by green ?
#     b, g, r = cv2.split(result)
#     filter = g.copy()
#     ret, mask = cv2.threshold(filter, 10, 255, 1)
    
    
    lower_color_bounds = np.array([50, 50, 248])
    upper_color_bounds = np.array([255, 255, 255])
    mask = cv2.inRange(image,lower_color_bounds,upper_color_bounds )
    mask_inv = cv2.bitwise_not(mask)
    return mask_inv


def make_cloth_mask(data_dir, image_name, save_dir=None):
    print(image_name)

    # define paths
    img_pth = os.path.join(data_dir, image_name)

    mask_path = None
    if save_dir is not None:
        mask_path = os.path.join(save_dir, image_name)
    if os.path.isfile(img_pth):
        # Load images
        img = cv2.imread(img_pth)
        # segm = Image.open(seg_pth)
        # the png file should be 1-ch but it is 3 ch ^^;

        cloth_mask = cloth_detection(img)
        cv2.imwrite(mask_path, cloth_mask )


def main():
    # define paths

    # root_dir = "data/viton_resize"
    root_dir = "storage/data/"
    mask_folder = "cloth-mask"

    data_mode = "train-opt"
    # data_mode = "test"
    image_folder = "cloth"

    image_dir = os.path.join(os.path.join(root_dir, data_mode), image_folder)
    try:
        shutil.rmtree(os.path.join(image_dir, '.ipynb_checkpoints'))
        shutil.rmtree('storage/data/train-opt/image-parse-new/.ipynb_checkpoints')
    except:
        print("Image directory is clean")
    image_list = os.listdir(image_dir)
    mask_dir = os.path.join(os.path.join(root_dir, data_mode), mask_folder)
    if not os.path.exists(mask_dir):
        os.makedirs(mask_dir)

    for each in image_list:
        make_cloth_mask(image_dir,  each, mask_dir)


if __name__ == '__main__':
    main()
