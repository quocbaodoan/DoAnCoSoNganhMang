import tkinter as tk
import tkinter.font as tkFont
import tkinter.ttk as ttk
import psutil
from tkinter import filedialog, Text
import os
from process import getListOfProcessSortedByMemory
import time

header = ['Name', 'Memory']

def getListOfProcessSortedByMemory():
    '''
    Get list of running process sorted by Memory Usage
    '''
    listOfProcObjects = []
    # Iterate over the list
    for process in psutil.process_iter():
       try:
            # Fetch process details as dict
            pinfo = process.as_dict(attrs=['name'])
            pinfo['vms'] = round(process.memory_info().vms / (1024 * 1024), 1)
            # Append dict to list
            listOfProcObjects.append(pinfo)
       except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
           pass
    # Sort list of dict by key vms i.e. memory usage
    listOfProcObjects = sorted(listOfProcObjects, key=lambda procObj: procObj['vms'], reverse=True)
    return listOfProcObjects

def endProcess(process):
    print(process)
    for proc in psutil.process_iter():
        # check whether the process name matches
        # print(proc.name())
        if any(procstr in proc.name() for procstr in [process]):
            print(f'Killing {proc.name()}')
            proc.kill()

def buildHeader():
    for col in header:
        tree.heading(col, text=col.title())
        # adjust the column's width to the header string
        if (col == "Name"):
            tree.column(col, width=300)
        else:
            tree.column(col, width=100)
    
def buildProcess():
    tree.delete(*tree.get_children())

    listOfRunningProcess = getListOfProcessSortedByMemory()
    for process in listOfRunningProcess:
        tree.insert('', 'end', values=(process['name'], process['vms']))
    root.after(2000, buildProcess)

def select_item(event):  # added  and a (event)
    test_str_library = tree.item(tree.selection())# gets all the values of the selected row
    print('The test_str = ', type(test_str_library), test_str_library, '\n')  # prints a dictionay of the selected row
    item = tree.selection()[0] # which row did you click on
    print('item clicked ', item) # variable that represents the row you clicked on
    print(tree.item(item)['values'][0]) # prints the first value of the values (the id value)

def endProcess():
    item = tree.selection()[0]
    process = tree.item(item)['values'][0]
    print(process)
    for proc in psutil.process_iter():
        # check whether the process name matches
        # print(proc.name())
        if any(procstr in proc.name() for procstr in [process]):
            print(f'Killing {proc.name()}')
            proc.kill()

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Task Manager")
    root.geometry('420x600')

    style = ttk.Style(root)
    style.configure('Treeview', rowheight=25)
    tree = None
    container = ttk.Frame()
    container.pack(fill='both', expand=True)

    # create a treeview with dual scrollbars
    tree = ttk.Treeview(columns=header, show="headings")
    vsb = ttk.Scrollbar(orient="vertical",
        command=tree.yview)
    hsb = ttk.Scrollbar(orient="horizontal",
        command=tree.xview)
    tree.configure(yscrollcommand=vsb.set,
        xscrollcommand=hsb.set)
    tree.grid(column=0, row=0, sticky='nsew', in_=container)
    vsb.grid(column=1, row=0, sticky='ns', in_=container)
    hsb.grid(column=0, row=1, sticky='ew', in_=container)
    container.grid_columnconfigure(0, weight=1)
    container.grid_rowconfigure(0, weight=1)

    

    buildHeader()
    buildProcess()

    tree.bind('<ButtonRelease-1>', select_item) 
    
    end_proc_button = tk.Button(root, text="End Process", padx=10, pady=4, fg="white", bg="#263D42", command=endProcess)
    end_proc_button.pack()

    root.mainloop()