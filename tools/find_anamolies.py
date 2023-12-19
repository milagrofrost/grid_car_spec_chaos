import csv
import os

def read_csv(file_path):
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        return next(reader)  # Assuming each CSV file has only one row

def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def float_equal(val1, val2):
    return is_float(val1) and is_float(val2) and float(val1) == float(val2)

def find_intersect_of_changes(reference_file, folder_path):
    reference_data = read_csv(reference_file)
    changed_indices_per_file = []

    for filename in os.listdir(folder_path):
        if filename.endswith('.csv') and filename != os.path.basename(reference_file):
            file_path = os.path.join(folder_path, filename)
            current_data = read_csv(file_path)
            
            changed_indices = {i for i, (ref_val, curr_val) in enumerate(zip(reference_data, current_data))
                               if ref_val != curr_val and not float_equal(ref_val, curr_val)}
            changed_indices_per_file.append(changed_indices)
            print(changed_indices_per_file)
    
    # Find intersection of all sets of changed indices
    intersected_indices = set.intersection(*changed_indices_per_file) if changed_indices_per_file else set()
    return sorted(intersected_indices), current_data

# Defining the paths
folder_path = "./scenarios/frontwheelslockedup/"
reference_file = "df3_original.csv"

# Finding the intersected indices
intersected_indices, current_data = find_intersect_of_changes(reference_file, folder_path)
print(intersected_indices)

for index in intersected_indices:
    print(current_data[index])
