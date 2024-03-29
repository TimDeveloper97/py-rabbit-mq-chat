from tkinter import *
import sys 
from A12_v2 import ChatApplication

root = Tk() 
top = Toplevel() 
# top.geometry("600x600")
# top.rowconfigure(3, weight=1)
# top.columnconfigure(3, weight=1)


username_label = Label(top , text="Username:")
room_label = Label(top , text="Room:")
username = Entry(top) 
room = Entry(top)
join = Button(top, text="Join", command=lambda:command1()) 
cancel = Button(top, text="Cancel", command=lambda:command2())

# Grid layout
# username_label.grid(row=0, column=0)
# username.grid(row=0, column=1)
# room_label.grid(row=1, column=0)
# room.grid(row=1, column=1)
# join.grid(row=2, column=0)
# cancel.grid(row=2, column=1)

# Command
def command1():
    if username.get() != "" and room.get() != "": 
        mainwindow = ChatApplication(root, username.get(), room.get())
        root.withdraw()
        top.destroy() 

def command2():
    top.destroy()
    root.destroy() 
    sys.exit()


username_label.pack() 
username.pack()
room_label.pack()
room.pack()
join.pack()
cancel.pack()

root.withdraw()
root.mainloop() 