#!/opt/local/bin/python2.7

import sys
import pygame
import random
from pygame.locals import *
import smap

windowWidth=1024
windowHeight=768

################################################################################
def drawMap(wm, screen, font, turn):
    xsize=32
    ysize=32
    screen.fill((0,0,0))

    for n in wm.nodes.values():
        r=pygame.Rect(n.x*xsize,n.y*ysize,xsize,ysize)
        screen.blit(n.image,r)
        if n.demand:
            textobj=font.render("%d" % n.demand,1,(255,0,0))
            screen.blit(textobj,r)
        elif n.amount:
            textobj=font.render("%d" % n.amount,1,(0,0,255))
            screen.blit(textobj,r)
        else:
            if n.transport:
                textobj=font.render("%d" % n.floodval,1,(255,255,255))
                screen.blit(textobj,r)
    drawText("Turn %d" % turn, font, screen, 0,0)

################################################################################
def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # pressing escape quits
                    terminate()
                return

################################################################################
def terminate():
    pygame.quit()
    sys.exit()

################################################################################
def drawText(text, font, surface, x, y, colour=(0,0,0)):
    textobj = font.render(text, 1, colour)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

################################################################################
def loop(wm, screen, font, turn, src):
    for event in pygame.event.get():
        if event.type==QUIT:
            terminate()
    drawMap(wm, screen, font, turn)
    pygame.display.update()
    #waitForPlayerToPressKey()
    if random.randrange(5)==1:
        dst=findGrassland(wm)
        dst.demand=random.randrange(15)
    src.amount+=1
    wm.turn()

################################################################################
def findGrassland(wm):
    count=100
    while True:
        count-=1
        x=random.randrange(wm.width)
        y=random.randrange(wm.height)
        if wm[(x,y)].__class__.__name__=='Grassland':
            return wm[(x,y)]
        if not count:
            sys.stderr.write("Couldn't find any grassland\n")
            return None
    
################################################################################
def main():
    pygame.init()
    screen=pygame.display.set_mode((windowWidth,windowHeight),DOUBLEBUF)
    wm=smap.Map(windowHeight/32,windowWidth/32)
    font = pygame.font.SysFont(None, 24)
    src=findGrassland(wm)
    src.amount=8
    src=findGrassland(wm)
    src.amount=8
    dst=findGrassland(wm)
    dst.demand=10
    dst=findGrassland(wm)
    dst.demand=5
    turn=0
    while True:
        turn+=1
        loop(wm, screen, font, turn, src)
        sys.stderr.write("turn=%d\n" % turn)

################################################################################
if __name__=="__main__":
    import cProfile as profile
    profile.run("main()")
    #main()

#EOF
