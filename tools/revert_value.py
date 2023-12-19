import csv

def revert_values(original_csv_path, destination_csv_path, indexes_to_revert):
    # Read the original CSV file
    with open(original_csv_path, mode='r', newline='') as file:
        reader = csv.reader(file)
        org_row = next(reader)  # Assuming there's only one row

        # Write the modified row to the destination CSV file
    with open(destination_csv_path, mode='r', newline='') as file:
        reader = csv.reader(file)
        dest_row = next(reader)  # Assuming there's only one row

    # Revert values at specified indexes
    for index in indexes_to_revert:
        dest_row[index] = org_row[index]

    # Write the modified row to the destination CSV file
    with open(destination_csv_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(dest_row)



# Example usage
original_csv = "D:\\Steam\\steamapps\\common\\GRID\\cars\\df3\\df3.csv"
destination_csv = "df3_original.csv"
indexes = [26, 97, 161]  # Example indexes to revert

revert_values(original_csv, destination_csv, indexes)
