import csv
import random
import glob
import time
import os

# things you can adjust in this script
########################################################


car_to_adjust = "df3"                           # the car to adjust,  set to the car abbreviation.  Example: "df3"
car_to_diff   = "random"                        # the car to compare against  # set to "random" to use a random car from the cars folder, otherwise set to the car abbreviation.  Example: "stk"

inc_dec       = 0.9                             # the amount to increase or decrease a value by.  0.9 = 90% of the original value. Best to keep below 1.0
odds          = 0.2                             # chance of adjusting a value.  I find it works better to have this lower when the inc_dec is higher. Valid range is 0.0 - 1.0
index_range_modifier = [list(range(0, 360))]    # default:  [list(range(0, 360))]   # a list of indexes to adjust.  Can be a single number or a range.  Example: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] or [list(range(0, 360))] or [list(range(0, 360)), 400, 401, 402, 403, 404, 405, 406, 407, 408, 409] or [list(range(0, 360)), 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, list(range(410, 420))]

grid_cars_path       = "D:\\Steam\\steamapps\\common\\GRID\\cars\\"                         # path to the Grid cars folder This is my path.  Change it to yours.  use double backslashes
grid_screenshot_path = "D:\\Steam\\userdata\\56736994\\760\\remote\\12750\\screenshots\\"   # path to the Grid screenshots folder '56736994' is my steam id.  Change it to yours.  use double backslashes

########################################################



# Define a function to adjust values
def adjust(value, factor):
    return float(value * factor)

# check if a value is a float/int
def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

# can be used if you want to adjust certain sets of values
def is_in_index_range_modifier(x, modifier):
    for element in modifier:
        # Check if the element is a list (range)
        if isinstance(element, list):
            if x in element:
                return True
        # Check if the element is an individual number
        elif x == element:
            return True
    return False

# adjust the values at a set percentage and takes into account the difference between the values of the cars
def inc_dec_car_specs(diff_value, value_to_be_adjusted):
    diff_value           = float(diff_value)
    value_to_be_adjusted = float(value_to_be_adjusted)

    # if the value is between -1 and 1, don't adjust it.  Adjusting these kinds of values can cause issues it seems
    if value_to_be_adjusted >= -1.0 and value_to_be_adjusted <= 1.0:
        #print("Between -1 and 1, not adjusting")
        adjusted_value = value_to_be_adjusted
    else:    
        
        difference = float(diff_value - value_to_be_adjusted)

        # if the adjust value is lesser then the car being diffed, decrease it 
        if difference > 0:
            if random.random() < odds:  # randomize the odds of adjusting a value
                difference = diff_value - value_to_be_adjusted
                adjusted_value = value_to_be_adjusted - (difference * (1.0 + inc_dec))
                print(f'original: {value_to_be_adjusted}')
                print(f'decrease: {adjusted_value}')
            else:
                #print("no decrease, not in the cards today")
                adjusted_value = value_to_be_adjusted

        # if the adjust value is greater then the car being diffed, increase it
        elif difference < 0:
            if random.random() < odds:  # randomize the odds of adjusting a value
                adjusted_value = value_to_be_adjusted + (difference * (1.0 + inc_dec))
                print(f'original: {value_to_be_adjusted}')
                print(f'increase: {adjusted_value}')
            else:
                #print("no increase, not in the cards today")
                adjusted_value = value_to_be_adjusted

        # if the adjust value is equal to the car being diffed, don't change it
        else:
            adjusted_value = value_to_be_adjusted  # No change needed
            #print("equal")
    
    #print(f'adjusted value: {adjusted_value}')
    return adjusted_value

# adjust the values at a set percentage and doesn't take into account the difference between the values of the cars
def inc_dec_car_specs_non_diff(diff_value, value_to_be_adjusted):
    diff_value           = float(diff_value)
    value_to_be_adjusted = float(value_to_be_adjusted)

    # if the value is between -1 and 1, don't adjust it.  Adjusting these kinds of values can cause issues it seems
    if value_to_be_adjusted >= -1.0 and value_to_be_adjusted <= 1.0:
        #print("Between -1 and 1, not adjusting")
        adjusted_value = value_to_be_adjusted
    else:
        if random.random() < odds:
            if random.random() <= 0.5:
                adjusted_value = adjust(value_to_be_adjusted, 1.0 - inc_dec)
                print(f'original: {value_to_be_adjusted}')
                print(f'decrease: {adjusted_value}')
            else:
                adjusted_value = adjust(value_to_be_adjusted, 1.0 + inc_dec)
                print(f'original: {value_to_be_adjusted}')
                print(f'increase: {adjusted_value}')
        else:
            adjusted_value = value_to_be_adjusted
    
    #print(f'adjusted value: {adjusted_value}')
    return adjusted_value

