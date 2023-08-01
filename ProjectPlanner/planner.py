from collections import namedtuple
import csv
import tkinter

#making a named tuple to make accessing data later easier
Task_tuple = namedtuple("Task_tuple", ["title", "length", "prereq"])

def task_reader(file):
    # creating an empty dictionary to store the data from the csv
    dict_tasks = {}
    for row in csv.reader(open(file)):
        num = int(row[0])
        title = row[1]
        length = float(row[2])
        prereq = set(map(int, row[3].split))

        # since I dont want the data from the csv to change, I am storing in a tuple
        dict_tasks[num] = Task_tuple(title, length, prereq)

    #returns all data
    return dict_tasks

def task_orderer(dict_tasks):
    not_completed = set(dict_tasks)
    days_start = {}
    completed = set()

    #looping over incompleted task until they become completed
    while not_completed:
        for id_num in not_completed:
            task = dict_tasks[id_num]

            # checks if a preq has been done
            if task.prereq.issubset(completed):
                earliest_day_start = 0
                for no_prereq in task.prereq:
                    prereq_day_end = days_start[no_prereq] + dict_tasks[no_prereq].length
                    if prereq_day_end > earliest_day_start:
                        earliest_day_start = prereq_day_end
                days_start[id_num] = earliest_day_start
                completed.add(id_num)
                not_completed.remove(id_num)

    return days_start

#drwing the ghenttchart using tk
root = thinker.Tk()
root.title("Project Planner")
open_button = tkinter.Button(root, text="Open project", command=open_project)
open_button.pack(side="top")
canvas = tkinter.Canvas(root, width=800, height=400, bg="white")
canvas.psck(side="bottom")
tkinter.mainloop()
