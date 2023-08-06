from tkinter import Tk, Canvas
import tkinter as tk

from phyengine.MathEngine import Vector
from phyengine import MathEngine as math_e
from phyengine import DynamicObjectManager as object_e
from phyengine import InputManager
from phyengine import DataEngine



def simple_update():
    return 0

class BasicWindow(Tk):
    def __init__(self, sizex, sizey, ping = 30, scale = 10):
        super().__init__()
        self.geometry("{}x{}".format(sizex, sizey))
        self.x, self.y = sizex, sizey
        self.resizable(False, False)
        self.title("Experiment")
        self.Objects: list[DynamicObject] = list()
        self.ping = ping
        self.scale = scale
        self.time = 0

        self.update = simple_update
        self.resume()
        self.paused = False
        def check_pause():
            if self.paused: self.resume()
            else: self.pause()
            self.paused = not self.paused
        self.bind('<Button-1>', lambda event: check_pause())
        
        self.canvas = Canvas(self)
        self.after(self.ping, lambda: self.after_())

    def start(self):
        self.canvas.pack(fill = tk.BOTH, expand = 1)
        self.mainloop()

    def pause(self):
        self.after_ = lambda: self.after(self.ping, self.after_)

    def resume(self):
        self.after_ = self.raw_update_w

    def InitObjects(self, *objects):
        self.Objects.extend(objects)

    @property
    def update(self):
        return self.raw_update_w

    @update.setter
    def update(self, fun):
        def wrap():
            fun()
            self.time += self.ping / 1000
            for obj in self.Objects:
                if isinstance(obj, DynamicObject): obj.raw_update_()
                elif isinstance(obj, DataEngine.RecordableValue): obj.record()
            self.after(self.ping, lambda: self.after_())
        self.raw_update_w = wrap

