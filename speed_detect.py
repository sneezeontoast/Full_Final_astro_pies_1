## ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
## ~~ CODE TO CALCULATE SPEED BY COMPARING IMAGES ~~ ##

# ~ Imports: ~ #
from exif import Image  # import image data thing

import cv2  # import image processing library

import numpy as np
# import pandas as pd  # import data frame library
import math  # import library to do calculations

from datetime import datetime  # import time and stuff

from colour_print import *
from filter_lines import calculate_line_truth

# ~~~~~~~~~~~~~ #

# ~ The def to calculate it: ~ #
def calculate_speed_of_ISS(image_1, image_2, filename_1, filename_2, grad_accuracy, dist_accuracy):


    def get_time(image):
        with open(image, 'rb') as image_file:  # when the image is open
            img = Image(image_file)  # define image file
            time_str = img.get("datetime_original")
            time = datetime.strptime(time_str, '%Y:%m:%d %H:%M:%S')
        # print("time", time)
        return time

        # for data in img.list_all():

        #   print(data)

    def get_time_difference(image_1, image_2):
        time_1 = get_time(image_1)
        time_2 = get_time(image_2)
        time_difference = time_2 - time_1
        return time_difference.seconds

    def convert_to_cv(image_1, image_2):
        image_1_cv = cv2.imread(image_1, 0)
        image_2_cv = cv2.imread(image_2, 0)
        return image_1_cv, image_2_cv

    def calculate_features(image_1, image_2, feature_number):
        orb = cv2.ORB_create(nfeatures=feature_number)
        keypoints_1, descriptors_1 = orb.detectAndCompute(image_1_cv, None)
        keypoints_2, descriptors_2 = orb.detectAndCompute(image_2_cv, None)
        return keypoints_1, keypoints_2, descriptors_1, descriptors_2

    # ###~~~there are different ways  ~~~### #
    def calculate_matches(descriptors_1, descriptors_2):
        brute_force = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = brute_force.match(descriptors_1, descriptors_2)
        matches = sorted(matches, key=lambda x: x.distance)
        return matches



    def find_matching_coordinates(keypoints_1, keypoints_2, matches):  # , correct, times_ran):
        coordinates_1 = []
        coordinates_2 = []

        lines = []

        coordinates_1_test = []
        coordinates_2_test = []
        gradients = []
        _imatch = 0
        # grad = 0
        for match in matches:
            _imatch += 1
            image_1_idx = match.queryIdx
            image_2_idx = match.trainIdx
            (x1, y1) = keypoints_1[image_1_idx].pt
            (x2, y2) = keypoints_2[image_2_idx].pt

            delta_y = y2 - y1
            delta_x = x2 - x1

            # print("coordinates: ", ((x1, y1), (x2, y2)))

            # calculate line distance
            line_length = math.dist((x1, y1), (x2, y2))

            if delta_x == 0:
                _grad = 0
            else:
                _grad = delta_y / delta_x

            # print(delta_x, delta_x)
            # print(_grad)

            gradients.append(_grad)

            coordinates_1_test.append((x1, y1))
            # print(coordinates_1)
            coordinates_2_test.append((x2, y2))

            coordinates_1.append((x1, y1))
            coordinates_2.append((x2, y2))

            lines.append([_imatch, (x1, y1), (x2, y2), round(_grad, 5), line_length])

        return lines, coordinates_1, coordinates_2




    def calculate_mean_distance(_lines):
        dist_lines = [i[4] for i in _lines]

        return np.mean(dist_lines)

    def calculate_speed_in_kmps(feature_distance, GSD, time_difference):
        distance = feature_distance * GSD / 100000
        speed = distance / time_difference
        return speed

    def display_matches(image_1_cv, keypoints_1, image_2_cv, keypoints_2, matches, im_1_name, im_2_name):
        # print(keypoints_1[image_1_idx].pt)
        match_img = cv2.drawMatches(image_1_cv, keypoints_1, image_2_cv, keypoints_2, matches[:100], None)
        resize = cv2.resize(match_img, (1600, 600), interpolation=cv2.INTER_AREA)
        name = f'{im_1_name} \t \t{im_2_name}'
        cv2.imshow(name, resize)
        # cv2.waitKey(0)
        # print("about to shut window")
        cv2.destroyWindow(name)
        # print("shuted window")


    # Print the result

    time_difference = get_time_difference(image_1, image_2)  # Get time difference between images

    # print("image_1: ", image_1)
    # print("image_2: ", image_2)

    image_1_cv, image_2_cv = convert_to_cv(image_1, image_2)  # Create OpenCV image objects

    # Get keypoints and descriptors
    keypoints_1, keypoints_2, descriptors_1, descriptors_2 = calculate_features(image_1_cv, image_2_cv, 1000)

    matches = calculate_matches(descriptors_1, descriptors_2)  # Match descriptors

    lines, coordinates_1, coordinates_2 = find_matching_coordinates(keypoints_1, keypoints_2, matches)
    prev_lines = lines

    lines, lines_mean, lines_median, grad_mean, grad_median = calculate_line_truth(lines)

    average_feature_distance = calculate_mean_distance(lines)

    percentage = len(lines) / len(prev_lines) * 100
    print(
        "the amount that were correct were",
        percentage, "%",
        "and ", len(lines), "/", len(prev_lines)
    )

    # print("image_1_cv: ", image_1_cv)
    # print("keypointsc_1: ", keypoints_1)
    # print("image_2_cv: ", image_2_cv)
    # print("keypoints_2: ", keypoints_2)
    # print("matches", matches)

    # print("SPEED CALC")
    # print(average_feature_distance, time_difference)
    # print("average_feature_distance: ", average_feature_distance)
    #  print("time_difference: ", time_difference)

    speed_off_ISS = calculate_speed_in_kmps(average_feature_distance, 12648, time_difference)
    print_result("the speed of the ISS is: ")
    print_result(speed_off_ISS)
    print_red("^^^^^^^^^^^^^^^^^^^^^^")

    # display_matches(image_1_cv, keypoints_1, image_2_cv, keypoints_2, matches, image_1, image_2)  # Display matches
    # show_lines()
    titles = ['0', 'Coordinates_1       ', 'Coordinates_2      ', 'Gradient ', 'Line Length ']

    return speed_off_ISS, percentage, lines_mean, lines_median, grad_mean, grad_median, average_feature_distance, lines



# speed_of_ISS, percentage_correct, line_mean, line_median, grad_mean, grad_median, average_feature_distance, lines = calculate_speed_of_ISS(
#     image_1=path_to_image_1, image_2=path_to_image_1,
#     filename_1=filename_1, filename_2=filename_2,
#     grad_accuracy=0.6, dist_accuracy=10  # how accurate these work best
# )
# print(grad_mean)

# print_red(speed_of_ISS)