from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
# from OBJFileLoader import *
import Utils
from ply import *
import math
import Materials


class Airplane():
    def __init__(self):
        self.model = PlyReader("models/airplane/airplane.ply", frontFace=GL_CW)

        self.debug = True

        self.modelOffset = -7

        self.forwardX = -1
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

        self.xRotV = 1
        self.yRotV = 1
        self.zRotV = 1

    def command(self, key):

        if key == b'p':
            self.debug = not self.debug
            print("DEBUG ATIVO") if self.debug else print("DEBUG DESATIVADO")

        # SETA ESQUERDA
        if key == 100:
            self.xRot += self.xRotV
            degree = Utils.radToDegrees(-self.xRotV)
            self.forwardZ = self.forwardZ * \
                math.cos(degree) - self.forwardY * math.sin(degree)

            self.forwardY = self.forwardZ * \
                math.sin(degree) + self.forwardY * math.cos(degree)

        # SETA DIREITA
        elif key == 102:
            self.xRot -= self.xRotV
            degree = Utils.radToDegrees(+self.xRotV)
            self.forwardZ = self.forwardZ * \
                math.cos(degree) - self.forwardY * math.sin(degree)

            self.forwardY = self.forwardZ * \
                math.sin(degree) + self.forwardY * math.cos(degree)

        # SETA CIMA
        elif key == 101:
            self.zRot += self.zRotV
            degree = Utils.radToDegrees(self.zRotV)
            self.forwardX = self.forwardX * \
                math.cos(degree) - self.forwardY * math.sin(degree)

            self.forwardY = self.forwardX * \
                math.sin(degree) + self.forwardY * math.cos(degree)

        # SETA BAIXO
        elif key == 103:
            self.zRot -= self.zRotV
            degree = Utils.radToDegrees(-self.zRotV)
            self.forwardX = self.forwardX * \
                math.cos(degree) - self.forwardY * math.sin(degree)

            self.forwardY = self.forwardX * \
                math.sin(degree) + self.forwardY * math.cos(degree)

        # PARA FRENTE
        elif key == b'f':
            self.x += self.forwardX * (self.xV)
            self.y += self.forwardY * (self.xV)
            self.z += self.forwardZ * (self.xV)
            # self.x += self.forwardX * (-1)
            # self.y += self.forwardY * (0)
            # self.z += self.forwardZ * (0)
            # self.x -= self.xV

        # PARA TRAS
        elif key == b'g':
            # self.x += self.forwardX * (+self.xV)
            self.x -= self.forwardX * (self.xV)
            self.y -= self.forwardY * (self.xV)
            self.z -= self.forwardZ * (self.xV)
            # self.x += self.xV

    def timer(self, delay, value):
        pass

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
            glTranslatef(0, 0, 0)
            glLineWidth(3.0)
            Materials.BlackMaterial()
            glBegin(GL_LINES)
            glVertex3f(0, 0, 0)
            glVertex3f(self.forwardX, self.forwardY, self.forwardZ)
            glEnd()
            glutSolidSphere(.2, 30, 30)

        # OBJETIVO
        # ALTERAR A POSICAO SOMANDO A POSICAO  + O VETOR FOWARD * VELOCIDADE * TEMPO
        # transform.position += transform.forward * speed * deltaTime
        glTranslatef(self.x, self.y, self.z)

        # glTranslatef(self.modelOffset, 0, 0)
        glRotatef(self.xRot, 1, 0, 0)
        glRotatef(self.yRot, 0, 1, 0)
        glRotatef(self.zRot, 0, 0, 1)

        self.defineMaterial()
        self.model.draw()

        glPopMatrix()
