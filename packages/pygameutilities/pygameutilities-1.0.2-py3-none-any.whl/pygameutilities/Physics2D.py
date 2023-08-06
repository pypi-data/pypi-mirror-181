import pygame.math
import json

Attractors = []

G = 6.6743 * (10 ** -11)


class RigidBody2D:
    def __init__(self, mass):
        self.mass = mass

    def addForce(self, initialVector, moveTowards, force):
        """Takes in initialVector and forceVector and returns Vector2 of initalVector moved towards a vector by a force"""
        return initialVector.move_towards(moveTowards.xy, force)


class Gravity:
    def __init__(self, autoGenerateGround=True, generateRadius=10000, windowHeight=900, defaultY=None) -> None:
        self.groundVectors = {}
        self.autoGenerateGround = autoGenerateGround
        self.generateRadius = generateRadius
        self.windowHeight = windowHeight
        if defaultY:
            self.defaultY = defaultY
        else:
            self.defaultY = self.windowHeight

    def findGround(self, win, objx, listOfGround):
        # for all positions, get ground y value, calculate before game runs
        # store in dict
        # access for gravity
        # random comment
        for y in range(self.windowHeight):
            for rect in listOfGround:
                #print(objx, y)
                pygame.draw.rect(win, (0, 0, 255), pygame.Rect(objx, y, 10, 1))
                if rect.collidepoint(objx, y):
                    self.groundVector[objx] = y

    def precomputeGround(self, groundobjects):
        try:
            with open("groundVectors.json") as f:
                self.groundVectors = json.load(f)
        except FileNotFoundError:
            for rect in groundobjects:
                for x in range(-self.generateRadius, self.generateRadius):
                    for y in range(self.windowHeight):
                        if rect.collidepoint(x, y):
                            self.groundVectors[str(x)] = y
                        else:
                            self.groundVectors[str(x)] = self.defaultY
            with open("groundVectors.json", "w+") as f:
                json.dump(self.groundVectors, f)

    def update(self, smallMass: float, largeMass: float, smallVector: pygame.math.Vector2, largeVector: pygame.math.Vector2 = pygame.math.Vector2()) -> pygame.math.Vector2:
        if not self.autoGenerateGround:
            distance = smallVector.distance_to(largeVector)
        else:
            distance = smallVector.distance_to(pygame.math.Vector2(smallVector.x, self.groundVectors[str(smallVector.x)[:-2]]))
        try:
            # f = G * (m1 * m2 / d^2)
            force = G * ((smallMass * largeMass) / distance)
            # f = GM / d^2
            # force = (G * largeMass) / distance
        except ZeroDivisionError:
            force = 0
        if not self.autoGenerateGround:
            return smallVector.move_towards(largeVector, force)
        else:
            return smallVector.move_towards(pygame.math.Vector2(smallVector.x, self.groundVectors[str(smallVector.x)[:-2]]), force)

