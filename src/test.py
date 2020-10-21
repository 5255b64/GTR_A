import csv

file_name = "/run/media/gx/Garage/GTR_A/out/mutation/evosuite/Chart/1/evosuite/summary.csv"
with open(file_name, "r") as f:
    cr = csv.reader(f)
    for row in cr:
        print(row)
