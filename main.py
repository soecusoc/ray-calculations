# -*- coding: utf-8 -*-

import tkinter as tk
import numpy as np
import keyboard


class Camera:
    def __init__(self, parent, x=None, y=None, n_rays=36):
        if x is None or y is None:
            x = int(int(parent.cget("width")) / 2)
            y = int(int(parent.cget("height")) / 2)
        self.x = x
        self.y = y
        self.n_rays = n_rays
        self.parent = parent

    def update_rays(self):
        wall_indices = self.parent.find_withtag("walls")
        walls = list()
        for idx in wall_indices:
            # returns a list: [x1, y1, x2, y2]
            walls.append(self.parent.coords(idx))
        for idx in self.parent.find_withtag("rays"):
            self.parent.delete(idx)
        for angle in np.linspace(0, 2 * np.pi, self.n_rays, endpoint=False):
            # TODO: Find, whether the ray and the wall collides.
            # Math in file 'Ray_Wall_collision_calculations.txt'.
            dx = int(np.round(40 * np.cos(angle)))
            dy = int(np.round(40 * np.sin(angle)))
            self.parent.create_line(self.x, self.y, self.x + dx, self.y + dy, tags="rays")
        self.parent.pack()


def set_borders(parent):
    x_max = parent.cget("width")
    y_max = parent.cget("height")
    parent.create_line(1, 1, x_max, 1, tags="walls", width=1)
    parent.create_line(1, 1, 1, y_max, tags="walls", width=1)
    parent.create_line(1, y_max, x_max, y_max, tags="walls", width=1)
    parent.create_line(x_max, 1, x_max, y_max, tags="walls", width=1)
    parent.pack()


def set_random_walls(parent):
    for i in range(5):
        x1 = int(np.random.randint(1, 300, 1)[0])
        x2 = int(np.random.randint(1, 300, 1)[0])
        y1 = int(np.random.randint(1, 200, 1)[0])
        y2 = int(np.random.randint(1, 200, 1)[0])
        parent.create_line(x1, y1, x2, y2, tags="walls", width=1)
        parent.pack()


if __name__ == '__main__':
    root = tk.Tk()
    frame_main = tk.Frame(root)
    frame_main.pack()
    frame_left = tk.Frame(frame_main)
    frame_left.pack(side=tk.LEFT)
    frame_right = tk.Frame(frame_main)
    frame_right.pack(side=tk.RIGHT)
    cmap = tk.Canvas(frame_left, width=300, height=200)
    set_borders(cmap)
    set_random_walls(cmap)
    camera = Camera(cmap)
    cmap.pack()
    cview = tk.Canvas(frame_right, width=300, height=200, bg="Green")
    cview.pack()

    def tick():
        if keyboard.is_pressed("d"):
            camera.x += 1
        if keyboard.is_pressed("s"):
            camera.y += 1
        if keyboard.is_pressed("a"):
            camera.x -= 1
        if keyboard.is_pressed("w"):
            camera.y -= 1
        camera.update_rays()
        root.after(10, tick)

    tick()

    root.mainloop()
