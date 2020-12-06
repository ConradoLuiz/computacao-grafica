from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import noise
import Utils
import random
import math


class Terrain():
    def __init__(self, width, height, scale=20):
        self.width = width
        self.height = height
        self.scale = scale

        self.xMin = -1
        self.xMax = 1

        self.zMin = -1
        self.zMax = 1

        self.delta = 0.1

        self.vertex = []
        # self.heights = [[None] * (self.xMin + self.xMax) /
        #                 self.delta] * (self.xMin + self.xMax) / self.delta

        self.heights = [[0 for _ in range(
            math.ceil((abs(self.xMin) + self.xMax)/self.delta)+2)] for _ in range(
            math.ceil((abs(self.xMin) + self.xMax)/self.delta)+2)]

        self.glLists = []

        self.generateHeight()
        self.createMesh()
        # self.generateList()

        self.posX = 0.
        self.posY = -3.
        self.posZ = 0.

    def defineMaterial(self):
        mat_ambient = (0.6, 0.0, 0.0, 1.0)
        mat_diffuse = (155/255, 118/255, 83/255, 1.0)
        mat_specular = (0.1, .1, .1, 1.0)
        mat_shininess = (2,)

        glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
        glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
        glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
        glMaterialfv(GL_FRONT, GL_SHININESS, mat_shininess)

    def generateHeight(self):
        z = self.zMin
        i = 0
        zoff = random.uniform(-1, 1)
        xoffSeed = random.uniform(-1, 1)
        while z <= self.zMax + self.delta:
            x = self.xMin
            j = 0
            xoff = xoffSeed
            while x <= self.xMax + self.delta:
                # print(j, j+1)
                self.heights[i][j] = noise.pnoise2(xoff, zoff)
                x += self.delta
                xoff += self.delta
                j += 1
            i += 1
            z += self.delta
            zoff += self.delta

    def createMesh(self):

        self.glLists.append(glGenLists(1))

        glNewList(self.glLists[-1], GL_COMPILE)
        glFrontFace(GL_CCW)
        self.defineMaterial()

        z = self.zMin
        i = 0

        while z < self.zMax:
            x = self.xMin
            j = 0
            glBegin(GL_TRIANGLE_STRIP)
            while x < self.xMax:

                vertex1 = [x, self.heights[j][i], z]

                vertex2 = [x, self.heights[j][i+1], z + self.delta]

                # APENAS PARA NORMAL
                vertex3 = [x + self.delta,
                           self.heights[j+1][i], z]

                normal = Utils.calcNormalTriangulo(
                    vertex1, vertex3, vertex2)

                glNormal3fv(normal)
                glVertex3fv(vertex1)
                glVertex3fv(vertex2)
                # self.vertex.append(vertex)
                x += self.delta
                j += 1
            glEnd()
            i += 1
            z += self.delta

        glEndList()

    def generateList(self):
        self.glLists.append(glGenLists(1))

        glNewList(self.glLists[-1], GL_COMPILE)
        glFrontFace(GL_CCW)

        glBegin(GL_TRIANGLE_STRIP)

        for i, vertex in enumerate(self.vertex):
            if i + 2 < len(self.vertex):
                normal = Utils.calcNormalTriangulo(
                    vertex, self.vertex[i+1], self.vertex[i+2])
                glNormal3fv(normal)
            glVertex3fv(vertex)

        glEnd()
        glEndList()

    def draw(self):
        glPushMatrix()

        glTranslatef(self.posX, self.posY, self.posZ)
        glScalef(50, 50, 50)
        glCallList(self.glLists[-1])

        glPopMatrix()
