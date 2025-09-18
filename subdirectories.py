import os
import csv

# Specify the directory for which you want to list sub-directories
directory_path = "D:\Appleton School of English\Clients\Formation Professionnelle\Formations terminées et facturées"

# Create a list to store sub-directories
subdirectories = []

# Iterate through the directory and list sub-directories
for root, dirs, files in os.walk(directory_path):
    for dir_name in dirs:
        subdirectories.append(os.path.join(dir_name))
        print(dir_name)

# Specify the output CSV file path
csv_file_path = "D:\Appleton School of English\Clients\subdirectories.csv"

# Write the sub-directories to a CSV file, one per row
with open(csv_file_path, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows([[subdir] for subdir in subdirectories])

print(f"Sub-directories listed and saved to {csv_file_path}")
