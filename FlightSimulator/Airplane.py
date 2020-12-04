from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
# from OBJFileLoader import *
from ply import *


class Airplane():
    def __init__(self):
        self.model = PlyReader("models/airplane/airplane.ply")

        self.x = 0
        self.y = 0
        self.z = 0

        self.xV = 0.1
        self.yV = 0
        self.zV = -0.1

        self.xRot = 0
        self.yRot = 0
        self.zRot = 0

        self.xRotV = 0.5
        self.yRotV = 0.5
        self.zRotV = 0.1

    def command(self, key):

        # ESQUERDA
        if key == 100:
            self.xRot += self.xRotV
            self.yRot += self.yRotV
            # self.zRot -= self.zRotV
            # self.x += self.xV

        # DIREITA
        elif key == 102:
            self.xRot -= self.xRotV
            self.yRot -= self.yRotV
            # self.zRot -= self.zRotV
            # self.x -= self.xV
            # yrot += dy

        # CIMA
        elif key == 101:
            self.zRot += self.zRotV

            # # BAIXO
        elif key == 103:
            self.zRot -= self.zRotV

    def updatePos(self):
        # self.x += self.xV
        # self.y += self.yV
        self.z += self.zV

        # self.xRot += self.xRotV
        # self.yRot += self.yRotV
        # self.zRot += self.zRotV

    def draw(self):
        glPushMatrix()
        # Rotacionando o modelo pq ele vem rodado
        glRotatef(-90, 0, 1, 0)

        glRotatef(self.xRot, 1, 0, 0)
        glRotatef(self.yRot, 0, 1, 0)
        glRotatef(self.zRot, 0, 0, 1)

        # Fazendo ele voar
        glTranslatef(self.z, self.y, self.x)
        self.model.draw()
        glPopMatrix()
