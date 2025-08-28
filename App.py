import tkinter as tk
from tkinter import font
import ttkbootstrap as ttk #type:ignore
from PIL import Image #type:ignore
import time
import datetime
from winotify import Notification, audio #type:ignore

class App(ttk.Window):
    def __init__(self):
        super().__init__(themename='darkly')
        
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        center_x = int(screen_width/2 - 1000/2)
        center_y = int(screen_height/2 - 600/2)
        
        self.title('Order Test')
        self.geometry(f'1000x600+{center_x}+{center_y}')
        self.iconbitmap('icon.ico')
        
        self.HEADER = ttk.Label(self, text='Start Your Day Correct', font=('Bahnschrift SemiBold', 20)).pack(pady=10)
        self.A = Menu_Bar(self)
        self.B = Note(self)
        
        self.mainloop()

class Note(ttk.Notebook):
    def __init__(self, parent):
        super().__init__(parent)
        
        T1 = ttk.Frame(self, width=600, height=400)
        T1.pack()
        
        self.Task_1 = Task_Gen(T1)
        
        T2 = ttk.Frame(self, width=600, height=400)
        T2.pack()
        
        self.Task_2 = Task_Gen(T2)
        
        T3 = ttk.Frame(self, width=600, height=400)
        T3.pack()
        
        self.Task_3 = Task_Gen(T3)
        
        self.add(T1, text='Daily Tasks')
        self.add(T2, text='Weekly Tasks')
        self.add(T3, text='Monthly Tasks')
        
        self.pack()

class Task_Gen(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        MOTHER = ttk.Frame(self)
        MOTHER.pack()
        
        self.task_var = tk.StringVar(value='Set Task')
        self.time_var = tk.StringVar(value='Set Time')
        self.entry = ttk.Entry(MOTHER, textvariable=self.task_var).pack(side='left', padx=5, pady=5)
        self.entry_2 = ttk.Entry(MOTHER, textvariable=self.time_var).pack(side='left', padx=5, pady=5)
        self.button = ttk.Button(MOTHER, text='ENTER', command=self.create_task).pack(side='left')
        
        self.pack()
        
    def create_task(self):
        new_task = self.task_var.get()
        new_time = self.time_var.get()
        CHILD = ttk.Frame(self, width=600)
        CHILD.pack(side='top', anchor='nw', fill='x', expand=True, pady=5)
        ttk.Label(CHILD, text=new_task, anchor='w', wraplength=350).pack(side='left', expand=True)
        ttk.Button(CHILD, text='Complete', command=lambda: CHILD.pack_forget()).pack(side='left', padx=5)
        ttk.Label(CHILD, text=new_time).pack(side='left')
        self.target_alarm()
        self.check_alarm()
        
    def task_notification(self, task_msg):
        toast = Notification(app_id="Log-Book",
                     title="Task",
                     msg=f"{task_msg}",
                     duration="short",
                     )
        toast.set_audio(audio.Default, loop=False)
        toast.add_actions(label="Bring me there")
        toast.show()
        
    def target_alarm(self):
        self.preservation = self.time_var.get()
        print('TARGET_ALARM - STATUS FINE')

    def check_alarm(self):
        current_time = datetime.datetime.now().strftime("%H:%M")
        if hasattr(self, 'preservation') and current_time == self.preservation:
            self.task_notification(self.task_var.get())
            return
        self.after(1000, self.check_alarm)

class Menu_Bar(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        menu = tk.Menu(parent)
        
        #creating the menu widgets and storing them inside the parent menu widget
        first_menu = tk.Menu(menu, tearoff=False)
        second_menu = tk.Menu(menu, tearoff=False)
        third_menu = tk.Menu(menu, tearoff=False)
        fourth_menu = tk.Menu(menu, tearoff=False)
        
        #creating menu items and storing them inside the child menu widgets
        menu.add_cascade(label='File', menu=first_menu)
        menu.add_cascade(label='Edit', menu=second_menu)
        menu.add_cascade(label='Settings', menu=third_menu)
        menu.add_cascade(label='Help', menu=fourth_menu)
        
        first_menu.add_command(label='New File')
        first_menu.add_command(label='New Window')
        first_menu.add_command(label='Open File')
        first_menu.add_command(label='Save File')
        first_menu.add_separator()
        first_menu.add_command(label='Exit', command= lambda: parent.destroy())
        
        second_menu.add_command(label='Theme')
        second_menu.add_command(label='Create New Entry')
        second_menu.add_command(label='Delete Entry')
        
        third_menu.add_command(label='Change Window Size')
        third_menu.add_command(label='Change App Title')
        
        fourth_menu.add_command(label='Documentation')
        fourth_menu.add_command(label='Keyboard Shortcut Key References')
        fourth_menu.add_command(label='Report Issue')
        
        parent.configure(menu=menu)

App()