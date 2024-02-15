
## ~~~ THIS CODE IMPORTS A FILE THAT WILL TAKE 5 PICTURES AND THEN IMPORTS A FILE ~~~ ##
## ~~~ THAT WILL TEST SPEED AND TAKES 5 PICTURES AND CALCULATES THE AVERAGE SPEED OF THOSE ~~~ ##
## ~~~ 5 PICTURES AND REPEATS UNTIL 5 MINUETS IS UP ~~~ ##


if __name__ == "__main__":

    # time - 2 seconds
    # ~ Import All Libraries ~ #
    from orbit import ISS
    from datetime import datetime, timedelta
    from take_exif_gps_photos import custom_capture

    start_time = datetime.now()  # code to tell me what time it started so I can see how long the code takes

    from save_file_txt_test1 import save_as_txt   # Code I created to save the file with special __File__ variable

    prev_time = datetime.now()

    import numpy as np

    from speed_detect import calculate_speed_of_ISS
    from picamera import PiCamera

    cam = PiCamera()
    cam.resolution = (4056, 3040)


    # ~ This code saves everything to a list ~ #
    def add_to_list(file_a, percentage_correct, line_mean, line_median, grad_mean, grad_median, speed_of_ISS):
        try:
            filenames.append(file_a)
            average_feature_distances.append(average_feature_distance)

            lines_means.append(line_mean)

            lines_medians.append(line_median)

            grad_means.append(grad_mean)

            grad_medians.append(grad_median)

            speeds.append(speed_of_ISS)

            percentage_for_df = percentage_correct, '%'

            percentages_for_df.append(round(percentage_correct))

            percentages.append(percentage_correct)

        except:

            print("ERROR!!!: ")

            print("filename (file_a): ", file_a)

            print("percentages: ", percentage_correct)

            print("line_mean: ", line_mean)

            print("line_median: ", line_median)

            print("grad_mean: ", grad_mean)

            print("grad_median: ", grad_median)

            print("speed_of_ISS: ", speed_of_ISS)

            error = [file_a, percentage_correct, line_mean, line_median, grad_mean, grad_median,
                     speed_of_ISS]

            errors.append(error)

        if percentage_correct < 60:
            bad_ones.append(path_1)

            bad_ones.append(path_2)

        return file_a, percentage_correct, line_mean, line_median, grad_mean, grad_median, speed_of_ISS, errors




    # import OS module

    # from colour_print import *

    import pandas as pd

    import os


    from save_speed import save_speed_as_txt # Code I created to save the file with special __File__ variable but also formating correctly

    # ~ The code I made to Take 5 photos ~ #
    from take_photos import take_5_photos

    # ~ Making Lists ~ #

    _good_speeds = []
    bad_ones = []
    all_speed = []

    speeds = []

    percentages = []
    percentages_for_df = []

    lines_means = []
    lines_medians = []
    grad_means = []
    grad_medians = []

    nan_speeds = []

    filenames = []

    average_feature_distances = []

    now_time = datetime.now()

    errors = []
    speeds_with_paths = []


    path = 'photos_for_speed'
    this_time = datetime.now()

    i = 0
    # Loop that will repeat untill 8 minutes has past
    while (now_time < start_time + timedelta(minutes=10)):
        # ~ Take 5 pics and put them into list to test speed through
        take_5_photos()

        dir_list = [f for f in os.listdir(path) if f.endswith('.jpg')]  # change ten to amount of files you want to list
        

        fs = sorted(dir_list)
        print("fs: ", fs)
        # ~ calculate speed with the 5 pics ~ #
    
        for i, f in enumerate(fs):
            
            print(i)

            # if f.endswith(".jpg") or f.endswith(".png"):

            # print('i: ', i)
            # ~ Make It be 4th time run because it is comparing speed with previos ~ #
            # if i > 0:

            file_a = fs[i-1] # find previos pic



            file_b = fs[i]

            # print(i, file_a, file_b)

            # ~ Make Paths for speed comapring ~ #
            path_1 = os.path.join(path, file_a)

            path_2 = os.path.join(path, file_b)


            # ~ Run the calculate speed of iss and get back lots of info ~ #
            (speed_of_ISS, percentage_correct, line_mean, line_median, grad_mean,

             grad_median, average_feature_distance, lines) = calculate_speed_of_ISS(

                image_1=path_1, image_2=path_2,

                filename_1=file_a, filename_2=file_b,

                grad_accuracy=0.6, dist_accuracy=10
            )

            if percentage_correct != 0.0: 
                speed_of_ISS = round(speed_of_ISS, 4)  # round to correct decimal places
                try:
                    speed_with_path = [path_1, speed_of_ISS]
                    speeds_with_paths.append(speed_with_path)
                except:
                    print("error")
                    print(path_1, speed_of_ISS)


                if i <= 2:
                    print("huraahh")
                    
                    file_a, percentage_correct, line_mean, line_median, grad_mean, grad_median, speed_of_ISS, errors = add_to_list(file_a, percentage_correct, line_mean, line_median, grad_mean, grad_median, speed_of_ISS)
                else:
                    print("i-2: ", i-2)
                    print("grad_means = ", grad_means)
                    print("file_a, percentage_correct, line_mean, line_median, grad_mean, grad_median, speed_of_ISS, errors = ", file_a, percentage_correct, line_mean, line_median, grad_mean, grad_median, speed_of_ISS, errors)
                    max_grad = grad_means[i-2]+20
                    min_grad = grad_means[i-2]-20
                    if max_grad > grad_mean > min_grad:
                        file_a, percentage_correct, line_mean, line_median, grad_mean, grad_median, speed_of_ISS, errors = add_to_list(file_a, percentage_correct, line_mean, line_median, grad_mean, grad_median, speed_of_ISS)
            
            else:
                if i > 1:
                    i -= 1
                    print("hellllooooooooooooooooooo   ", i)
                    
                else:
                    i = 0
                    print("hellllooooooooooooooooooo   ", i)
                    
            
            # i += 1
            now_time = datetime.now()
            one_min_since_last = this_time + timedelta(1)
            if datetime.now() + timedelta(0.4) > one_min_since_last :
                pic_name = f"gps_image_{datetime.now()}.jpg"
                custom_capture(ISS(), cam, pic_name)
                this_time = datetime.now()
        
        



                
            
        
    try:
        average_percentage = round(np.mean(percentages))

        print(average_percentage, "%")
    except:
        print("error") 
        print(percentages)

    # ~ make structure for pandas dataframe ~ #

    data = {

        'FileName': filenames,

        'Lines Mean': lines_means,

        'Lines Medians': lines_medians,

        'Grad Mean': grad_means,

        'Grad Medians': grad_medians,

        'Average Feature Dist': average_feature_distances,

        'Correct (%)': percentages_for_df,

        'Speed Of ISS': speeds

    }

    average_speed_of_ISS = np.median(speeds) # ? should we use other average

    print("length of speeds: ", len(speeds))

    print("length of filenames : ", len(filenames))

    print("length of lines mean : ", len(lines_means))

    print("length of lines median: ", len(lines_medians))

    print("length of grad_mean: ", len(grad_means))

    print("length of grad_median: ", len(grad_medians))

    print("length of average_feature_dist: ", len(average_feature_distances))

    print("length of correct (%): ", len(percentages_for_df))
    

    
    # ~ Make and save data frame and save to My_Data.html ~ #
    df = pd.DataFrame(data)

    df.to_html('My_Data.html')

    # ~ Print Average speed of ISS
    print('data writen to my_data.html')

    print("the average speed of the ISS is: ")

    print(("average_speed_of_ISS = ", average_speed_of_ISS))

    print(" ^^^^^^^^^^^^^^^^")

    time_taken = datetime.now() - prev_time
    

    print("time taken: ", time_taken)

    print("nan_speeds = ", nan_speeds)

    # ~ save as txt fil the speeds and the result speeed ~ #
    save_as_txt(str(speeds), 'Speeds.txt')
    save_speed_as_txt(average_speed_of_ISS, 'result.txt')

    
