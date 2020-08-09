import numpy as np
import matplotlib.pyplot as plt
import cv2


def key_points_to_dict(filepath):
    key_points_dict = {}

    with open(filepath) as file:
        for line in file:
            line_split = line.strip('\n').split(' ')
            if len(line_split) < 2:
                continue

            x_coordinate = int(float(line_split[0]))
            y_coordinate = int(float(line_split[1]))
            key_points_dict[(x_coordinate, y_coordinate)] = (
                [float(param_A_B_C) for param_A_B_C in line_split[2:5]],
                [int(param_n) for param_n in line_split[5:]])

    return key_points_dict


def find_nearest_neighbour(key_point_A: tuple, key_points_dict_A: dict, key_points_dict_B: dict):
    best_score = float('inf')  # the higher the furthest neighbour
    nearest_neighbour_B = None

    for k, v in key_points_dict_B.items():
        score = sum(np.bitwise_xor(key_points_dict_A[key_point_A][1], v[1]))
        if score < best_score:
            best_score = score
            nearest_neighbour_B = k

    return nearest_neighbour_B


def get_k_nearest_neighbours(_k: int, key_point_A: tuple, key_points_dict_A: dict, key_points_dict_B: dict,
                             verbose=False):
    scores = []

    if verbose:
        iter_count = 0

    for k, v in key_points_dict_B.items():
        score = sum(np.bitwise_xor(key_points_dict_A[key_point_A][1], v[1]))
        scores.append((score, k))

        if verbose:
            iter_count += 1
            print(
                f'Getting nearest neighbours, iterating {key_point_A}: {round(iter_count * 100 / len(key_points_dict_B), 1)}%')

    return {score[1] for score in sorted(scores)[:_k]}


def get_key_points_pairs(key_points_dict_A: dict, key_points_dict_B: dict, verbose=False):
    neighbours_A = set()
    neighbours_B = set()

    if verbose:
        a_iter_count = 0
        b_iter_count = 0

    for k_A, v_A in key_points_dict_A.items():
        k_B = find_nearest_neighbour(k_A, key_points_dict_A, key_points_dict_B)
        neighbours_A.add((k_A, k_B))

        if verbose:
            a_iter_count += 1
            print(f'Finding key points pairs, iterating A: {round(a_iter_count * 100 / len(key_points_dict_A), 1)}%')

    for k_B, v_B in key_points_dict_B.items():
        k_A = find_nearest_neighbour(k_B, key_points_dict_B, key_points_dict_A)
        neighbours_B.add((k_A, k_B))

        if verbose:
            b_iter_count += 1
            print(f'Finding key points pairs, iterating B: {round(b_iter_count * 100 / len(key_points_dict_B), 1)}%')

    return neighbours_A.intersection(neighbours_B)


def neighbourhood_cohesion_pairs(knn_k: int, key_points_pairs: set, key_points_dict_A: dict, key_points_dict_B: dict,
                                 key_points_pairs_dict_A: dict, key_points_pairs_dict_B: dict, verbose=False):
    cohesion_pairs = set()

    if verbose:
        iter_count = 0

    for pair in key_points_pairs:
        neighbourhood_A = get_k_nearest_neighbours(knn_k, pair[0], key_points_dict_A, key_points_dict_B)
        neighbourhood_B = get_k_nearest_neighbours(knn_k, pair[1], key_points_dict_B, key_points_dict_A)

        score = sum([1 for neighbour_A in neighbourhood_A if key_points_pairs_dict_B[neighbour_A] in neighbourhood_B])

        if score > knn_k // 2:
            # if score > 17:
            cohesion_pairs.add(pair)

        if verbose:
            iter_count += 1
            print(f'Getting cohesion pairs: {round(iter_count * 100 / len(key_points_pairs), 1)}%')

    return cohesion_pairs


def draw_matches(img1, kp1, img2, kp2, matches, color=None):
    """Draws lines between matching keypoints of two images.
    Keypoints not in a matching pair are not drawn.
    Places the images side by side in a new image and draws circles
    around each keypoint, with line segments connecting matching pairs.
    You can tweak the r, thickness, and figsize values as needed.
    Args:
        img1: An openCV image ndarray in a grayscale or color format.
        kp1: A list of cv2.KeyPoint objects for img1.
        img2: An openCV image ndarray of the same format and with the same
        element type as img1.
        kp2: A list of cv2.KeyPoint objects for img2.
        matches: A list of DMatch objects whose trainIdx attribute refers to
        img1 keypoints and whose queryIdx attribute refers to img2 keypoints.
        color: The color of the circles and connecting lines drawn on the images.
        A 3-tuple for color images, a scalar for grayscale images.  If None, these
        values are randomly generated.
    """
    # We're drawing them side by side.  Get dimensions accordingly.
    # Handle both color and grayscale images.
    if len(img1.shape) == 3:
        new_shape = (max(img1.shape[0], img2.shape[0]), img1.shape[1] + img2.shape[1], img1.shape[2])
    elif len(img1.shape) == 2:
        new_shape = (max(img1.shape[0], img2.shape[0]), img1.shape[1] + img2.shape[1])
    new_img = np.zeros(new_shape, type(img1.flat[0]))
    # Place images onto the new image.
    new_img[0:img1.shape[0], 0:img1.shape[1]] = img1
    new_img[0:img2.shape[0], img1.shape[1]:img1.shape[1] + img2.shape[1]] = img2

    # Draw lines between matches.  Make sure to offset kp coords in second image appropriately.
    r = 3
    thickness = 1
    if color:
        c = color
    for m in matches:
        # Generate random color for RGB/BGR and grayscale images as needed.
        if not color:
            c = np.random.randint(0, 256, 3) if len(img1.shape) == 3 else np.random.randint(0, 256)
            c = (int(c[0]), int(c[1]), int(c[2]))
        # So the keypoint locs are stored as a tuple of floats.  cv2.line(), like most other things,
        # wants locs as a tuple of ints.
        end1 = tuple(np.round(m[0]).astype(int))
        end2 = tuple(np.round(m[1]).astype(int) + np.array([img1.shape[1], 0]))
        cv2.line(new_img, end1, end2, c, thickness)
        cv2.circle(new_img, end1, r, c, thickness)
        cv2.circle(new_img, end2, r, c, thickness)

    # plt.figure(figsize=(15, 15))
    cv2.imshow("IMG3", new_img)
    cv2.waitKey(0)
    # plt.imshow(new_img)
    # plt.show()
