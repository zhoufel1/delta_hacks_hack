import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from matplotlib import style
import matplotlib.animation as animation
import pipe
from tinydb import TinyDB, Query
import time

import urllib
import json

import pandas as pd
import numpy as np

import tkinter as tk
from tkinter import ttk

import main

LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Verdana", 10)
SMALL_FONT = ("Verdana", 8)

# Drawing the Graph
f = Figure(figsize = (5, 5), dpi = 100)
a = f.add_subplot(111)
db = TinyDB("../delta_hacks/db.json")
dbquery = Query()


def popupmsg(msg):
    popup = tk.Tk()

    popup.wm_title("!")
    label = ttk.Label(popup, text=msg, font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10, expand=True)
    Button1 = ttk.Button(popup, text="Okay", command = popup.destroy)
    Button1.pack()
    popup.mainloop()

def animate(i):
    results = db.search(dbquery.item == "ped")[0]['history']
    xList = []
    yList = []
    for eachLine in results:
        if len(eachLine) > 1:
            xList.append(time.strftime("%H:%M", time.localtime(eachLine['time'])))
            yList.append(int(eachLine['total']))
    a.clear()
    a.plot(xList, yList)

class CityIQ(tk.Tk):
    style.use("ggplot")

    # args = arguments/variables | kwargs = dictionaries
    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        # tk.Tk.iconbitmap(self, default="citm.ico")
        tk.Tk.wm_title(self, "CityIQ Pipeline Application")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar, tearoff=0)

        filemenu.add_command(label="Upcoming Updates", command=lambda:popupmsg("""
        Upcoming updates: Traffic, Bicycle, Parking, Noise levels, Temperature!"""))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=quit)
        menubar.add_cascade(label="File", menu=filemenu)

        tk.Tk.config(self, menu=menubar)

        self.frames = {}

        for F in (StartPage, PedestrianPage, GraphPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

def qf(param):
    print(param)

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="CityIQ Pipeline Application", font=LARGE_FONT)
        label.pack()
        label2 = tk.Label(self, text=""" This application pulls data from two CityIQ monitors in Hamilton
        which is then piped """, font=NORM_FONT)
        label2.pack()
        button1 = ttk.Button(self, text="Show Pedestrian Data", command=lambda:popupmsg("""
        Future Updates, not yet patched"""))
        button1.pack()
        button2 = ttk.Button(self, text="Show Vehicle Data", command=lambda:popupmsg("""
        Future Updates, not yet patched"""))
        button2.pack()
        button3 = ttk.Button(self, text="Show Bicycle Data", command=lambda:popupmsg("""
        Future Updates, not yet patched"""))
        button3.pack()
        button4 = ttk.Button(self, text="Show Parking Data", command=lambda:popupmsg("""
        Future Updates, not yet patched"""))
        button4.pack()
        button5 = ttk.Button(self, text="Show Noise Level Data", command=lambda:popupmsg("""
        Future Updates, not yet patched"""))
        button5.pack()
        
class PedestrianPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Pedestrian Data", font=NORM_FONT)
        label.pack()

        #scrollbar for listbox
        scrollbar = tk.Scrollbar(self)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        listbox = tk.Listbox(self, width = 50)
        results = db.search(dbquery.item == "ped")[0]['history']
        for i in range(len(results)):
            listbox.insert(i, results[i])
        listbox.pack(side="top", expand = True)
        listbox.configure(yscrollcommand=scrollbar.set)
        scrollbar.configure(command=listbox.yview)

        button1 = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPage))
        button1.pack()
        button2 = ttk.Button(self, text="Show Graph", command=lambda: controller.show_frame(GraphPage))
        button2.pack()
        button3 = ttk.Button(self, text="Refresh Data", command=lambda: controller.show_frame(PedestrianPage))
        button3.pack()
        button4 = ttk.Button(self, text="Enable Data Fetch", command=lambda: main.data_fetcher())
        button4.pack()

class GraphPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Graph Page", font=NORM_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPage))
        button1.pack()
        button2 = ttk.Button(self, text="Back to Pedestrian Page", command=lambda: controller.show_frame(PedestrianPage))
        button2.pack()

        # Displaying the Graph (plt.show())
        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


app = CityIQ()
app.geometry("1280x720")
ani = animation.FuncAnimation(f, animate, interval=1000)
app.mainloop()
