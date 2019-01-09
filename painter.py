
import pygame
from pygame import *

aqua = (0, 255, 255)   # морская волна
black = (0,   0,   0)   # черный
blue = (0,   0, 255)   # синий
white_blue = (128, 208, 234)
fuchsia = (255,   0, 255)   # фуксия
gray = (128, 128, 128)   # серый
green = (0, 128,   0)   # зеленый
lime = (0, 255,   0)   # цвет лайма
maroon = (128,   0,   0)   # темно-бордовый
navy_blue = (0,   0, 128)   # темно-синий
olive = (128, 128,   0)   # оливковый
purple = (128,   0, 128)   # фиолетовый
red = (255,   0,   0)   # красный
silver = (192, 192, 192)   # серебряный
teal = (0, 128, 128)   # зелено-голубой
white = (255, 255, 255)   # белый
yellow = (255, 255,   0)   # желтый
yellow_white = (251, 248, 167)
light_orange = (238, 203, 88)
orange_red = (245, 152, 25)

colors = {
    "O": blue,
    "B": white_blue,
    "A": white,
    "F": yellow_white,
    "G": yellow,
    "K": light_orange,
    "M": orange_red,
    "C": red,
    "S": orange_red
}


class PySkyPainter:
    def __init__(self, sky):
        self.sky = sky

    def draw_stars(self, screen):
        for star in filter(lambda x: x.is_bright(self.sky.r), self.sky.get_stars()):
            pygame.draw.circle(screen, colors[star.stellar_classification], (int(star.x), int(star.y)),
                               int(star.r(self.sky.r)), int(star.r(self.sky.r)))

    def draw_labels(self, labels, screen):
        for label in labels:
            fontObj = pygame.font.Font('freesansbold.ttf', 12)
            textSurfaceObj = fontObj.render(label.name, True, white)
            textRectObj = textSurfaceObj.get_rect()
            textRectObj.center = (label.x, label.y)
            screen.blit(textSurfaceObj, textRectObj)

    def draw_selected_star(self, screen):
        fontObj = pygame.font.Font('freesansbold.ttf', 12)

        if self.sky.selected_star is not None:
            textSurfaceObj = fontObj.render('selected star apparent magnitude: {}, stellar classification: {}'.format(
                self.sky.selected_star.apparent_magnitude,
                self.sky.selected_star.stellar_classification), True, white)
        else:
            textSurfaceObj = fontObj.render('No star selected', True, white)

        timeSurfaceObj = fontObj.render('current time: {} hours, {} minutes'.format(
            self.sky.time.hour,
            self.sky.time.minute), True, white)

        time_rect = timeSurfaceObj.get_rect()
        time_rect.center = (700, 50)

        textRectObj = textSurfaceObj.get_rect()
        textRectObj.center = (660, 500)
        screen.blit(textSurfaceObj, textRectObj)
        screen.blit(timeSurfaceObj, time_rect)

    def run(self, width=880, height=550):
        pygame.init()
        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Py-sky")
        bg = Surface((width, height))

        while 1:
            for e in pygame.event.get():
                if e.type == QUIT:
                    return

                if e.type == KEYDOWN:
                    if e.key == K_l:
                        self.sky.print_label()

                    if e.key == K_LEFT:
                        self.sky.rotate_sky(0.1, 0)

                    if e.key == K_RIGHT:
                        self.sky.rotate_sky(-0.1, 0)

                    if e.key == K_UP:
                        self.sky.rotate_sky(0, 0.1)

                    if e.key == K_DOWN:
                        self.sky.rotate_sky(0, -0.1)

                    if e.key == K_e:
                        self.sky.rotate_sky_on_axis(0.1)

                    if e.key == K_q:
                        self.sky.rotate_sky_on_axis(-0.1)

                    if e.key == K_EQUALS:
                        self.sky.increase_time(15)

                    if e.key == K_MINUS:
                        self.sky.decrease_time(15)

                if e.type == MOUSEBUTTONDOWN:
                    if e.button == 4:
                        self.sky.zoom(1)
                    if e.button == 5:
                        self.sky.zoom(-1)

                    pos = pygame.mouse.get_pos()
                    self.sky.draw_point_at(pos)

            screen.blit(bg, (0, 0))

            self.draw_stars(screen)
            self.draw_labels(self.sky.get_labels(), screen)
            self.draw_selected_star(screen)

            pygame.display.update()


def paint(sky):
    window = PySkyPainter(sky)

    window.run()

