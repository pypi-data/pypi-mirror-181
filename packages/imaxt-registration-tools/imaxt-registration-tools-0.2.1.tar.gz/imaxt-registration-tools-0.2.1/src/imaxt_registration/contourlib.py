import math
from functools import wraps

import cv2
import numpy as np
import scipy.ndimage as ndi
from scipy.stats import median_abs_deviation
from skimage.transform import rescale, rotate

from .settings import Settings


def get_contours(mask):
    mask = ((mask > 0) * 255).astype("uint8")
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    max_area = -1
    for i in range(len(contours)):
        area = cv2.contourArea(contours[i])
        if area > max_area:
            cnt = contours[i]
            max_area = area

    return cnt


def mask_coordinates(mask):
    cnt = get_contours(mask)

    x, y, w, h = cv2.boundingRect(cnt)
    return (x, y, w, h)


def crop_mask(mask):
    x, y, w, h = mask_coordinates(mask)
    return mask[y : y + h, x : x + w]


def get_area(img, name):
    mask = create_mask(img, name=name)
    cnt = get_contours(mask)
    return cv2.contourArea(cnt)


def get_scale(im1, im2):
    area1 = get_area(im1, name="1_" + im1.name)
    area2 = get_area(im2, name="2_" + im2.name)
    scale = math.sqrt(area1 / area2)
    return scale


def create_mask_v0(im):
    img = ndi.gaussian_filter(im, (3, 3))
    m = img.flatten()

    z1 = np.median(m[m > 0])
    z2 = median_abs_deviation(m[m > 0])
    mask = img

    mask = mask > z1 + 10 * z2
    img[~mask] = 0
    z = np.percentile(img.ravel(), 50)
    mask = mask > z

    mask = ndi.binary_opening(mask, iterations=3)

    mask = (
        ndi.binary_dilation(mask, iterations=3) * 1
        - ndi.binary_erosion(mask, iterations=3) * 1
    )
    mask = ndi.binary_fill_holes(mask)

    mask = mask * 255

    mask = ndi.gaussian_filter(mask, 3)
    mask = mask / mask.max() * 255

    mask = mask.astype("uint8")

    analysis = cv2.connectedComponentsWithStats(mask, 4, cv2.CV_16U)
    (totalLabels, label_ids, values, centroid) = analysis

    output = np.zeros(img.shape, dtype="uint8")
    area = 0
    for i in range(1, totalLabels):
        if values[i, cv2.CC_STAT_AREA] > area:
            area = values[i, cv2.CC_STAT_AREA]
            componentMask = (label_ids == i).astype("uint8") * 255

    # Creating the Final output mask
    output = cv2.bitwise_or(output, componentMask)

    output = ndi.binary_erosion(output, iterations=3)
    output = ((output > 0) * 255).astype("uint8")

    mask = im * output
    z1 = np.percentile(mask.ravel(), 50)
    mask = (mask > z1) * 255
    return mask.astype("uint8")


def maskcache(f):
    cache = {}

    @wraps(f)
    def wrapper(*args, **kwargs):
        name = kwargs.get("name", None)
        img = args[0]
        if name is None:
            return f(img.values, **kwargs)
        if name not in cache:
            cache[name] = f(img.values, **kwargs)
        # print(name)
        return cache[name]

    return wrapper


