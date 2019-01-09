import math
from Vector import Vector
from star import Star
import datetime
sphere_radius = 1
eps = 1e-4

North = Vector(0, 0, 1)
zoom_const = 0.85
rad_in_minute = 2 * math.pi / 1440


class Label:
    def __init__(self, vector, label_name):
        self.name = label_name
        self.vector = vector

    @property
    def x(self):
        return self.vector.x

    @property
    def y(self):
        return self.vector.y


class Sky:
    def __init__(self, direction, top, stars, width=500, height=500, time='00:00'):
        self.direction = direction
        self.top = top
        self.mouse_pos_point = None
        self._selected_star = None
        val = time.split(':')
        self.current_date_time = datetime.datetime(2000, 1, 1, int(val[0]), int(val[1]))

        w = self.top.vector_multiplication(self.direction)
        value = self.direction.vector_multiplication(w)
        self.top = value.change_len(1)

        self.stars = stars
        self.size = Vector(width, height, 0)
        self.r = 1

        self.cached = False
        self.cache = []

    @property
    def width(self):
        return self.size.x

    @property
    def height(self):
        return self.size.y

    @property
    def selected_star(self):
        return self._selected_star

    @property
    def time(self):
        return self.current_date_time

    @property
    def time_angle(self):
        return (60 * self.current_date_time.hour + self.current_date_time.minute) * rad_in_minute

    def increase_time(self, value=1):
        if self.current_date_time.minute + value > 59:
            if self.current_date_time.hour == 23:
                self.current_date_time = datetime.datetime(2000, 1, 1, 0, (self.current_date_time.minute + value) % 60)
                return
            self.current_date_time = datetime.datetime(2000, 1, 1, self.current_date_time.hour + 1,
                                                       (self.current_date_time.minute + value) % 60)
            return

        self.current_date_time = datetime.datetime(2000, 1, 1, self.current_date_time.hour,
                                                   (self.current_date_time.minute + value) % 60)
        self.cached = False

    def decrease_time(self, value=1):
        if self.current_date_time.minute - value < 0:
            if self.current_date_time.hour == 0:
                self.current_date_time = datetime.datetime(2000, 1, 1, 23, (self.current_date_time.minute - value) % 60)
                return
            self.current_date_time = datetime.datetime(2000, 1, 1, self.current_date_time.hour - 1,
                                                       (self.current_date_time.minute - value) % 60)
            return

        self.current_date_time = datetime.datetime(2000, 1, 1, self.current_date_time.hour,
                                                   (self.current_date_time.minute - value) % 60)
        self.cached = False

    def get_stars(self):
        if self.cached:
            for each in self.cache:
                yield each
        else:
            self.cache = []

            for star in self.stars:
                star = star.rotate(self.time_angle)
                s = star.get_changed_coord(self.direction, self.top, self.r)

                if s is not None:
                    if self.mouse_pos_point is not None:
                        if (self.resize_vector(s.vector) - self.mouse_pos_point).get_norm() < 3:
                            self._selected_star = s

                    self.cache.append(self.resize(s))
                    yield self.cache[-1]
            self.cached = True

    def resize_vector_to_border(self, vector):
        angle = abs(math.pi / 4 - math.atan2(vector.y, vector.x))

        return vector.scalar(1 / math.cos(angle)).scalar(1 / math.exp(self.r))

    def resize_vector(self, vector):
        center = self.size.scalar(1/2)
        vector = vector.scalar(min(center.x, center.y))
        vector += center
        return vector

    def resize(self, star):
        center = self.size.scalar(1/2)
        star.vector = star.vector.scalar(min(center.x, center.y))
        star.vector += center
        return star

    @staticmethod
    def rotate(v, u, dx, dy):
        x_angle = 2 * math.asin(dx / 2)
        y_angle = 2 * math.asin(dy / 2)
        v = v.rotate(x_angle, u)
        w = v.vector_multiplication(u)
        return v.rotate(y_angle, w), u.rotate(y_angle, w)

    def rotate_sky(self, dx, dy):
        delta_x_angle = -dx * self.r
        delta_y_angle = -dy * self.r

        self.direction, self.top = self.rotate(self.direction, self.top,  -delta_x_angle,  -delta_y_angle)

        self.top = self.top.change_len(1)
        self.direction = self.direction.change_len(1)

        # labs = self.get_labels()
        # if len(labs):
        #     self.rotate_sky_on_axis(-Vector.get_angle(labs[1].vector, Vector(135.0, 275.0, 0.0)))

        self.mouse_pos_point = None
        self._selected_star = None
        self.cached = False

    def rotate_sky_on_axis(self, angle):
        self.top = self.top.rotate(angle, self.direction)
        self.cached = False

    def draw_point_at(self, coordinates):
        self.mouse_pos_point = Vector(coordinates[0], coordinates[1], 0)
        self.cached = False

    def on_axis(self):
        return abs(abs(self.direction.z) - 1) < eps

    def get_north(self):
        def sign(x):
            return 0 if x == 0 else 1 if x > 0 else -1

        return North.get_coord_in_base(self.direction, self.top).change_len(sign(North.scalar_multiplication(
            self.direction)))

    def zoom(self, value):
        self.r *= zoom_const ** value
        self.r = min(1, self.r)
        self.cached = False

    def get_labels(self):

        def get_label_names():
            yield "North"
            yield "West"
            yield "South"
            yield "East"

        if self.on_axis():
            return []

        labels = []
        prev = self.get_north()
        for name in get_label_names():
            labels.append(Label(prev, name))
            prev = labels[-1].vector.get_perpendicular(North)

        center = self.size.scalar(1/2)
        return [Label(label.vector.scalar(min(center.x, center.y) - 10) + center, label.name) for label in labels]

    def print_label(self):
        labs = self.get_labels()
        print(Vector.get_angle(labs[1].vector, Vector(135.0, 275.0, 0.0)))
