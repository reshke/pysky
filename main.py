
from painter import paint
from sys import argv
from sky import Sky
import math
from Vector import Vector
from dataParser import DataParser
import argparse


def get_parser():
    parser = argparse.ArgumentParser(prog="main")

    parser.add_argument('-V', '--vos', type=str,
                        default="00:00:00.0")
    parser.add_argument('-S', '--skl', type=str,
                        default="00:00:00.0")
    parser.add_argument('-T', '--time', type=str,
                        default='00:00')

    return parser


def main():
    parser = get_parser()
    options = parser.parse_args(argv[1:])
    alpha = DataParser.parse_hours(options.vos)
    theta = 90 - DataParser.parse_angle(options.skl)
    time = options.time

    sky = Sky(Vector(0, 0, 1), Vector(1, 0, 0), DataParser().get_stars(), 800, 550, time=time)
    #sky.rotate_sky(math.radians(alpha), math.radians(theta))
    paint(sky)


if __name__ == '__main__':
    main()

