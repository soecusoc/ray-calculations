# -*- coding: utf-8 -*-

import tkinter as tk
import numpy as np
import keyboard


class Camera:
    def __init__(self, parent, initial_x=None, initial_y=None, n_rays=36, fov=90, offset=0):
        if initial_x is None or initial_y is None:
            initial_x = int(int(parent.cget("width")) / 2)
            initial_y = int(int(parent.cget("height")) / 2)
        self.x = initial_x
        self.y = initial_y
        self.n_rays = n_rays
        self.parent = parent
        self.fov = fov / 360
        self.__offset = offset
        self.move = 0
        self.collision_info = np.zeros(n_rays)

    # Offset is always in the range [0, 1].
    @property
    def offset(self):
        return self.__offset

    @offset.setter
    def offset(self, off):
        off_int = int(off)
        self.__offset = off - off_int

    def find_ray_walls_collision_coordinates(self, theta, wall_coordinates):
        # The math heavy portion of the code.
        # The math is explained (poorly) in the file 'Ray_Wall_collision_calculations.txt'.

        x = self.x
        y = self.y
        # Eliminate numbers close to zero by rounding.
        # Numbers close to zero raise precision problems.
        a = np.round(np.cos(theta), 7)
        d = np.round(np.sin(theta), 7)

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

        if self.move:
            angle = 2 * np.pi * self.offset + (self.fov / 2) * 2 * np.pi + np.pi
            self.x += self.move * np.cos(angle)
            self.y += self.move * np.sin(angle)
            self.move = 0

        for i, angle in enumerate(self.offset * 2 * np.pi + np.linspace(0, self.fov * 2 * np.pi, self.n_rays, endpoint=False)):
            distance, closet_coordinates = self.find_ray_walls_collision_coordinates(angle, walls)
            self.collision_info[i] = distance
            # Closest_coordinates may be None (when the ray does not collide).
            # In that case, do not draw the ray (for now, maybe handle more elegantly later).
            try:
                self.parent.create_line(self.x, self.y, closet_coordinates[0], closet_coordinates[1], tags="rays")
            except TypeError:
                pass
        self.parent.pack()


class Pixel:
    def __init__(self, parent, x, y, size):
        self.parent = parent
        self.x = x
        self.y = y
        self.size = size
        self.__color = "#000000"
        self.idx = self.parent.create_rectangle(
            self.x, self.y, self.x + self.size, self.y + self.size, tag="pixel", width=0, fill=self.color
        )

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, rgb_triplet):
        # This property does not check for the numbers to be in range [0, 255].
        # This is because the PixelMap handles 8-bit integers.
        r = hex(rgb_triplet[0]).split('x')[-1].rjust(2, '0')
        g = hex(rgb_triplet[1]).split('x')[-1].rjust(2, '0')
        b = hex(rgb_triplet[2]).split('x')[-1].rjust(2, '0')
        self.__color = "#{}{}{}".format(r, g, b)

    def update(self):
        self.parent.itemconfig(self.idx, fill=self.color)


class PixelMap:
    def __init__(self, parent, height, width, pixel_size):
        self.parent = parent
        self.height = height
        self.width = width
        self.pixel_size = pixel_size
        self.map = np.zeros((self.height, self.width, 3), dtype=np.int8)
        self.pixels = self.init_pixels()

    def init_pixels(self):
        pixels = [None] * self.height * self.width
        for i in range(self.height):
            for j in range(self.width):
                pixel = Pixel(self.parent, j * self.pixel_size, i * self.pixel_size, self.pixel_size)
                pixel.color = self.map[i, j]
                pixel.update()
                pixel_idx = int(i * self.width + j)
                pixels[pixel_idx] = pixel
        self.parent.pack()
        return pixels

    def update(self):
        for i in range(self.height):
            for j in range(self.width):
                pixel_idx = int(i * self.width + j)
                self.pixels[pixel_idx].color = self.map[i, j]
                self.pixels[pixel_idx].update()
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
    # 4 pixels * 75 rays = 300 pixels.
    camera = Camera(cmap, n_rays=60)
    cmap.pack()

    cview = tk.Canvas(frame_right, width=300, height=200, bg="Green")
    pixel_map = PixelMap(cview, height=40, width=60, pixel_size=5)
    pixel_map.update()
    cview.pack()

    max_dist = 300
    def tick():
        if keyboard.is_pressed("d"):
            camera.offset += 0.02
        if keyboard.is_pressed("s"):
            camera.move = 3
        if keyboard.is_pressed("a"):
            camera.offset += -0.02
        if keyboard.is_pressed("w"):
            camera.move = -3
        camera.update_rays()
        pixel_map.map = np.dstack((np.ones((40, 60), dtype=np.int8), np.ones((40, 60), dtype=np.int8), 250 * np.ones((40, 60), dtype=np.int8)))
        for i, dist in enumerate(camera.collision_info):
            color = dist / max_dist
            color = int(np.round(color * 255))
            height = 40 - int(np.round(20 * color / 255))
            idx_list = np.arange(40 - height, height)
            pixel_map.map[idx_list, i, :] = (255 - color) * np.ones((len(idx_list), 3), dtype=np.int8)
        pixel_map.update()
        root.after(10, tick)

    tick()

    root.mainloop()
