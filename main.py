#!/usr/bin/env python3
import pipe
import time
import gui

running = False

f = gui.Figure(figsize=(5, 5), dpi=100)
a = f.add_subplot(111)


def data_fetcher():
    data_pipe = pipe.Pipe()
    data_pipe.fetch_token()
    if running:
        response = data_pipe.fetch_pedestrian_data('f6057765-ae16-4b8a-b0b8-c48de3b193c6', 1579962143154, 1580048543154)
        print("Data retrieved... ")
        time.sleep(4)
    data_fetcher()

def start():
    global running
    running = True
    data_fetcher()

def stop():
    global running
    running = False

def main_gui():
    app = gui.CityIQ()
    app.geometry("1280x720")
    ani = gui.animation.FuncAnimation(f, gui.animate, interval=1000)
    app.mainloop()


if __name__ == '__main__':
    main_gui()