class DynamicObject:
    def __init__(self, window: BasicWindow, x, y, collidable = True,
     image: object_e.DO_Image = object_e.DO_Image.STANDART(),
     behaivour: object_e.DO_Behaivour = object_e.DO_Behaivour.STANDART()):
        self.window = window
        self.canvas = window.canvas
        self.x, self.y = x, y
        self.color = image.color
        self.collidable = collidable
        self.behaivour = behaivour
        self.r_image = image
        self.need_to_redraw = False
        self.r_velocity: Vector = None
        self.r_acceleration: Vector = None

        self.speed = Vector.ZERO()
        self.acceleration = Vector.ZERO()

        self.index = len(self.window.Objects) + 1
        self.update = simple_update

        self.create_image_func_ = None
        if image.shape_type == 'circle':
            self.create_image_func_ = self.canvas.create_oval
        elif image.shape_type == 'rectangle':
            self.create_image_func_ = self.canvas.create_rectangle
        self.object = -1
        self.draw()
        window.InitObjects(self)

    def __eq__(self, other):
        return self.index == other.index

    def __delitem__(self):
        self.canvas.delete(self.object)
        self.window.Objects.remove(self)

    def move(self, dx, dy):
        self.canvas.move(self.object, dx, dy)
        self.x += dx
        self.y += dy

    def stamp(self, color):
        self.create_image_func_(
        self.x - self.r_image.dx / 2,
        self.y - self.r_image.dy / 2,
        self.x + self.r_image.dx / 2,
        self.y + self.r_image.dy / 2,
        fill=color, width=0)

    def standart_move(self):
        self.r_velocity += self.r_acceleration * self.dt / 10
        self.move(*((self.r_velocity * self.dt / 10 + (self.r_acceleration * (self.dt / 10)**2)/2)
             * self.window.scale))

    def draw(self):
        if self.r_image.shape_type == 'circle':
            self.create_image_func_ = self.canvas.create_oval
        elif self.r_image.shape_type == 'rectangle':
            self.create_image_func_ = self.canvas.create_rectangle
        if self.object != -1: self.canvas.delete(self.object)
        self.object = self.create_image_func_(
        self.x - self.r_image.dx,
        self.y - self.r_image.dy,
        self.x + self.r_image.dx,
        self.y + self.r_image.dy,
        fill = self.r_image.color
        )

    def collide_with_borders(self):
        out_x = (self.r_image.dx <= self.x <= self.window.x - self.r_image.dx)
        out_y = (self.r_image.dy <= self.y <= self.window.y - self.r_image.dy)
        return (not out_x) or (not out_y)

    def collide_with(self, other):
        center_dist = math_e.math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
        if center_dist >= 2 * (max(self.image.dx, self.image.dy) + 
         max(other.image.dx, other.image.dy)):
            return False

        if abs(self.x - other.x) <= 1:
            return abs((self.y - other.y)) < self.image.dy + other.image.dy
        if abs(self.y - other.y) <= 1:
            return abs((self.x - other.x)) < self.image.dx + other.image.dx

        if not (self.collidable and other.collidable):
            return False

        try:
            if self.r_image.shape_type == 'circle':
                pow1 = 2
            else:
                pow1 = 30
            tan = (other.y - self.y) / (other.x - self.x)
            xb = 1 / (1 / pow(self.r_image.dx, pow1) + pow(tan / self.r_image.dy, pow1))
            yb = (1 - xb / pow(self.r_image.dx, pow1)) * pow(self.r_image.dy, pow1)
            border1 = math_e.math.sqrt(pow(xb, 2 / pow1) + pow(yb, 2 / pow1))
        
            if other.r_image.shape_type == 'circle':
                pow2 = 2
            else:
                pow2 = 30
            tan = (other.y - self.y) / (other.x - self.x)
            xb = 1 / (1 / pow(other.r_image.dx, pow2) + pow(tan / other.r_image.dy, pow2))
            yb = (1 - xb / pow(other.r_image.dx, pow2)) * pow(other.r_image.dy, pow2)
            border2 = math_e.math.sqrt(pow(xb, 2 / pow2) + pow(yb, 2 / pow2))

            return border1 + border2 > center_dist
        
        except TypeError:
            return False

    @property
    def image(self):
        return self.r_image

    @property
    def update(self):
        return self.raw_update_

    @property
    def dt(self):
        return self.window.ping / 1000

    @property
    def position(self):
        return Vector(self.x, self.y)
    
    @property
    def speed(self):
        return self.r_velocity

    @property
    def acceleration(self):
        return self.r_acceleration

    @image.setter
    def image(self, new_im: object_e.DO_Image):
        self.r_image = new_im
        self.need_to_redraw = True

    @position.setter
    def position(self, new_position: Vector):
        x, y = new_position
        self.canvas.move(self.object, x - self.x, y - self.y)
        self.x, self.y = x, y

    @speed.setter
    def speed(self, new_speed):
        self.r_velocity = new_speed

    @acceleration.setter
    def acceleration(self, new_acceleration: Vector):
        extra = Vector.ZERO()
        if self.behaivour.gravity > 0:
            extra += Vector(0, self.behaivour.gravity)
        if self.behaivour.air_friction > 0:
            extra += -self.r_velocity.unit * self.behaivour.air_friction * abs(self.r_velocity)**2
        self.r_acceleration = new_acceleration + extra
    
    @update.setter
    def update(self, fun):
        def wrap():
            fun()

            if self.behaivour.bounce_from_borders_friction >= 0:
                new_x, new_y = self.x, self.y
                if not (self.r_image.dx <= self.x <= self.window.x - self.r_image.dx):
                    self.r_velocity.x *= -self.behaivour.bounce_from_borders_friction
                    new_x = self.window.x / 2 + math_e.sgn(self.x - self.r_image.dx) * (self.window.x / 2 - self.r_image.dx)
                if not (self.r_image.dy <= self.y <= self.window.y - self.r_image.dy):
                    self.r_velocity.y *= -self.behaivour.bounce_from_borders_friction
                    new_y = self.window.y / 2 + math_e.sgn(self.y - self.r_image.dy) * (self.window.y / 2 - self.r_image.dy)
                self.position = new_x, new_y

            for i in range(10): self.standart_move()
            if self.need_to_redraw: self.draw()
            self.need_to_redraw = False

        self.raw_update_ = wrap