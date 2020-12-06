from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math


def lerp(x0, x1, amt):
    return (1 - amt) * x0 + amt * x1


def myMap(v, b1, t1, b2, t2):
    return (v - b1)/(t1 - b1) * (t2 - b2) + b2


def calcNormalPolygon(p):
    normal = [0, 0, 0]
    for i, v in enumerate(p):
        j = (i + 1) % len(p)
        normal[0] += (p[i][1] - p[j][1]) * (p[i][2] + p[j][2])
        normal[1] += (p[i][2] - p[j][2]) * (p[i][0] + p[j][0])
        normal[2] += (p[i][0] - p[j][0]) * (p[i][1] + p[j][1])

    return normal


def calcNormalTriangulo(v0, v1, v2):
    x = 0
    y = 1
    z = 2
    U = (v2[x]-v0[x], v2[y]-v0[y], v2[z]-v0[z])
    V = (v1[x]-v0[x], v1[y]-v0[y], v1[z]-v0[z])
    N = ((U[y]*V[z]-U[z]*V[y]), (U[z]*V[x]-U[x]*V[z]), (U[x]*V[y]-U[y]*V[x]))
    NLength = math.sqrt(N[x]*N[x]+N[y]*N[y]+N[z]*N[z])
    return (N[x]/NLength, N[y]/NLength, N[z]/NLength)


def calculaNormalFace(face, vertices):
    x = 0
    y = 1
    z = 2
    v0 = vertices[face[0]]
    v1 = vertices[face[1]]
    v2 = vertices[face[2]]
    U = (v2[x]-v0[x], v2[y]-v0[y], v2[z]-v0[z])
    V = (v1[x]-v0[x], v1[y]-v0[y], v1[z]-v0[z])
    N = ((U[y]*V[z]-U[z]*V[y]), (U[z]*V[x]-U[x]*V[z]), (U[x]*V[y]-U[y]*V[x]))
    NLength = math.sqrt(N[x]*N[x]+N[y]*N[y]+N[z]*N[z])
    return (N[x]/NLength, N[y]/NLength, N[z]/NLength)
