import csv
from collections import namedtuple
import tkinter
from tkinter.filedialog import askopenfilename

#making a named tuple to make accessing data later easier
Task_tuple = namedtuple("Task_tuple", ["title", "length", "prereq"])


def main():
    root = tkinter.Tk()
    root.title("Project Planner")
    open_button = tkinter.Button(root, text="Open project", command=open_project)
    open_button.pack(side="top")
    canvas = tkinter.Canvas(root, width=800, height=400, bg="white")
    canvas.pack(side="bottom")
    tkinter.mainloop()


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
def draw_chart(tasks, canvas, row_height=40, title_width=300, line_height=40, day_width=20, bar_height=20, title_indent=20, font_size=-16):
    height = canvas["height"]
    width = canvas["width"]
    week_width = 5 * day_width
    canvas.create_line(0, row_height, width, line_height, fill="grey")
    for week_number in range(5):
        x = title_width + week_number * week_width
        canvas.create_line(x, 0, x, height, fill="grey")
        canvas.create_text(x + week_width/2, row_height/2, text=f"Week {week_number + 1}", font=("Helvetica", font_size, "bold"))
        start_days = task_orderer(tasks)
        y = row_height
        for task_number in start_days:
            task = tasks[task_number]
            canvas.create_text(title_indent, y + row_height / 2, text=task.title, anchor=tkinter.W, font=("Helvetica", font_size))
            bar_x = title_width + start_days[task_number] * day_width
            bar_y = y + (row_height - bar_height) / 2
            bar_width = task.length * day_width
            canvas.create_rectangle(bar_x, bar_y, bar_x + bar_width, bar_y + bar_height, fill="red")
            y = y + row_height

def open_project():
    filename = askopenfilename(title="Open Project", initialdir=".", filetypes=[("CSV Document", "*.csv")])
    tasks = task_reader(filename)
    draw_chart(tasks, canvas)


if __name__ == "__main__":
    main()
