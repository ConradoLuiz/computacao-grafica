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
        self.model = PlyReader(
            "models/airplane/airplane2.ply", frontFace=GL_CW)

        self.debug = False

        self.modelOffset = -7

        self.forwardX = -1
        self.forwardY = 0
        self.forwardZ = 0

        self.up = [0, 1, 0]
        self.right = [0, 0, -1]

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

        self.angle = 0

        self.rotationMatrix = [
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
        ]

        self.xRotV = 1
        self.yRotV = 1
        self.zRotV = 1

    def command(self, key):

        if key == b'p':
            self.debug = not self.debug
            print("DEBUG ATIVO") if self.debug else print("DEBUG DESATIVADO")
            # print(Utils.norm(self.up))
            # print(Utils.norm(self.right))
            # print(Utils.norm([self.forwardX, self.forwardY, self.forwardZ]))

        # # SETA ESQUERDA
        # if key == 100:
        #     self.xRot += self.xRotV

        # # SETA DIREITA
        # elif key == 102:
        #     self.xRot -= self.xRotV

        # # SETA CIMA
        # elif key == 101:
        #     self.zRot += self.zRotV

        # # SETA BAIXO
        # elif key == 103:
        #     self.zRot -= self.zRotV

        # # PARA FRENTE
        # elif key == b'f':
        #     self.x -= self.xV

        # # PARA TRAS
        # elif key == b'g':
        #     self.x += self.xV

        # # ROTAÇÃO Y ESQUERDA
        # elif key == b'j':
        #     self.yawPlane(-1)

        # # ROTAÇÃO Y DIREITA
        # elif key == b'k':
        #     self.yawPlane(1)

        # -------------------------------------------------------------------------------------
        # -------------------------------------------------------------------------------------
        # -------------------------------------------------------------------------------------
        # -------------------------------------------------------------------------------------
        #

        # SETA ESQUERDA
        if key == 100:
            self.rollPlane(self.xRotV)

        # SETA DIREITA
        elif key == 102:
            self.rollPlane(-self.xRotV)

        # SETA CIMA
        elif key == 101:
            self.pitchPlane(-self.zRotV)

        # SETA BAIXO
        elif key == 103:
            self.pitchPlane(+self.zRotV)

        # # ROTAÇÃO Y ESQUERDA
        # elif key == b'j':
        #     self.yawPlane(-1)

        # # ROTAÇÃO Y DIREITA
        # elif key == b'k':
        #     self.yawPlane(1)

        # # PARA FRENTE
        # elif key == b'f':
        #     self.x += self.forwardX * (self.xV)
        #     self.y += self.forwardY * (self.xV)
        #     self.z += self.forwardZ * (self.xV)

        # # PARA TRAS
        # elif key == b'g':
        #     # # self.x += self.forwardX * (+self.xV)
        #     self.x -= self.forwardX * (self.xV)
        #     self.y -= self.forwardY * (self.xV)
        #     self.z -= self.forwardZ * (self.xV)

    def timer(self, delay, value):
        pass

    def rollPlane(self, rad):
        # self.forwardX, self.forwardY, self.forwardZ = Utils.rotateAroundX(
        #     [self.forwardX, self.forwardY, self.forwardZ], degree)
        # print(rad)
        # print(degree)

        degree = Utils.radToDegrees(rad)

        self.angle += degree

        oldRot = [self.xRot, self.yRot, self.zRot]

        self.rotationMatrix = Utils.rotation_matrix(
            [self.forwardX, self.forwardY, self.forwardZ], -degree)

        self.up = Utils.rotate(self.rotationMatrix, self.up)
        self.right = Utils.rotate(self.rotationMatrix, self.right)

        self.rotationMatrix = Utils.rotation_matrix(
            [self.forwardX, self.forwardY, self.forwardZ], self.angle)

        # print(rotMat)
        # print(self.rotationMatrix)
        # self.rotationMatrix = Utils.multiplyMatrix(self.rotationMatrix, rotMat)

        # self.xRot, self.yRot, self.zRot = Utils.eulerAnglesFromMatrix(
        #     self.rotationMatrix)

        # self.xRot, self.yRot, self.zRot = Utils.degreeToRad(
        #     self.xRot), Utils.degreeToRad(self.yRot), Utils.degreeToRad(self.zRot)

        return

    def pitchPlane(self, rad):

        # -------------------------------------------------------------------------------------------
        # -------------------------------------------------------------------------------------------
        # -------------------------------------------------------------------------------------------

        degree = Utils.radToDegrees(rad)

        self.angle += degree

        oldRot = [self.xRot, self.yRot, self.zRot]

        # self.xRot, self.yRot, self.zRot = Utils.eulerAngleFromMatrix(
        #     self.rotationMatrix)
        # print(self.rotationMatrix)
        # self.xRot, self.yRot, self.zRot = Utils.degreeToRad(
        #     self.xRot), Utils.degreeToRad(self.yRot), Utils.degreeToRad(self.zRot)
        self.rotationMatrix = Utils.rotation_matrix(self.right, -degree)

        self.forwardX, self.forwardY, self.forwardZ = Utils.rotate(self.rotationMatrix,
                                                                   [self.forwardX, self.forwardY, self.forwardZ])

        self.up = Utils.rotate(self.rotationMatrix, self.up)

        self.rotationMatrix = Utils.rotation_matrix(self.right, self.angle)

        return

    def yawPlane(self, rad):

        self.angle += rad

        degrees = Utils.radToDegrees(rad)

        self.forwardX = math.cos(degrees)
        self.forwardY = 0
        self.forwardZ = math.sin(degrees)

        # self.xRot, self.yRot, self.zRot = Utils.normalize(
        #     [self.xRot, self.yRot, self.zRot])

        return

    def defineMaterial(self):
        Materials.AirplaneMaterial()

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
            print('angle', self.angle)
            print('xRot', self.xRot)
            print('yRot', self.yRot)
            print('zRot', self.zRot)
            print('RotationMatrix', self.rotationMatrix)
            print('forwardX', self.forwardX)
            print('forwardY', self.forwardY)
            print('forwardZ', self.forwardZ)
            print('Up', self.up)
            print('Right', self.right)
            glTranslatef(0, 0, 0)
            glLineWidth(3.0)
            Materials.BlackMaterial()
            glBegin(GL_LINES)
            glVertex3f(0, 0, 0)
            glVertex3f(self.forwardX*10, self.forwardY*10, self.forwardZ*10)
            glEnd()
            glBegin(GL_LINES)
            glVertex3f(0, 0, 0)
            glVertex3f(self.up[0]*10, self.up[1]*10, self.up[2]*10)
            glEnd()
            glBegin(GL_LINES)
            glVertex3f(0, 0, 0)
            glVertex3f(self.right[0]*10, self.right[1]*10, self.right[2]*10)
            glEnd()
            glutSolidSphere(.2, 30, 30)

        # OBJETIVO
        # glTranslatef(-self.x, -self.y, -self.z)

        glTranslatef(self.x, self.y, self.z)

        # glTranslatef(self.modelOffset, 0, 0)
        # glRotatef(self.xRot, 1, 0, 0)
        # glRotatef(self.yRot, 0, 1, 0)
        # glRotatef(self.zRot, 0, 0, 1)
        # glRotatef(self.angle, self.xRot, self.yRot, self.zRot)

        glMultMatrixf(Utils.rotationMatrixTo4d(self.rotationMatrix))

        # glTranslatef(-self.x, -self.y, -self.z)

        # glTranslatef(self.x, self.y, self.z)

        # glMultMatrixf(self.rotationMatrix)

        self.defineMaterial()
        self.model.draw()

        glPopMatrix()
