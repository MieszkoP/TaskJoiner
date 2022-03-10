from functions import *
import csv
import sys

file_path1, file_path2, column_name, join_type = enter_input(input('Enter command: \n'))

with open('NewTable.csv', 'w', encoding="UTF-16", newline='') as file:
    csvwriter = csv.writer(file)
    x = script_reader(file_path1, file_path2, column_name, join_type)
    for i in x:
        csvwriter.writerow(i)
