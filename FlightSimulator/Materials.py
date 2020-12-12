from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


def MountainMaterial():
    mat_ambient = (0.6, 0.0, 0.0, 1.0)
    mat_diffuse = (155/255, 118/255, 83/255, 1.0)
    mat_specular = (0, 0, 0, 1.0)
    mat_shininess = (0,)

    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialfv(GL_FRONT, GL_SHININESS, mat_shininess)


def OceanMaterial():
    mat_ambient = (0.6, 0.0, 0.0, 1.0)
    mat_diffuse = (0/255, 47/255, 75/255, 1.0)
    mat_specular = (0.1, 0.1, 0.2, 1.0)
    mat_shininess = (0,)

    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialfv(GL_FRONT, GL_SHININESS, mat_shininess)


def AirplaneMaterial():
    mat_ambient = (.3, .3, .3, 1)
    mat_diffuse = (196/255, 202/255, 206/255, 1.0)
    mat_specular = (1.0, 1.0, 1.0, 1.0)
    mat_shininess = (10,)

    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialfv(GL_FRONT, GL_SHININESS, mat_shininess)


def BlackMaterial():
    mat_ambient = (.6, .6, .6, 1.0)
    mat_diffuse = (0/255, 0/255, 0/255, 1.0)
    mat_specular = (0.1, 0.1, 0.2, 1.0)
    mat_shininess = (0,)

    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialfv(GL_FRONT, GL_SHININESS, mat_shininess)


def GeneralMaterial(diffuse):
    mat_ambient = (0, 0.0, 0.0, 1.0)
    # mat_diffuse = (0/255, 0/255, 0/255, 1.0)
    mat_specular = (0.1, 0.1, 0.2, 1.0)
    mat_shininess = (0,)

    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialfv(GL_FRONT, GL_SHININESS, mat_shininess)
