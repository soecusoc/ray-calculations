#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
import numpy as np
import keyboard


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
        cview.create_rectangle(t, 0, t + 100, 100, fill="Red")
        root.after(10, tick)
        if keyboard.is_pressed("d"):
            t += 1
        if keyboard.is_pressed("a"):
            t -= 1

    tick()

    root.mainloop()
