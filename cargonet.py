#!/usr/bin/env python

import sys
import pygame
import smap
import pygame.locals

windowWidth = 1024
windowHeight = 768


##########################################################################
##########################################################################
class Game(object):

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(
            (windowWidth, windowHeight), pygame.locals.DOUBLEBUF)
        self.wm = smap.Map(windowHeight / 32, windowWidth / 32)
        self.font = pygame.font.SysFont(None, 24)
        self.turn = 0
        self.wm.initialResources()

    ##########################################################################
    def drawMap(self):
        xsize = 32
        ysize = 32
        self.screen.fill((0, 0, 0))

        self.wm.draw(self.screen, xsize, ysize)
        self.drawText("Turn %d" % self.turn, 0, 0)

    ##########################################################################
    def waitForPlayerToPressKey(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.locals.QUIT:
                    self.terminate()
                if event.type == pygame.locals.KEYDOWN:
                    if event.key == pygame.locals.K_ESCAPE:  # pressing escape quits
                        self.terminate()
                    return

    ##########################################################################
    def terminate(self):
        pygame.quit()
        sys.exit()

    ##########################################################################
    def drawText(self, text, x, y, colour=(0, 0, 0)):
        textobj = self.font.render(text, 1, colour)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        self.screen.blit(textobj, textrect)

    ##########################################################################
    def loop(self):
        self.turn += 1
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                self.terminate()
        self.drawMap()
        pygame.display.update()
        # self.waitForPlayerToPressKey()
        self.wm.turn()


##########################################################################
def main():
    g = Game()
    while True:
        g.loop()

##########################################################################
if __name__ == "__main__":
    # import cProfile as profile
    # profile.run("main()")
    main()

# EOF
