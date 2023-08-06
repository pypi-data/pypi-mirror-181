from pygame.sprite import collide_rect
import pygame


def detectCollision(obj: pygame.Rect, listToCheck: list[pygame.Rect]) -> list[bool, pygame.Rect]:
    for rect in listToCheck:
        if pygame.sprite.collide_rect(obj, rect):
            return True, rect
    return False, None