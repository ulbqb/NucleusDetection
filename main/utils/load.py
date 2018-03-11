
#
# load.py : utils on generators / lists of ids to transform from strings to
#           cropped images and masks

import os
import numpy as np

from PIL import Image
from functools import partial
from .utils import normalize
import pdb


def get_ids(dir):
    """Returns a list of the ids in the directory"""
    return [f.split(".")[0] for f in os.listdir(dir)]


def split_ids(ids, n=2):
    """Split each id in n, creating n tuples (id, k) for each id"""
    return [(id, i) for i in range(n) for id in ids]


def to_resized_imgs(ids, dir, suffix, size, drop_alpha=True):
    """From a list of tuples, returns the resized img"""
    original_sizes = []
    for id in ids:
        im = Image.open(dir + id + suffix)
        original_sizes.append(im.size)
        im = im.resize(size) #ここでリサイズする
        if drop_alpha:
            yield np.asarray(im)[:, :, :3] #alpha channelを落とす
        else:
            yield np.asarray(im)


def get_original_sizes(ids, dir, suffix):
    original_sizes = []
    for id in ids:
        im = Image.open(dir + id + suffix)
        original_sizes.append(im.size)
    return original_sizes


def get_imgs_and_masks(ids, dir_img, dir_mask, dir_edge, size):
    """Return all the couples (img, mask)"""
    imgs = to_resized_imgs(ids, dir_img, '.png', size)
    # need to transform from HWC to CHW
    imgs_switched = map(partial(np.transpose, axes=[2, 0, 1]), imgs)
    imgs_normalized = map(normalize, imgs_switched)
    masks = to_resized_imgs(ids, dir_mask, '.png', size, drop_alpha=False)
    edges = to_resized_imgs(ids, dir_edge, '.png', size, drop_alpha=False)
    return zip(imgs_normalized, masks, edges)
