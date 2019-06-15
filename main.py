# -*- coding: utf-8 -*-

import tkinter as tk
import numpy as np
import keyboard


class Camera:
    def __init__(self, parent, initial_x=None, initial_y=None, n_rays=36):
        if initial_x is None or initial_y is None:
            initial_x = int(int(parent.cget("width")) / 2)
            initial_y = int(int(parent.cget("height")) / 2)
        self.x = initial_x
        self.y = initial_y
        self.n_rays = n_rays
        self.parent = parent

    def find_ray_walls_collision_coordinates(self, theta, wall_coordinates):
        # The math heavy portion of the code.
        # The math is explained (poorly) in the file 'Ray_Wall_collision_calculations.txt'.

        x = self.x
        y = self.y
        a = np.cos(theta)
        d = np.sin(theta)

        smallest_distance = np.inf
        closest_coordinates = None
        # Handy unpacking for each wall.
        for x1, y1, x2, y2 in wall_coordinates:
            b = x1 - x2
            c = x - x1
            e = y1 - y2
            f = y - y1
            # Since ||(cos(theta),sin(theta)|| == 1, variable t is the distance from the camera to the collision.
            if d * b - a * e != 0 and a != 0:
                s = (a * f - c * d) / (d * b - a * e)
                t = -(s * b + c) / a
            elif d * b - a * e == 0:
                # Ray and line segment (wall) are parallel.
                s = np.inf
                # The logic is equivalent to s = -np.inf .
                t = np.inf
            else:
                s = (a * f - c * d) / (d * b - a * e)
                t = -(s * e + f) / d
            if 0 <= t < smallest_distance and 0 <= s <= 1:
                # The coordinates can be found from the equation pair.
                # Let's use the line segment to avoid expensive trigonometric calculations.
                # This means that the vector is (1-s)(x1,y1)+s(x2,y2).
                smallest_distance = t
                closest_coordinates = [
                    int(np.round((1 - s) * x1 + s * x2)),
                    int(np.round((1 - s) * y1 + s * y2))
                ]
        return smallest_distance, closest_coordinates

    def update_rays(self):
        wall_indices = self.parent.find_withtag("walls")
        # Fill walls-array. Get coordinates from the parent.
        walls = np.zeros((len(wall_indices), 4))
        for idx, wall_idx in enumerate(wall_indices):
            # returns a list: [x1, y1, x2, y2]
            walls[idx] = self.parent.coords(wall_idx)
        for idx in self.parent.find_withtag("rays"):
            self.parent.delete(idx)
        for i, angle in enumerate(np.linspace(0, 2 * np.pi, self.n_rays, endpoint=False)):
            # TODO: Fix the bug from rays going straight up or down.  --Preferred action--
            # TODO: OR use configurations, that do not create vertical rays
            # TODO: (Values 2^k * n  with k >= 2 and n >= 1 for self.n_rays).
            # Has something to do with angles 90 degrees and 270 degrees:
            # In these cases, cos(theta) = 0.
            distance, closet_coordinates = self.find_ray_walls_collision_coordinates(angle, walls)
            # closest_coordinates may be None (when the ray does not collide).
            # In that case, do not draw the ray (for now, maybe handle more elegantly later).
            try:
                self.parent.create_line(self.x, self.y, closet_coordinates[0], closet_coordinates[1], tags="rays")
            except TypeError:
                pass
        self.parent.pack()


def set_borders(parent):
    x_max = parent.cget("width")
    y_max = parent.cget("height")
    parent.create_line(1, 1, x_max, 1, tags="walls", width=1)
    parent.create_line(1, 1, 1, y_max, tags="walls", width=1)
    parent.create_line(1, y_max, x_max, y_max, tags="walls", width=1)
    parent.create_line(x_max, 1, x_max, y_max, tags="walls", width=1)
    parent.pack()


def set_random_walls(parent, n_walls=5, seed=None):
    prng = np.random.RandomState(seed)
    for i in range(n_walls):
        x1 = int(prng.randint(1, 300, 1)[0])
        x2 = int(prng.randint(1, 300, 1)[0])
        y1 = int(prng.randint(1, 200, 1)[0])
        y2 = int(prng.randint(1, 200, 1)[0])
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
    set_random_walls(cmap, n_walls=5, seed=27)
    # Values 2^k * n for n_rays with k >= 2 and n >= 1 cause a see-through-walls bug.
    camera = Camera(cmap, n_rays=64)
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
