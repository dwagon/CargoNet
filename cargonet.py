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
        if n.demand.get('Stone',0)!=0 or n.demand.get('Timber',0)!=0:
            textobj=font.render("%d/%d" % (n.demand.get('Stone',0), n.demand.get('Timber',0)),1,(255,0,0))
            screen.blit(textobj,r)
            continue
        numcargo={'Stone':0, 'Timber':0}
        for c in wm.cargo:
            if c.loc==n:
                numcargo[c.label]+=1
        if numcargo['Stone']!=0 or numcargo['Timber']!=0:
            textobj=font.render("%d/%d" % (numcargo['Stone'], numcargo['Timber']),1,(0,0,255))
            screen.blit(textobj,r)
            continue

    drawText("Turn %d - Cargo %d" % (turn, len(wm.cargo)), font, screen, 0,0)

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
def loop(wm, screen, font, turn):
    for event in pygame.event.get():
        if event.type==QUIT:
            terminate()
    drawMap(wm, screen, font, turn)
    pygame.display.update()
    #waitForPlayerToPressKey()
    if random.randrange(4)==1:
        dst=wm.findGrassland()
        wm.demandTimber(dst, random.randrange(10))
    if random.randrange(4)==1:
        dst=wm.findGrassland()
        wm.demandStone(dst, random.randrange(10))
    src=wm.findMountain()
    wm.addStone(src)
    src=wm.findWoodland()
    wm.addTimber(src)
    wm.turn()

################################################################################
def main():
    pygame.init()
    screen=pygame.display.set_mode((windowWidth,windowHeight),DOUBLEBUF)
    wm=smap.Map(windowHeight/32,windowWidth/32)
    font = pygame.font.SysFont(None, 24)
    turn=0
    while True:
        turn+=1
        loop(wm, screen, font, turn)
        if turn==100:
            sys.exit(1)

################################################################################
if __name__=="__main__":
    import cProfile as profile
    profile.run("main()")
    main()

#EOF
