from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import itertools


class PlyReader():

    def __init__(self, filename, cor=[0, 0, 1]):
        with open(filename, 'r') as file:
            self.end_of_header = 0
            self.n_vertex = 0
            self.n_faces = 0
            self.vertex = []
            self.faces = []
            self.cor = cor

            for i, line in enumerate(file):
                if 'element' in line:
                    if 'vertex' in line:
                        self.n_vertex = int(line.split(' ')[2])
                    if 'face' in line:
                        self.n_faces = int(line.split(' ')[2])
                if 'end_header' in line:
                    self.end_of_header = i
                    break

            # LENDO OS VERTICES
            for i, line in enumerate(file):
                vertex = []
                for n in line.split(' ')[:-1]:
                    vertex.append(float(n))
                self.vertex.append(vertex)
                if i >= self.n_vertex - 1:
                    break

            # LENDO AS FACES
            for i, line in enumerate(file):
                if i >= self.n_faces:
                    break
                faces = []
                for n in line.split(' ')[1:-1]:
                    faces.append(int(n))
                self.faces.append(faces)

            self.gl_list = glGenLists(1)
            glNewList(self.gl_list, GL_COMPILE)
            glFrontFace(GL_CCW)

            for face in self.faces:
                glBegin(GL_POLYGON)
                for vertex in face:
                    # print(self.vertex[vertex])
                    # glColor3fv(self.ver)
                    glNormal3fv(self.vertex[vertex][0:3])
                    glVertex3fv(self.vertex[vertex][0:3])
                glEnd()
            glEndList()

    def draw(self):
        glCallList(self.gl_list)
