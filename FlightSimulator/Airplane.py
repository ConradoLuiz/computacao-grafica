from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
# from OBJFileLoader import *
from ply import *
import math


class Airplane():
    def __init__(self):
        self.model = PlyReader("models/airplane/airplane.ply", frontFace=GL_CW)

        self.debug = False

        self.modelOffset = -7

        self.forwardX = 0
        self.forwardY = 0
        self.forwardZ = 0

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

        if key == b'p':
            self.debug = not self.debug

        # SETA ESQUERDA
        if key == 100:
            self.xRot += self.xRotV
            self.forwardZ = math.cos(self.xRot)
            self.forwardY = math.sin(-self.xRot)

        # SETA DIREITA
        elif key == 102:
            self.xRot -= self.xRotV
            self.forwardZ = math.cos(self.xRot)
            self.forwardY = math.sin(-self.xRot)

        # SETA CIMA
        elif key == 101:
            self.zRot += self.zRotV
            self.forwardY = math.cos(self.zRot)
            self.forwardX = math.sin(self.zRot)

        # SETA BAIXO
        elif key == 103:
            self.zRot -= self.zRotV
            self.forwardY = math.cos(self.zRot)
            self.forwardX = math.sin(self.zRot)

        # PARA FRENTE
        elif key == b'f':
            self.x -= self.forwardX * self.xV

        # PARA TRAS
        elif key == b'g':
            self.x += self.forwardX * self.xV

    def defineMaterial(self):
        mat_ambient = (1, 1, 1, 1.0)
        mat_diffuse = (196/255, 202/255, 206/255, 1.0)
        mat_specular = (1.0, 1.0, 1.0, 1.0)
        mat_shininess = (10,)

        glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
        glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
        glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
        glMaterialfv(GL_FRONT, GL_SHININESS, mat_shininess)

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

        # OBJETIVO
        # ALTERAR A POSICAO SOMANDO A POSICAO  + O VETOR FOWARD * VELOCIDADE * TEMPO
        # transform.position += transform.forward * spéed * deltaTime

        glTranslatef(self.x, self.y, self.z)

        glRotatef(self.xRot, 1, 0, 0)
        glRotatef(self.yRot, 0, 1, 0)
        glRotatef(self.zRot, 0, 0, 1)

        self.defineMaterial()
        self.model.draw()
        glPopMatrix()

        if self.debug:
            print('x', self.x)
            print('y', self.y)
            print('z', self.z)
            print('xRot', self.xRot)
            print('yRot', self.yRot)
            print('zRot', self.zRot)
            print('forwardX', self.forwardX)
            print('forwardY', self.forwardY)
            print('forwardZ', self.forwardZ)
