import pygame
import time
import numpy as np

# ----------------- Initialisation pygame font

pygame.font.init()


# ----------------- Assets des blocks

BLOCKS = {
    0:   "./crate_42.png",
    1:   "./crate_44.png",
}

# ----------------- Shape de la configuration

SHAPE = (50, 40)
CONFIGURATION = np.zeros(SHAPE)

# ----------------- Structure de John Horton Conway (1103 génération pour stabiliser)

CONFIGURATION[20:23, 21:22] = 1
CONFIGURATION[20, 22] = 1
CONFIGURATION[21, 20] = 1

WIDTH = (len(CONFIGURATION[0]))*10
HEIGHT = (len(CONFIGURATION))*10

# ----------------- Fonction qui verifie si un cellule survie


def survive(x, y, map):
    nb_cellule_around = 0
    legale_values = {-1, 0, 1}
    survive_value = {2, 3}
    illegale_value = {0, 1, len(map[0])-1, len(map)-1}

    for i in legale_values:
        for j in legale_values:
            if x not in illegale_value and y not in illegale_value and map[x+i][y+j] == 1:
                nb_cellule_around += 1

    nb_cellule_around -= 1

    return nb_cellule_around in survive_value

# ----------------- Fonction qui verifie si un cellule née


def create(x, y, map):
    nb_cellule_around = 0
    legale_values = {-1, 0, 1}
    illegale_value = {0, 1, len(map[0])-1, len(map)-1}

    for i in legale_values:
        for j in legale_values:
            if x not in illegale_value and y not in illegale_value and map[x+i][y+j] == 1:
                nb_cellule_around += 1

    return nb_cellule_around == 3


# ----------------- Fonction qui fait évoluer une configuration


def evolve(configuration):
    new_config = np.zeros(SHAPE)

    for row_index in range(len(configuration)):
        for col_index in range(len(configuration[0])):
            if configuration[row_index][col_index] == 0:
                if create(row_index, col_index, configuration):
                    new_config[row_index][col_index] = 1
            else:
                if survive(row_index, col_index, configuration):
                    new_config[row_index][col_index] = 1

    return new_config


# ----------------- Fonction qui fait le rendu de la configuration

def render_map(surface, configuration):
    for row_index, row in enumerate(configuration):
        for col_index, column in enumerate(row):
            position_x = col_index*8
            position_y = row_index*8
            asset = pygame.image.load(
                BLOCKS[column]).convert_alpha()

            asset = pygame.transform.scale(asset, (8, 8))

            surface.blit(asset, (position_x, position_y))


# ----------------- Initialisation surface de pygame

surface = pygame.display.set_mode((WIDTH, HEIGHT))  # pygame.RESIZABLE
surface.fill((255, 255, 255))

# ----------------- Max génération

MAX_GEN = 100
generation = 0


# ----------------- Programme

while generation <= MAX_GEN:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            generation = MAX_GEN

    render_map(surface, CONFIGURATION)
    CONFIGURATION = evolve(CONFIGURATION)
    generation += 1

    text = f"Steps : {generation}"
    text_font = pygame.font.SysFont("Comic Sans MS", 30)
    text_render = text_font.render(text, False, (0, 0, 0))
    surface.blit(text_render, (0, 0))

    pygame.display.flip()
