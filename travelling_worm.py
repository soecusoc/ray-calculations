# -*- coding: utf-8 -*-

import tkinter as tk
import keyboard


t = 0
momentum = "right"


# Bonus, the game of a travelling worm.
# The values are hard coded for now.
def travelling_worm():
    worm_size = 10
    positions = [(100, 0), (90, 0), (80, 0), (70, 0), (60, 0), (50, 0), (40, 0), (30, 0), (20, 0), (10, 0), (0, 0)]

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
    for pos in positions:
        cview.create_rectangle(pos[0], pos[1], worm_size, worm_size, fill="Red", width=1)
    cview.pack()

    def tick():
        global t
        # Change momentum according key presses.
        global momentum
        if keyboard.is_pressed("d"):
            momentum = "right"
        elif keyboard.is_pressed("s"):
            momentum = "down"
        elif keyboard.is_pressed("a"):
            momentum = "left"
        elif keyboard.is_pressed("w"):
            momentum = "up"

        # This value controls the speed of the snake.
        if t > 49:
            t = 0
            # Update position
            for i in reversed(range(1, len(positions))):
                positions[i] = positions[i-1]
            if momentum == "right":
                positions[0] = (positions[0][0] + worm_size, positions[0][1])
            if momentum == "down":
                positions[0] = (positions[0][0], positions[0][1] + worm_size)
            if momentum == "left":
                positions[0] = (positions[0][0] - worm_size, positions[0][1])
            if momentum == "up":
                positions[0] = (positions[0][0], positions[0][1] - worm_size)
            cview.delete(tk.ALL)
            for pos in positions:
                cview.create_rectangle(pos[0], pos[1], pos[0] + worm_size, pos[1] + worm_size, fill="Red", width=1)
            cview.update()
        t += 1

        # This value controls the refresh rate.
        root.after(10, tick)

    tick()

    root.mainloop()
