from pprint import pprint
from datetime import datetime

import cv2
import numpy as np
import matplotlib.pyplot as plt
import pickle as pkl

from utils import *

print(datetime.now())

KNN = 25
IMG_NAME = 'bpal'  # rpi pies ratu bpal
PREFIX_LENGTH = 4
BASE_IMG_PATH = '/home/mateusz/PWr/SI/SI_4/Photos800_600/'
IMG_1_FILE = f'{IMG_NAME}_1.png'
IMG_2_FILE = f'{IMG_NAME}_2.png'
# IMG_1_FILE = 'ratu_1.png'
# IMG_2_FILE = 'bpal_1.png'
HARAFF_SIFT = '.haraff.sift'
DRAW_POLYLINES = 0
DONT_DRAW_MATCHES = 1

LOAD = 1

img1 = cv2.imread(f'{BASE_IMG_PATH}/{IMG_1_FILE}')
img2 = cv2.imread(f'{BASE_IMG_PATH}/{IMG_2_FILE}')

key_points_img1 = key_points_to_dict(f'{BASE_IMG_PATH}/{IMG_1_FILE}{HARAFF_SIFT}')
key_points_img2 = key_points_to_dict(f'{BASE_IMG_PATH}/{IMG_2_FILE}{HARAFF_SIFT}')

if not LOAD:
    key_points_pairs = get_key_points_pairs(key_points_img1, key_points_img2, True)

    with open(f'key_points_pairs_{IMG_1_FILE[:PREFIX_LENGTH]}__{IMG_2_FILE[:PREFIX_LENGTH]}_k{KNN}.pkl', 'wb') as file:
        pkl.dump(key_points_pairs, file)

else:

    with open(f'key_points_pairs_{IMG_1_FILE[:PREFIX_LENGTH]}__{IMG_2_FILE[:PREFIX_LENGTH]}_k{KNN}.pkl', 'rb') as file:
        key_points_pairs = pkl.load(file)

# for kpp in key_points_pairs:
#     cv2.circle(img1, kpp[0], 5, (255, 255, 255))

# cv2.imshow('rdr', img1)
# cv2.waitKey(0)

key_points_pairs_A_dict = {point_A: point_B for point_A, point_B in key_points_pairs}
key_points_pairs_B_dict = {point_B: point_A for point_A, point_B in key_points_pairs}

key_points_img1_paired = {k: v for k, v in key_points_img1.items() if k in key_points_pairs_A_dict.keys()}
key_points_img2_paired = {k: v for k, v in key_points_img2.items() if k in key_points_pairs_B_dict.keys()}

if not LOAD:
    cohesion_pairs = neighbourhood_cohesion_pairs(KNN, key_points_pairs,
                                                  key_points_img1_paired, key_points_img2_paired,
                                                  key_points_pairs_A_dict, key_points_pairs_B_dict, True)

    with open(f'key_points_cohesion_pairs_{IMG_1_FILE[:PREFIX_LENGTH]}__{IMG_2_FILE[:PREFIX_LENGTH]}_k{KNN}.pkl',
              'wb') as file:
        pkl.dump(cohesion_pairs, file)

else:
    with open(f'key_points_cohesion_pairs_{IMG_1_FILE[:PREFIX_LENGTH]}__{IMG_2_FILE[:PREFIX_LENGTH]}_k{KNN}.pkl',
              'rb') as file:
        cohesion_pairs = pkl.load(file)

# for cp in cohesion_pairs:
#     cv2.circle(img1, cp[0], 5, (0, 0, 0))

# cv2.imshow('rdr', img1)
# cv2.waitKey(0)

cohesion_pairs = list(cohesion_pairs)  # in order to make it ordered

# find perspective transform
M, mask = cv2.findHomography(np.array([cp[1] for cp in cohesion_pairs]),
                             np.array([cp[0] for cp in cohesion_pairs]),
                             cv2.RANSAC, 5.0)  # maxIters -> parameter to use

# M, mask = cv2.findHomography(np.array([k for k,v in key_points_pairs_B_dict.items()]),
#                              np.array([v for k,v in key_points_pairs_B_dict.items()]),
#                              cv2.RANSAC, 5.0) # maxIters -> parameter to use

matches_mask = mask.ravel().tolist()
h, w, color_dim = img2.shape

pts_offset = 0
pts = np.float32(
    [[0 + pts_offset, 0 + pts_offset], [0 + pts_offset, h - 1 - pts_offset], [w - 1 - pts_offset, h - 1 - pts_offset],
     [w - 1 - pts_offset, 0 + pts_offset]]).reshape(-1, 1, 2)  # for drawing polylines, edges of img

dst = cv2.perspectiveTransform(pts, M)

if DRAW_POLYLINES:
    img2 = cv2.polylines(img2, [np.int32(dst)], True, 255, 3, cv2.LINE_AA)  # draw polylines of perspective

# input_cords= np.float32([[cp[0][0], cp[0][1]] for cp in cohesion_pairs[:4]])
# output_cords = np.float32([[cp[1][0], cp[1][1]] for cp in cohesion_pairs[:4]])

# m = cv2.getPerspectiveTransform(input_cords, output_cords) # 4 pairs

transform_rigid_mat, rigid_mask = cv2.estimateAffinePartial2D(np.array([[cp[1] for cp in cohesion_pairs]]),
                                                              np.array([[cp[0] for cp in cohesion_pairs]]),
                                                              method=cv2.RANSAC, maxIters=10000)  # maxIters ...

transform_rigid_mat_2x3 = transform_rigid_mat
transform_rigid_mat = np.vstack([transform_rigid_mat, [0., 0., 1.]])  # bottom row is missing so added

second_dst = cv2.perspectiveTransform(pts, transform_rigid_mat)

if DRAW_POLYLINES:
    img2 = cv2.polylines(img2, [np.int32(second_dst)], True, 100, 3, cv2.LINE_AA)  # estimated affine

# img2 = cv2.warpPerspective(img2, M, (img2.shape[1], img2.shape[0])) # warps img2 to look like img1
img2 = cv2.warpAffine(img2, transform_rigid_mat_2x3, (img2.shape[1], img2.shape[0]))  # warps img2 to look like img1

if DONT_DRAW_MATCHES:
    cohesion_pairs = {}  # to clear matches on imview

print('Pairs: ', len(cohesion_pairs))
draw_matches(img1, key_points_img1, img2, key_points_img2, cohesion_pairs)

# cv2.imshow('img3', img2)
# cv2.waitKey(0)

# TODO apply perspective and seek then


print(datetime.now())
