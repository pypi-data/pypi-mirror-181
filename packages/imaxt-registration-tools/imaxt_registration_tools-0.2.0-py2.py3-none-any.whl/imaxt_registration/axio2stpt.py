import os
import time
import traceback
from functools import partial, wraps
from multiprocessing import Pool

import cv2
import msgpack
import msgpack_numpy as mn
import numpy as np
import pandas as pd
import scipy.ndimage as ndi
import SimpleITK as sitk
import xarray as xr
from scipy import optimize
from scipy.stats import median_abs_deviation
from skimage.transform import rescale

from .contourlib import (
    create_mask,
    crop_mask,
    func_iou,
    get_contours,
    get_flip,
    get_scale,
)
from .plotting import NBPlot
from .registration import find_rigid_alignment, get_image_bb, get_initial_transform
from .terminal import debug, error, info, warn, set_verbose

os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["VECLIB_MAXIMUM_THREADS"] = "1"


def stats(im2, im1):
    """Compare two images using Hu moments and return statistic

    Parameters
    ----------
    im1, im2 : np.ndarray
       input images

    Returns
    -------
    comparison statistic (the smaller the more similar the images are)
    """

    mask1 = create_mask(im1, name="1_" + im1.name)
    cnt1 = get_contours(mask1)

    mask2 = create_mask(im2, name="2_" + im2.name)
    cnt2 = get_contours(mask2)

    ret = cv2.matchShapes(cnt1, cnt2, 1, 0.0)
    return ret


def match_image(ref_image, images):
    """Compute best matching image to a reference image

    Parameters
    ----------
    ref_image : np.ndarray
        Reference image
    images : list of np.ndarray or dask arrays
        List of images to compare to

    Returns
    -------
    index of most similar image in the input list
    """

    match = {}
    for j, img in enumerate(images):
        ret = stats(ref_image, img)
        match[j] = ret

    return match


def fit_angle_scale(im1, im2, scale=1, flip=0, use_gradients=False):
    mask1 = create_mask(im1, name="1_" + im1.name)
    mask2 = create_mask(im2, name="2_" + im2.name)

    if flip == 1:
        mask2 = mask2[::-1, :]
    elif flip == 2:
        mask2 = mask2[:, ::-1]

    mask2 = rescale(mask2, scale)

    mask1 = crop_mask(mask1)
    mask2 = crop_mask(mask2)

    if use_gradients:
        guess1 = angle_from_gradients(mask1, mask2)
        guess2 = guess1 + 180
        guess2 = guess2 - 360 * (guess2 > 360)
        out = []
        for angle in [guess1, guess2]:
            x = np.array([angle, 1])
            lsq = optimize.least_squares(
                func_iou,
                x,
                args=(mask2, mask1),
                diff_step=[1, 0.005],
                bounds=[(angle - 20, 0.96), (angle + 20, 1.04)],
            )
            out.append(lsq)
    else:
        out = []
        for angle in range(-140, 180, 40):
            x = np.array([angle, 1])
            lsq = optimize.least_squares(
                func_iou,
                x,
                args=(mask2, mask1),
                diff_step=[1, 0.005],
                bounds=[(angle - 40, 0.96), (angle + 40, 1.04)],
            )
            out.append(lsq)

    j = np.argmin([o.fun for o in out])
    angle = out[j].x[0]
    scale = scale * out[j].x[1]
    cost = out[j].cost
    return angle, scale, cost


def angle_from_gradients(mask1, mask2):
    def _corr(i, h, h2):
        return sum(h * np.roll(h2, i))

    # TODO: use ndi.distance_transform_edt ?
    t1 = ndi.distance_transform_bf(mask1)
    t2 = ndi.distance_transform_bf(mask2)

    t1 = t1.astype("float32")
    gx = cv2.Sobel(t1, cv2.CV_32F, 1, 0, ksize=-1)
    gy = cv2.Sobel(t1, cv2.CV_32F, 0, 1, ksize=-1)
    mag, angle1 = cv2.cartToPolar(gx, gy, angleInDegrees=True)
    angle1 = angle1.flatten()

    t2 = t2.astype("float32")
    gx = cv2.Sobel(t2, cv2.CV_32F, 1, 0, ksize=-1)
    gy = cv2.Sobel(t2, cv2.CV_32F, 0, 1, ksize=-1)
    mag, angle2 = cv2.cartToPolar(gx, gy, angleInDegrees=True)
    angle2 = angle2.flatten()

    h1, _ = np.histogram(angle1[angle1 > 0], bins=np.arange(0, 360))
    h2, _ = np.histogram(angle2[angle2 > 0], bins=np.arange(0, 360))

    # TODO: There must be a one liner for correlation of two vectors...
    c = np.array([_corr(i, h1, h2) for i in range(0, 359)])
    return np.argmax(c)


