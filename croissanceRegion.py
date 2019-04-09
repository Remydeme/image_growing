# -*- coding: utf-8 -*-

import cv2
import numpy as np
import random

def square(dim):
    return np.ones(shape=(dim, dim))


def traingle():
    return [
        [0, 0, 0, 1],
        [0, 0, 1, 1],
        [0, 1, 1, 1],
        [1, 1, 1, 1]
    ]

def generateSeed(height, width, img):
    x = random.randint(0, width - 1)
    y = random.randint(0, height - 1)
    pix = img[x, y]
    while (pix == 0):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        pix = img[x, y]
    seed = (x,y)
    return seed

def getHeightNeighborhood(x, y, shape):
    """ This function get the coordinate of the heights pixel arounds the pixel (x, y) and return those coordinates"""
    out = []
    maxx = shape[1]-1
    maxy = shape[0]-1

    # on traite le pixel du haut situé à gauche
    outx = min(max(x-1,0),maxx)
    outy = min(max(y-1,0),maxy)
    out.append((outx,outy))

    #on traite le pixel du haut
    outx = x
    outy = min(max(y-1,0),maxy)
    out.append((outx,outy))

    # on traite le pixel du haut situé à gauche
    outx = min(max(x+1,0),maxx)
    outy = min(max(y-1,0),maxy)
    out.append((outx,outy))

     # on traite le pixel du haut situé à gauche

    outx = min(max(x-1,0),maxx)
    outy = y
    out.append((outx,outy))

    # on traite le pixel du haut situé à gauche
    outx = min(max(x+1,0),maxx)
    outy = y
    out.append((outx,outy))

    # on traite le pixel du haut situé à gauche
    outx = min(max(x-1,0),maxx)
    outy = min(max(y+1,0),maxy)
    out.append((outx,outy))

    #bottom center
    outx = x
    outy = min(max(y+1,0),maxy)
    out.append((outx,outy))

    #bottom right
    outx = min(max(x+1,0),maxx)
    outy = min(max(y+1,0),maxy)
    out.append((outx,outy))

    return out

def region_growing(img, seed):
    """
        La fonction prend l'image d'origin en paramètre ainsi qu'une seed qui correspond au pixel à un pixel choisi de manière
        aléatoire sur l'image avec la souri.
        Le pixel passé à une valeur supérieur à zéro.
        La list contient tous les pixels que notre fonction getHeightNeighborhood nous retourne. Ces pixels correspondent aux
        8 pixels voisins à notre pixel.
        Le premier pixel de la liste correspond à la seed. par la suite nous ajouterons tous les pixels voisins à chaque itérations et nous
        supprimerons le pixel le plus ancien.

        Nous avons une liste processed qui contient les pixel que l'on à déjà parcourus. Si un pixel à déja été visité il n'est pas ajouté
        à notre liste. Une fois que nous aurons parcourus tous les pixels voisins qui ont une valeur différent de 1 nous nous arrêterons.

    """
    list = []
    outimg = np.zeros_like(img) # on cree un matrice pleine de zero de la taille de l'image
    list.append((seed[0], seed[1])) # on ajoute les coordonees sur le quel on a clique a notre liste de pixel
    processed = []
    while(len(list) > 0):
        pix = list[0]
        outimg[pix[0], pix[1]] = 255 # on met notre pixel a la valeur max 255
        for coord in getHeightNeighborhood(pix[0], pix[1], img.shape):
            if img[coord[0], coord[1]] != 0:
                outimg[coord[0], coord[1]] = 255
                if not coord in processed: # si le pixel n'a pas encore été traite on l'ajoute a la liste des pixels
                    list.append(coord)
                processed.append(coord) # ajoute a la liste des pixels traité
        list.pop(0) # on retire le premier pixel qui à été ajouté à notre liste
        cv2.imshow("progress",outimg) # on affiche l'image
        cv2.waitKey(1) # empeche la fermeture de la fenetre
    return outimg # on retourne notre image segmenté

def on_mouse(event, x, y, flags, params):
    """ Cette fonction détecte un clique à la sourie"""
    if event == cv2.EVENT_LBUTTONDOWN:
        print ('Seed: ' + str(x) + ', ' + str(y), img[y,x])
        clicks.append((y,x))

if __name__ == "__main__":
    clicks = []
    image = cv2.imread('lena.bmp', 0)
    ret, img = cv2.threshold(image, 130, 255, cv2.THRESH_BINARY)
    cv2.namedWindow('Input')
    cv2.imshow('Input', img)
    seed = generateSeed(image.shape[1], image.shape[0], img)
    out = region_growing(img, seed)
    cv2.imshow('Region Growing', out)
    cv2.waitKey()
    cv2.destroyAllWindows()
