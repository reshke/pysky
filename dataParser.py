import os
import re
from star import Star
from Vector import Vector
sphere_radius = 1


class DataParser:
    @staticmethod
    def parse_hours(s):
        data = re.split(r'[^\d+-]', s)
        line = list(map(int, data))
        return (line[0] + (line[1] + (line[2] + line[3] / 10) / 60) / 60) * 15

    @staticmethod
    def parse_angle(s):
        data = re.split(r'[^\d+-]', s)
        line = list(map(int, filter(lambda x: len(x) > 0, data)))
        return line[0] + (line[1] + line[2] / 60) / 60

    def parse_line(self, line):
        alpha = self.parse_hours(line[4:14].replace(' ', '0'))
        delta = self.parse_angle(line[16:24].replace(' ', '0'))

        stellar_classification = line[49]
        let = line[103:106]
        if let[0] == ' ':
            let = None
        apparent_magnitude = float(line[41:46].replace(' ', '0'))

        if line[15] == '-':
            delta = -delta

        delta = 90 - delta
        return Star(Vector.get_decart_coordinates_from_spherical(alpha, delta),
                    apparent_magnitude,
                    stellar_classification,
                    letter=let)

    def get_stars(self):
        stars = []
        files = os.listdir('data/')
        for file in files:
            with open('data/' + file) as f:
                for l in f.readlines():
                    stars.append(self.parse_line(l))

        return stars


