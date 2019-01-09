import math
from math import cos, sin, atan

eps = 1e-14
sphere_radius = 1


class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return self.addition(other)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __str__(self):
        return "{}x {}y {}z".format(self.x, self.y, self.z)

    def __sub__(self, other):
        return self + other.scalar(-1)

    def rotation(self, alpha):
        from math import cos, sin
        x = self.x
        y = self.y
        self.x = x * cos(alpha) - y * sin(alpha)
        self.y = x * sin(alpha) + y * cos(alpha)
        return Vector(self.x, self.y, 0)

    def get_coordinates(self):
        return [self.x, self.y, self.z]

    def get_norm(self):
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def scalar(self, a):
        return Vector(a * self.x, a * self.y, a * self.z)

    def addition(self, vector):
        coordinates = vector.get_coordinates()
        return Vector(self.x + coordinates[0], self.y + coordinates[1], self.z + coordinates[2])

    def scalar_multiplication(self, vector):
        coordinates = vector.get_coordinates()
        return self.x * coordinates[0] + self.y * coordinates[1] + self.z * coordinates[2]

    def vector_multiplication(self, vector):
        coordinates = vector.get_coordinates()
        return Vector(self.y * coordinates[2] - coordinates[1] * self.z,
                      self.z * coordinates[0] - self.x * coordinates[2],
                      self.x * coordinates[1] - self.y * coordinates[0])

    def get_scalar_square(self):
        return self.scalar_multiplication(self)

    def dist(self, other):
        return (self - other).get_norm()

    def scalar_square_dist(self, other):
        return (self - other).get_scalar_square()

    def get_angle(self, other):
        return atan(self.vector_multiplication(other).get_norm() / self.scalar_multiplication(other))

    def change_len(self, k=1):
        d = self.get_norm()

        if abs(d) < eps:
            return Vector(0, 0, 0)

        return self.scalar(k).scalar(1/d)

    def get_perpendicular(self, norm):
        return self.vector_multiplication(norm)

    def rotate(self, angle, norm):
        other = self.get_perpendicular(norm)
        return self.scalar(cos(angle)) + other.scalar(sin(angle))

    def strictly_in_sphere(self, vec, r):
        val = r * r
        another_val = self.scalar_square_dist(vec)

        return another_val < val and abs(val - another_val) > eps

    def get_coordinates_in_plane_base(self, u, v):
        return Vector(self.scalar_multiplication(u), self.scalar_multiplication(v), 0)

    @staticmethod
    def get_decart_coordinates_from_spherical(alpha, delta):
        alpha = math.radians(alpha)
        delta = math.radians(delta)
        return Vector(sphere_radius * sin(delta) * cos(alpha),
                      sphere_radius * sin(delta) * sin(alpha), sphere_radius * cos(delta))

    @staticmethod
    def get_vector_len(p, q, h):
        angle = p.get_angle(q)
        return h / cos(angle)

    def get_coord_in_base(self, v, u, radius=1):
        w = self.change_len(self.get_vector_len(v, self, 1)) - v.change_len(1)
        return w.get_coordinates_in_plane_base(u.vector_multiplication(v), u).scalar(1 / radius)
