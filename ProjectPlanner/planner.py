import csv

def task_reader(file):
    # creating an empty dictionary to store the data from the csv
    dict_tasks = {}
    for row in csv.reader(open(file)):
        num = int(row[0])
        title = row[1]
        length = float(row[2])
        prereq = row[3]

        # since I dont want the data from the csv to change, I am storing in a tuple
        dict_tasks[num] = (title, length, prereq)

    #returns all data
    return dict_tasks