@maskcache
def create_mask(
    image,
    name=None,
):

    """Create mask from the scaled image

    Parameters
    ----------
    image
        input image (better to be an scaled image)
    name
        mask id for cache purposes

    Returns
    -------
    output
        Mask image with mask values set to 1 and background values set to 0
    """

    cl_morph_parm = Settings.cl_morph_parm
    c_min_area = Settings.c_min_area
    c_count_max = Settings.c_count_max

    # to avoid compressing all background values around 0, and dealing with
    # zero values for background, we scale data to 25 and and add 1 later
    image = cv2.normalize(image, None, 1, 255, cv2.NORM_MINMAX, -1)

    # apply close morphology to get rid of small structures and make the big blog bolder
    outer = cv2.morphologyEx(
        image,
        cv2.MORPH_CLOSE,
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (cl_morph_parm, cl_morph_parm)),
    )

    # fill/replace zeros with median value to have smoother background
    # then we apply blur filter to remove any artificial casued by filling with median
    outer[outer <= 1] = np.median(outer[outer > 1])
    outer = outer.astype(np.uint8)
    outer = cv2.blur(outer, (5, 5))

    # remove noise by filtering the most frequent element from the image
    ret, th1 = cv2.threshold(
        outer, np.median(outer), 255, cv2.THRESH_BINARY + cv2.THRESH_TRIANGLE
    )

    # binaries the image and fill the holes
    image_fill_holes = ndi.binary_fill_holes(th1).astype(np.uint8)

    cnts, _ = cv2.findContours(
        image_fill_holes, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE
    )

    # create an empty mask image
    mask = np.zeros(image.shape, np.uint8)

    # assuming the min area for tissue is (e.g. 0.01 = 0.1x * 0.1y)
    min_blob_area = c_min_area * image.shape[1] * image.shape[0]
    blob_counter = 0

    # sort contours by area (large to small) and then loop over them and
    # select those with specific characteristics
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
    for cnt in cnts[: np.min([int(c_count_max), len(cnts) - 1])]:
        if cv2.contourArea(cnt) > min_blob_area:
            blob_counter += 1
            cv2.drawContours(mask, [cnt], -1, 255, cv2.FILLED)
            mask = cv2.bitwise_and(image_fill_holes, mask)

    return (mask * 255).astype("uint8")


def get_flip(im_stpt, im_axio):
    mask_stpt = create_mask(im_stpt, name="1_" + im_stpt.name)
    mask_axio = create_mask(im_axio, name="2_" + im_axio.name)

    moments = cv2.moments(mask_stpt)
    hu_stpt = cv2.HuMoments(moments)

    moments = cv2.moments(mask_axio)
    hu_axio = cv2.HuMoments(moments)
    if np.sign(hu_stpt[-1]) == np.sign(hu_axio[-1]):
        return 0

    moments = cv2.moments(mask_axio[::-1, :])
    hu_axio = cv2.HuMoments(moments)
    if np.sign(hu_stpt[-1]) == np.sign(hu_axio[-1]):
        return 1

    moments = cv2.moments(mask_axio[:, ::-1])
    hu_axio = cv2.HuMoments(moments)
    if np.sign(hu_stpt[-1]) == np.sign(hu_axio[-1]):
        return 2


def func_iou(x, img1, img2):
    angle = x[0]
    scale = x[1]
    img2_rot = rotate(img2, angle, resize=True)
    img2_scl = rescale(img2_rot, scale)
    img2_shift = img2_scl
    # img2_shift = shift(img2_scl, (y_offset, x_offset))
    img2 = crop_mask(img2_shift)

    dy = max(img1.shape[0], img2.shape[0])
    dx = max(img1.shape[1], img2.shape[1])
    img1_f = np.pad(
        img1,
        [
            ((dy - img1.shape[0]) // 2, (dy - img1.shape[0]) // 2),
            ((dx - img1.shape[1]) // 2, (dx - img1.shape[1]) // 2),
        ],
    )

    img2_f = np.pad(
        img2,
        [
            ((dy - img2.shape[0]) // 2, (dy - img2.shape[0]) // 2),
            ((dx - img2.shape[1]) // 2, (dx - img2.shape[1]) // 2),
        ],
    )

    dy = min(img1_f.shape[0], img2_f.shape[0])
    dx = min(img1_f.shape[1], img2_f.shape[1])

    c1 = img1_f[:dy, :dx] > 0
    c2 = img2_f[:dy, :dx] > 0
    intersection = c1 * c2
    union = (c1 + c2) > 0
    iou = intersection.sum() / float(union.sum())
    return -np.log(iou)


def func_iou_old(x, *, img1, img2):
    angle = x[0]
    scale = x[1]
    # x_offset = x[2]
    # y_offset = x[3]
    img2_rot = rotate(img2, angle, resize=True)
    img2_scl = rescale(img2_rot, scale)
    # img2_shift = shift(img2_scl, (y_offset, x_offset))
    img2_f = crop_mask(img2_scl)
    dy = min(img1.shape[0], img2_f.shape[0])
    dx = min(img1.shape[1], img2_f.shape[1])
    c1 = img1[:dy, :dx] > 0
    c2 = img2_f[:dy, :dx] > 0
    intersection = c1 * c2
    union = (c1 + c2) > 0
    iou = intersection.sum() / float(union.sum())
    return 1 - iou