def safe(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        watch = time.monotonic()
        try:
            return f(*args, **kwargs)
        except Exception:
            error("ERROR:", traceback.format_exc())
        finally:
            debug("Elapsed", time.monotonic() - watch)

    return wrapper


"""

def func1(axio_entry_0, all_stpt_flip_0):
    -> list[(id, prob), (id, prob)]

def func2(axio_slice, stpt):
    for each id in axio_slice:
        func1(id, all_stpt)
    -> get the best

"""


@safe
def axio2stpt_firstpass(stpt_path, axio_path, section_axio, level="l.16", pl=None):

    ds_stpt = xr.open_zarr(f"{stpt_path}/mos", group=level)
    ds_axio = xr.open_zarr(f"{axio_path}/mos", group=level)

    # Prepare the data
    im_axio = ds_axio[section_axio].sel(z=0)
    im_mean_axio = im_axio.mean("channel")
    im_median_axio = im_axio.median("channel")
    if im_mean_axio.values.max() == 0:
        return

    images_stpt = [ds_stpt[s].sel(z=0).mean("channel") for s in list(ds_stpt)]

    # Get best match based on moments
    info("Get closest image based on moments", section_axio)
    match_st = match_image(im_median_axio, images_stpt)
    st_sorted = sorted(match_st.items(), key=lambda x: x[1])
    best_j = st_sorted[0][0]
    info("Best match", list(ds_stpt)[best_j])
    n_best = min(20, len(st_sorted) // 4)
    st_selected = [s[0] for s in st_sorted[:n_best]]

    """
        if method==1:
            # 1. load the fsb from stpt_path and axio_path
            # 2. for each axio and z

            # best_stpt gives
            top_n_stpt_list = func2(axio, stpt)
            # axio: S001 is stpt: S023

            for top_n_stpt_list:
                scale, etc. = func3_affine_transform()
                best_stpt
                fixed_axio = func4_transform(axio_im, stpt_im)

        elif method==2:
    """

    # Compute initial scale
    info("Compute initial scale", section_axio)
    section_stpt = list(ds_stpt)[best_j]
    im_stpt = ds_stpt[section_stpt].sel(z=0)
    im_mean_stpt = im_stpt.mean("channel")
    # im_mean_axio = im_mean_axio.compute()
    scale = get_scale(im_mean_stpt, im_mean_axio)

    # See if images are flipped
    info("Check if image is flipped", section_axio)
    flip = get_flip(im_mean_stpt, im_mean_axio)

    # Compute angle and improved scale
    info("Compute initial angle", section_axio)

    angle, scale, cost = fit_angle_scale(
        im_mean_stpt, im_mean_axio, scale=scale, flip=flip, use_gradients=False
    )

    debug(
        f"Initial transformation - angle: {angle:.2f}, scale: {scale:.2f}, flip: {flip:d}"
    )

    # Get initial transformation
    info("Compute initial transformation", section_axio)
    tx, fp1, fp2 = get_initial_transform(
        im_mean_stpt, im_mean_axio, angle=angle, scale=scale, flip=flip
    )

    info("Bead analysis", section_axio)
    cat_axio = pd.read_parquet(f"{axio_path}/bead/{section_axio}.parquet")
    x, y = cat_axio["x"] / 16, cat_axio["y"] / 16
    if flip == 1:
        y = len(ds_axio[section_axio].y) - y
    elif flip == 2:
        x = len(ds_axio[section_axio].x) - x
    x, y = x - fp2[0] + 100, y - fp2[1] + 100

    inv = tx._transform.GetInverse()
    c2 = np.array([inv.TransformPoint((xi, yi)) for xi, yi in zip(x, y)])

    nbeads = 0
    best_j2 = 0
    dbeads = {}
    for j in st_selected:
        if (j < 0) or (j > len(list(ds_stpt))):
            continue
        try:
            this = list(ds_stpt)[j]
        except Exception:
            continue

        cat_stpt = pd.read_parquet(f"{stpt_path}/bead/{this}.parquet")
        x, y = cat_stpt["x"] / 16, cat_stpt["y"] / 16
        x, y = x - fp1[0] + 100, y - fp1[1] + 100
        c1 = np.array([x, y]).T

        mc1 = c1.copy()

        if np.any(np.isnan(c1)):
            warn("Catalogue contains NaN values", this)

        for i in range(300):
            tc1 = []
            tc2 = []

            for c in mc1:
                res = np.sqrt((np.sum((c2 - c) ** 2, axis=1)))
                k = np.argmin(res)
                if res[k] < 200 / 16.0:
                    tc2.append(c2[k])
                    tc1.append(c)

            tc1 = np.array(tc1)
            tc2 = np.array(tc2)
            if len(tc1) < 10:
                break
            R, T = find_rigid_alignment(tc2, tc1)
            mc1 = np.array([R @ c + T for c in mc1])

        this_beads = len(tc1)
        if this_beads > nbeads:
            nbeads = this_beads
            best_j2 = j
        dbeads[this] = this_beads
        debug("Detected common beads", this, this_beads)

    info("Compute final transformation", section_axio)
    best_j = best_j2
    section_stpt = list(ds_stpt)[best_j]
    info("Best final match", section_stpt)
    im_stpt = ds_stpt[section_stpt].sel(z=0)
    im_mean_stpt = im_stpt.mean("channel")
    tx, fp1, fp2 = get_initial_transform(
        im_mean_stpt, im_mean_axio, angle=angle, scale=scale, flip=flip
    )

    if pl is not None:
        info("Plotting", section_axio)
        im1, im2, fp1, fp2 = get_image_bb(im_mean_stpt, im_mean_axio, flip=flip)

        indx = im2.ravel() > 0
        z1, z2 = np.median(im2.ravel()[indx]), median_abs_deviation(im2.ravel()[indx])
        im2 = im2.clip(0, z1 + 5 * z2)

        indx = im1.ravel() > 0
        z1, z2 = np.median(im1.ravel()[indx]), median_abs_deviation(im1.ravel()[indx])
        im1 = im1.clip(0, z1 + 5 * z2)

        # im1 = match_histograms(im1, im2)

        fixed = sitk.GetImageFromArray(im1)
        moving = sitk.GetImageFromArray(im2)
        outTx = tx._transform

        resampler = sitk.ResampleImageFilter()
        resampler.SetReferenceImage(fixed)
        resampler.SetInterpolator(sitk.sitkLinear)
        resampler.SetDefaultPixelValue(1)
        resampler.SetTransform(outTx)

        out = resampler.Execute(moving)
        array = sitk.GetArrayFromImage(out)

        data = (section_axio, section_stpt, match_st, dbeads, best_j, im1, array)
        data_enc = msgpack.packb(data, default=mn.encode)
        pl.send(data_enc)

    df = pd.DataFrame(
        [
            [section_axio, section_stpt, scale, flip, angle]
            + [fp2[0] - 100, fp2[1] - 100, fp2[2] + 200, fp2[3] + 200]
            + [fp1[0] - 100, fp1[1] - 100, fp1[2] + 200, fp1[3] + 200]
            + list(tx.center)
            + list(tx.translation)
            + list(tx.matrix)
        ],
        columns=[
            "axio",
            "stpt",
            "scale",
            "flip",
            "angle",
            "x_axio",
            "y_axio",
            "h_axio",
            "w_axio",
            "x_stpt",
            "y_stpt",
            "h_stpt",
            "w_stpt",
            "x_centre",
            "y_centre",
            "x_translation",
            "y_translation",
            "m00",
            "m10",
            "m01",
            "m11",
        ],
    )

    return df


def axio2stpt(args):

    if not args.stpt.exists():
        raise FileNotFoundError(f"File does not exist: {args.stpt}")

    if not args.axio.exists():
        raise FileNotFoundError(f"File does not exist: {args.axio}")

    ds_axio = xr.open_zarr(f"{args.axio}/mos")

    pl = NBPlot(args.pdf)

    info(f"Using {args.nprocs} processes")
    if args.sections is not None:
        sections = args.sections.split(",")
    else:
        sections = list(ds_axio)

    info(f"Running for {len(sections)} sections")
    watch = time.monotonic()

    set_verbose(args.verbose)

    f = partial(axio2stpt_firstpass, args.stpt, args.axio, pl=pl.plot_pipe)
    with Pool(processes=args.nprocs) as pool:
        df = pool.map(f, sections)

    pl.plot(finished=True)
    pl.plot_process.join()
    try:
        df = pd.concat(df)
    except Exception as e:
        error("ERROR:", e)
        df = pd.DataFrame()

    if args.output.suffix.endswith("csv"):
        df.to_csv(f"{args.output}", index=False)
    elif args.output.suffix.endswith("parquet"):
        df.to_parquet(f"{args.output}", index=False)
    elif args.output.suffix.endswith("npy"):
        df.to_numpy(f"{args.output}", index=False)
    elif args.output.suffix.endswith("pkl"):
        df.to_pkl(f"{args.output}", index=False)
    elif args.output == "stdout":
        print(df.to_string())
    else:
        df.to_csv(f"{args.output}", index=False)

    elapsed = int(time.monotonic() - watch)
    info(f"Finished in {elapsed} seconds")
