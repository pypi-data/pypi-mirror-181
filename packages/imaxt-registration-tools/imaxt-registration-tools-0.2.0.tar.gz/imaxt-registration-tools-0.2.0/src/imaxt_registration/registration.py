import SimpleITK as sitk
from skimage.transform import rotate, rescale
import math
import numpy as np
from typing import Tuple
from scipy.stats import median_abs_deviation
from skimage.exposure import match_histograms

from .contourlib import mask_coordinates, create_mask


class Transformation(dict):

    __slots__ = ["metric", "translation", "matrix", "center", "transform"]

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __repr__(self):  # pragma: nocover
        if self.keys():
            m = max(map(len, list(self.keys()))) + 1
            return "\n".join(
                [k.rjust(m) + ": " + repr(v) for k, v in sorted(self.items())]
            )
        else:
            return self.__class__.__name__ + "()"

    def __dir__(self):
        return list(self.keys())


def _command_iteration(method):
    if method.GetOptimizerIteration() == 0:
        print("Estimated Scales: ", method.GetOptimizerScales())
    print(
        f"{method.GetOptimizerIteration():3} "
        + f"= {method.GetMetricValue():7.5f} "
        + f": {method.GetOptimizerPosition()}"
    )


def get_transformation(img1, img2, angle=0, scale=1, verbose=False):

    theta = angle / 180 * np.pi
    matrix = (
        np.array([math.cos(theta), math.sin(theta), -math.sin(theta), math.cos(theta)])
        / scale
    )

    at = sitk.AffineTransform(
        matrix, (0, 0), (img2.shape[0] // 2 + 0.5, img2.shape[1] / 2 + 0.5)
    )

    fixed = sitk.GetImageFromArray(img1)
    moving = sitk.GetImageFromArray(img2)

    R = sitk.ImageRegistrationMethod()
    R.SetMetricAsCorrelation()
    R.SetOptimizerAsRegularStepGradientDescent(
        learningRate=2.0,
        minStep=1e-4,
        numberOfIterations=1000,
        gradientMagnitudeTolerance=1e-8,
    )
    R.SetOptimizerScalesFromIndexShift()

    tx = sitk.CenteredTransformInitializer(fixed, moving, at)
    R.SetInitialTransform(tx)
    R.SetInterpolator(sitk.sitkLinear)
    if verbose:
        R.AddCommand(sitk.sitkIterationEvent, lambda: _command_iteration(R))

    outTx = R.Execute(fixed, moving)

    data = {
        "metric": R.GetMetricValue(),
        "translation": outTx.GetTranslation(),
        "matrix": outTx.GetMatrix(),
        "center": outTx.GetCenter(),
        "_transform": outTx,
    }

    return Transformation(data)


def get_image_bb(img1, img2, scale=1, angle=0, flip=0):

    mask1 = create_mask(img1, name="1_" + img1.name)
    im1 = mask1 * img1.values / mask1.max()

    mask2 = create_mask(img2, name="2_" + img2.name)
    im2 = mask2 * img2.values / mask2.max()

    im2 = rescale(im2, scale)
    mask2 = rescale(mask2, scale)
    if flip == 1:
        im2 = im2[::-1, :]
        mask2 = mask2[::-1, :]
    elif flip == 2:
        im2 = im2[:, ::-1]
        mask2 = mask2[:, ::-1]

    im2 = rotate(im2, angle, resize=False)
    mask2 = rotate(mask2, angle, resize=False)

    x1, y1, w1, h1 = mask_coordinates(mask1)
    x2, y2, w2, h2 = mask_coordinates(mask2)

    im1 = im1[y1 : y1 + h1, x1 : x1 + w1]
    im2 = im2[y2 : y2 + h2, x2 : x2 + w2]

    dy = dx = 200
    im1 = np.pad(im1, (dy // 2, dx // 2))
    im2 = np.pad(im2, (dy // 2, dx // 2))

    return im1, im2, (x1, y1, h1, w1), (x2, y2, h2, w2)


def get_initial_transform(im_mean1, im_mean2, flip=0, angle=0, scale=1):
    im1, im2, fp1, fp2 = get_image_bb(im_mean1, im_mean2, flip=flip)

    indx = im2.ravel() > 0
    z1, z2 = np.median(im2.ravel()[indx]), median_abs_deviation(im2.ravel()[indx])
    im2 = im2.clip(0, z1 + 10 * z2)

    indx = im1.ravel() > 0
    z1, z2 = np.median(im1.ravel()[indx]), median_abs_deviation(im1.ravel()[indx])
    im1 = im1.clip(0, z1 + 10 * z2)

    im1 = match_histograms(im1, im2)

    t = get_transformation(im1, im2, angle=angle, scale=scale, verbose=False)
    return t, fp1, fp2


def find_rigid_alignment(A: np.ndarray, B: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    2-D or 3-D registration with known correspondences.
    Registration occurs in the zero centered coordinate system, and then
    must be transported back.

    Args:
        A: Array of shape (N,D) -- Reference Point Cloud (target)
        B: Array of shape (N,D) -- Point Cloud to Align (source)

    Returns:
        R: optimal rotation (3,3)
        t: optimal translation (3,)
    """
    num_pts = A.shape[0]
    dim = A.shape[1]

    a_mean = np.median(A, axis=0)
    b_mean = np.median(B, axis=0)

    # Zero-center the point clouds
    A -= a_mean
    B -= b_mean

    N = np.zeros((dim, dim))
    for i in range(num_pts):
        N += A[i].reshape(dim, 1) @ B[i].reshape(1, dim)
    N = A.T @ B

    U, D, V_T = np.linalg.svd(N)
    S = np.eye(dim)
    det = np.linalg.det(U) * np.linalg.det(V_T.T)

    # Check for reflection case
    if not np.isclose(det, 1.0):
        S[dim - 1, dim - 1] = -1

    R = U @ S @ V_T
    t = R @ b_mean.reshape(dim, 1) - a_mean.reshape(dim, 1)
    return R, -t.squeeze()
