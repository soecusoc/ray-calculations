#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import Tkinter as tk
import numpy as np


if __name__ == '__main__':
    root = tk.Tk()
    frame_main = tk.Frame(root)
    frame_main.pack()
    frame_left = tk.Frame(frame_main)
    frame_left.pack(side=tk.LEFT)
    frame_right = tk.Frame(frame_main)
    frame_right.pack(side=tk.RIGHT)
    cmap = tk.Canvas(frame_left, width=300, height=200, bg="Blue")
    cmap.pack()
    cview = tk.Canvas(frame_right, width=300, height=200, bg="Green")
    cview.create_rectangle(0, 0, 100, 100, fill="Red")
    cview.pack()

    t = 0

    def tick():
        global t
        cview.delete(tk.ALL)
        cview.create_rectangle(t, t, t + 100, t + 100, fill="Red")
        root.after(10, tick)
        t += 1

    tick()

    root.mainloop()