# write the adjusted values to a csv.  Both at the grid cars folder and the current directory
def update_car_specs(car_to_adjust, car_to_diff, index_range_modifier):

    adjusted_data = []

    # take car name and make csv path  
    car_to_adjust_csv = f'.\\originals\\{car_to_adjust}_original.csv'
    car_to_diff_csv   = f'.\\originals\\{car_to_diff}_original.csv'



    with open(car_to_diff_csv, 'r') as diff_file, open(car_to_adjust_csv, 'r') as adjust_file:
        diff_reader = csv.reader(diff_file)  
        adjust_reader = csv.reader(adjust_file)

        x = 0
        
        # loop through each value in the first row of the files using next()
        for diff_value, value_to_be_adjusted in zip(next(diff_reader), next(adjust_reader)):
            skip = False

            if is_in_index_range_modifier(x, index_range_modifier): # check if the index is in the index_range_modifier list
                skip = False

            if not is_float(value_to_be_adjusted) or not is_float(diff_value): # check if the value is a float
                skip = True

            if skip:
                adjusted_value = value_to_be_adjusted # No change needed
            else: 
                adjusted_value = inc_dec_car_specs_non_diff(diff_value, value_to_be_adjusted) # adjust the value

            x += 1
            adjusted_data.append(str(adjusted_value)) # add the adjusted value to the adjusted_data list

    save_files(adjusted_data, car_to_adjust)


def save_files(adjusted_data, car_to_adjust):
    # date time appended to the file name in file friendly format
    date = time.strftime("%Y%m%d-%H%M%S")
    
    car_to_adjust_name = f'{car_to_adjust}_{date}.csv'
    print(f'new file name: {car_to_adjust_name}')

    print(','.join(adjusted_data) + "\n\n")

    grid_car_path = f'{grid_cars_path}{car_to_adjust}\\{car_to_adjust}.csv'
    
    # Write the adjusted data to a new CSV file
    with open( grid_car_path, 'w', newline='') as adjusted_file:
        writer = csv.writer(adjusted_file)
        writer.writerows([adjusted_data])
        # write new line
        
        adjusted_file.write('\n\n')
    
    print(f'file saved as {grid_car_path}')



    # Write the adjusted data to a new CSV file
    with open(f'updated_configs\\{car_to_adjust_name}', 'w', newline='') as adjusted_file:
        writer = csv.writer(adjusted_file)
        writer.writerows([adjusted_data])
        # write new line
        
        adjusted_file.write('\n')

    print(f'file saved as updated_configs\\{car_to_adjust_name}')

def car_diff_select(car_to_diff):
    if car_to_diff == "random":
        # and car folder in the cars folder.  exclude files
        car_folders = glob.glob(f"{grid_cars_path}*\\")
    
        # remove the path from the folder names and trailing \\
        car_folders = [x.replace(grid_cars_path, '').replace('\\', '') for x in car_folders]

        # pick a random car folder
        random_diff_car = random.choice(car_folders)
        print(f'random car: {random_diff_car}')

        # there's a folder called originals in the current directory.  see if you car is in there
        if f'.\\originals\\{random_diff_car}_original.csv' in glob.glob(f".\\originals\\*"):
            print(f'{random_diff_car}_original.csv is in the originals folder.')
        else:
            # copy the car csv from the cars folder to the originals folder
            print(f'{random_diff_car}_original.csv is not in the originals folder.  Copying it now.')
            os.system(f'copy {grid_cars_path}{random_diff_car}\\{random_diff_car}.csv .\\originals\\{random_diff_car}_original.csv')
        car_diff_name = random_diff_car
    else:
       car_diff_name = car_to_diff

    return car_diff_name


if __name__ == "__main__":

    interval=5 # interval in seconds to check for new files

    file_list = glob.glob(f"{grid_screenshot_path}*") # get a list of files in the screenshots folder
    last_file_count = len(file_list) # get the number of files in the screenshots folder

    car_diff_name = car_diff_select(car_to_diff) 
    update_car_specs(car_to_adjust, car_diff_name, index_range_modifier)
    
    # loop forever checking for new files in the screenshots folder
    while True:

        print(f"Checking for new files in {grid_screenshot_path}.")
        file_list = glob.glob(f"{grid_screenshot_path}*")
        current_file_count = len(file_list)
        print(f"current file count: {current_file_count}")

        if current_file_count > last_file_count:
            print(f"New file detected in {grid_screenshot_path}.")
            time.sleep(5)

            car_diff_name = car_diff_select(car_to_diff)
            update_car_specs(car_to_adjust, car_diff_name, index_range_modifier)
            last_file_count = current_file_count

        time.sleep(interval)

