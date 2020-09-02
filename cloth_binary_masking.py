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
    # binary thresholding by blue ?
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([0, 0, 120])
    upper_blue = np.array([180, 38, 255])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    result = cv2.bitwise_and(image, image, mask=mask)

    # binary threshold by green ?
    b, g, r = cv2.split(result)
    filter = g.copy()
    ret, mask = cv2.threshold(filter, 10, 255, 1)

    return mask


def make_body_mask(data_dir, image_name, save_dir=None):
    print(image_name)

    # define paths
    img_pth = os.path.join(data_dir, image_name)

    mask_path = None
    if save_dir is not None:
        mask_path = os.path.join(save_dir, image_name)

    # Load images
    img = cv2.imread(img_pth)
    # segm = Image.open(seg_pth)
    # the png file should be 1-ch but it is 3 ch ^^;
    print('gray image name', image_name)

    cloth_mask = cloth_detection(img)
    cv2.imwrite(mask_path, cloth_mask )


def main():
    # define paths

    # root_dir = "data/viton_resize"
    root_dir = "storage/data/"
    mask_folder = "image-mask"

    data_mode = "test-end2end"
    # data_mode = "test"
    image_folder = "image"

    image_dir = os.path.join(os.path.join(root_dir, data_mode), image_folder)
    try:
        shutil.rmtree(os.path.join(image_dir, '.ipynb_checkpoints'))
        shutil.rmtree('storage/data/test-end2end/image-parse-new/.ipynb_checkpoints')
    except:
        print("Image directory is clean")
    image_list = os.listdir(image_dir)
    mask_dir = os.path.join(os.path.join(root_dir, data_mode), mask_folder)
    if not os.path.exists(mask_dir):
        os.makedirs(mask_dir)

    for each in image_list:
        make_body_mask(image_dir,  each, mask_dir)


if __name__ == '__main__':
    main()