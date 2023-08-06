from pygame import Rect
from pygame.math import Vector2
from Physics2D import RigidBody2D


class physicsObject:
    def __init__(self, x: float, y: float, width: int, height: int, mass: int, name: str):
        """
        All Physics effected objects require x, y, width, height, name and mass.
        This is the bare bones values needed for physics calculations.
        Currently there is no support for objects other then rectangles.
        :param x:
        :param y:
        :param width:
        :param height:
        :param name:
        :param mass:
        """
        self.vector = Vector2(x, y)
        self.width = width
        self.height = height
        self.rect = Rect(self.vector.x, self.vector.y, self.width, self.height)
        self.name = name
        self.rb = RigidBody2D(int(mass))
