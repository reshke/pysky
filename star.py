import math
from Vector import Vector
North = Vector(0, 0, 1)

R = 1


class Star:
    def __init__(self, vector, apparent_magnitude, stellar_classification, r=1, letter=None):
        self.vector = vector
        self._r = r
        self.apparent_magnitude = apparent_magnitude
        self.letter = letter
        self.stellar_classification = stellar_classification

    @property
    def x(self):
        return self.vector.x

    @property
    def y(self):
        return self.vector.y

    def current_visible_magnitude(self, r=1):
        return self.apparent_magnitude + 5 * math.log(r, 10)

    def r(self, r):
        return min(6.0, 6 / math.exp(self.current_visible_magnitude(r) / 6.0)**2)

    @staticmethod
    def get_height(r, d):
        return R * (R * R + d * d - r * r) / (2 * R * d)

    def rotate(self, angle):
        h = self.get_height(self.vector.dist(North), self.vector.get_norm()) / R * self.vector.get_norm()
        s = North.change_len(h)
        return self.change_counter_vector(s + (self.vector - s).rotate(angle, North))

    def is_bright(self, r):
        return self.current_visible_magnitude(r) < 4

    def change_counter_vector(self, vector):
        return Star(vector, self.apparent_magnitude, self.stellar_classification)

    def change_counter_vector_with_function(self, f):
        self.vector = f(self.vector)

    def in_borders(self, v, r):
        return self.vector.strictly_in_sphere(v, r)

    def get_changed_coord(self, v, u, r):
        if not self.in_borders(v, r):
            return None

        return self.change_counter_vector(self.vector.get_coord_in_base(v, u, r))
