from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
# from OBJFileLoader import *
from ply import *
import math


class Airplane():
    def __init__(self):
        self.model = PlyReader("models/airplane/airplane.ply")

        self.modelOffset = -7

        self.x = 0
        self.y = 0
        self.z = 0

        self.prevX = 0
        self.prevY = 0
        self.prevZ = 0

        self.xV = .7
        self.yV = 0
        self.zV = -.1

        self.xRot = 0
        self.yRot = 0
        self.zRot = 0

        self.xRotV = 1.5
        self.yRotV = 1
        self.zRotV = 1

    def command(self, key):
        # SETA ESQUERDA
        if key == 100:
            self.xRot += self.xRotV

        # SETA DIREITA
        elif key == 102:
            self.xRot -= self.xRotV

        # SETA CIMA
        elif key == 101:
            self.zRot += self.zRotV

        # SETA BAIXO
        elif key == 103:
            self.zRot -= self.zRotV

        # PARA FRENTE
        elif key == b'f':
            self.x -= self.xV

        # PARA TRAS
        elif key == b'g':
            self.x += self.xV

    def updatePos(self):
        pass
        # self.x += self.xV
        # self.y += self.yV
        # self.z += self.zV

        # self.xRot += self.xRotV
        # self.yRot += self.yRotV
        # self.zRot += self.zRotV

    def draw(self):
        glPushMatrix()

        glTranslatef(self.x, self.y, self.z)

        # ROTACIONANDO
        glRotatef(self.xRot, 1, 0, 0)
        glRotatef(self.yRot, 0, 1, 0)
        glRotatef(self.zRot, 0, 0, 1)

        glTranslatef(0, 0, 0)

        glRotatef(self.xRot, 1, 0, 0)
        glRotatef(self.yRot, 0, 1, 0)
        glRotatef(self.zRot, 0, 0, 1)

        glTranslatef(self.x, self.y, self.z)

        # glRotatef(self.xRot, 1, 0, 0)
        # glRotatef(self.yRot, 0, 1, 0)
        # glRotatef(self.zRot, 0, 0, 1)

        # glTranslatef(self.x, self.y, self.z)

        # glTranslatef(self.x, self.y, self.z)

        self.model.draw()
        glPopMatrix()
