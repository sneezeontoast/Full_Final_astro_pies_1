## ~~ THE CODE TO FILTER THE SPEED ~~ ##

# ~ Imports ~ #
import numpy as np

import cv2
# ~ ~~~~~~~ ~ #


# ~ Definition To See If the point is on the wire ~ #
def not_on_wire(x_y_point):

    x = x_y_point[0]
    y = x_y_point[1]

    if x <= 200 and 1030 <= y <= 1800:
        return False
    else:
        return True
# ~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ~ #

def calculate_line_truth(test_lines):
    # print("test_lines = ", test_lines)
    grad_accuracy = 0.6 # Accuracy tested to be best
    dist_accuracy = 10
    new_matches_1 = []

    # ~ Go Through List And Test If Not On Wire Take Of If On Wire ~
    for l in test_lines:
        if not_on_wire(l[1]):
            # print_red('not on line')
            new_matches_1.append(l)
        elif not_on_wire(l[2]):
            # print_red('not on line')
            new_matches_1.append(l)
    # ~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ~ #

    _bad_ones = []

    # ~ Filter Using Average ~ #
    new_matches_2, grad_mean, grad_median = stats(test_lines, 'grad', grad_accuracy)
    new_matches_2, lines_mean, lines_median = stats(new_matches_2, 'dist', dist_accuracy)
    # ~ ~~~~~~~~~~~~~~~~~~~~ ~ #

    # ~ Make Sure it is not finding part of spacecraft by testing is the point is still ~ #
    def is_filter(n):
        if round(n[3], 1) != 0.0:
            return True
        else:
            return False

    new_matches_3 = [c for c in test_lines if is_filter(c)]
    # ~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ~ #

    # ~ Find Smallest Line Within Line Of L ~ #
    def smallest_of(l):
        for i, m in enumerate(l):
            if i == 0:
                min_len = m
            else:
                if len(m) < len(min_len):
                    min_len = m

        return min_len

    # ~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ~ #

    all_new_matches = [new_matches_1, new_matches_2, new_matches_3]

    # ~ Remove Lists With No Contents ~ #
    for i, m in enumerate(all_new_matches):
        if len(m) == 0:
            all_new_matches.remove(m)
    # ~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ~ #

    # ~ If Filters Filter To Much Don't Filter Else Use Smallest Part Of all_new_matches ~ #
    if len(all_new_matches) == 0:
        new_matches = test_lines

    else:
        new_matches = smallest_of([new_matches_1, new_matches_2, new_matches_3])
    # ~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ~ #

    return new_matches, lines_mean, lines_median, grad_mean, grad_median  # not def


def stats(lines, param, fact):  # l = list
    # ~ See If it is Gradient or grad in param to know which part of list to use ~ #

    if param.lower() in ['gradient','grad']:
        n = 3
    elif param.lower() in ['distance','dist']:
        n = 4
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

    # ~ create list g with just the n (n will be 3 or 4 if it is gradient or distance) element of the list ~ #
    g = [l[n] for l in lines]
    # ~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ~ #

    mean, median, s_t_d = np.mean(g), np.median(g), np.std(g)  # return mean and median averaged and standard deviations

    # Make min and max for filtering #
    max_val = median + s_t_d*fact
    min_val = median - s_t_d*fact



    new_matches = [l for l in lines if min_val <= l[n] <= max_val]  # This line of code filteres it using the min and max

    removed = [l for l in lines if l not in new_matches] # this line tells you what is not in new matches
    # ~ the full code not shortened is bellow ~ #
    # ~ The code for the list comprehension above: ~ #
    """
    def filter(x):
       _grad = x[n]
       if min_val < _grad < max_val:
           return True
       else:
           return False
    
    def bad_stuff(x):
       _grad = x[4]
       if min_val < _grad < max_val:
           return False
       else:
           return True
    

    removed = [c for c in lines if bad_stuff(c)]
    
    if len(lines) == 0:
        print(len(new_matches))
    else:
        print(len(new_matches) * 100 // len(lines))
    
    print("removed: ", removed)
    """

    return new_matches, mean, median

