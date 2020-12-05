from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math


def lerp(x0, x1, amt):
    return (1 - amt) * x0 + amt * x1


def printText(x, y, r, g, b, string):
    glColor3f(r, g, b)
    glRasterPos2f(x, y)
    for char in string:
        glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(char))
