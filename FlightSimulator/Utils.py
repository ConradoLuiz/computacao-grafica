from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math
import numpy as np


def lerp(x0, x1, amt):
    return (1 - amt) * x0 + amt * x1


def myMap(v, b1, t1, b2, t2):
    return (v - b1)/(t1 - b1) * (t2 - b2) + b2


def radToDegrees(rad):
    return rad * (math.pi/180)


def degreeToRad(degree):
    return degree * (180/math.pi)


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


def dot_product(x, y):
    return sum([x[i] * y[i] for i in range(len(x))])


def norm(x):
    return math.sqrt(dot_product(x, x))


def normalize(x):
    return [x[i] / norm(x) for i in range(len(x))]


def project_onto_plane(x, n):
    d = dot_product(x, n) / norm(n)
    p = [d * normalize(n)[i] for i in range(len(n))]
    return [x[i] - p[i] for i in range(len(x))]


def perpendicular_vector(v):
    if v[1] == 0 and v[2] == 0:
        if v[0] == 0:
            raise ValueError('zero vector')
        else:
            return np.cross(v, [1, 0, 0])
    return np.cross(v, [0, 1, 0])


def rotateAroundX(vector, teta):
    rotMat = [
        [1, 0, 0],
        [0, math.cos(teta), -math.sin(teta)],
        [0, math.sin(teta), math.cos(teta)]
    ]
    a = [0, 0, 0]
    a[0] = rotMat[0][0]*vector[0] + rotMat[0][1] * \
        vector[1] + rotMat[0][2]*vector[2]
    a[1] = rotMat[1][0]*vector[0] + rotMat[1][1] * \
        vector[1] + rotMat[1][2]*vector[2]
    a[2] = rotMat[2][0]*vector[0] + rotMat[2][1] * \
        vector[1] + rotMat[2][2]*vector[2]
    return a


def rotateAroundY(vector, teta):
    rotMat = [
        [math.cos(teta), 0, math.sin(teta)],
        [0, 1, 0],
        [-math.sin(teta), 0, math.cos(teta)]
    ]
    a = [0, 0, 0]

    a[0] = rotMat[0][0]*vector[0] + rotMat[0][1] * \
        vector[1] + rotMat[0][2]*vector[2]
    a[1] = rotMat[1][0]*vector[0] + rotMat[1][1] * \
        vector[1] + rotMat[1][2]*vector[2]
    a[2] = rotMat[2][0]*vector[0] + rotMat[2][1] * \
        vector[1] + rotMat[2][2]*vector[2]
    return a


def rotateAroundZ(vector, teta):
    rotMat = [
        [math.cos(teta), -math.sin(teta), 0],
        [math.sin(teta), math.cos(teta), 0],
        [0, 0, 1]
    ]

    a = [0, 0, 0]
    a[0] = rotMat[0][0]*vector[0] + rotMat[0][1] * \
        vector[1] + rotMat[0][2]*vector[2]
    a[1] = rotMat[1][0]*vector[0] + rotMat[1][1] * \
        vector[1] + rotMat[1][2]*vector[2]
    a[2] = rotMat[2][0]*vector[0] + rotMat[2][1] * \
        vector[1] + rotMat[2][2]*vector[2]
    return a


def rotate(rotMat, vector):
    a = [0, 0, 0]
    a[0] = rotMat[0][0]*vector[0] + rotMat[0][1] * \
        vector[1] + rotMat[0][2]*vector[2]
    a[1] = rotMat[1][0]*vector[0] + rotMat[1][1] * \
        vector[1] + rotMat[1][2]*vector[2]
    a[2] = rotMat[2][0]*vector[0] + rotMat[2][1] * \
        vector[1] + rotMat[2][2]*vector[2]
    return a


def rotation_matrix(axis, theta):
    """
    Return the rotation matrix associated with counterclockwise rotation about
    the given axis by theta radians.
    """
    axis = np.asarray(axis)
    axis = axis / math.sqrt(np.dot(axis, axis))
    a = math.cos(theta / 2.0)
    b, c, d = -axis * math.sin(theta / 2.0)
    aa, bb, cc, dd = a * a, b * b, c * c, d * d
    bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
    return np.array([[aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac)],
                     [2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab)],
                     [2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc]])


def eulerAnglesFromMatrix(matrix):
    x = math.atan2(matrix[2][1], matrix[2][2])
    y = math.atan2(-matrix[2][0], math.sqrt(matrix[2][1]**2 + matrix[2][2]**2))
    z = math.atan2(matrix[1][0], matrix[0][0])

    return [x, y, z]


def rotationMatrixTo4d(rotMat):
    newMat = []
    newMat.append([0, 0, 0, 0])
    newMat.append([0, 0, 0, 0])
    newMat.append([0, 0, 0, 0])
    newMat.append([0, 0, 0, 1])

    for i, row in enumerate(rotMat):
        for j, col in enumerate(row):
            newMat[i][j] = rotMat[i][j]

    return newMat


def addMatrix(mat1, mat2):
    newMat = []
    for _ in range(len(mat1)):
        newMat.append([0] * len(mat1[0]))

    for i, row in enumerate(mat1):
        for j, col in enumerate(row):
            newMat[i][j] = mat1[i][j] + mat2[i][j]

    return newMat


def multiplyMatrix(mat1, mat2):
    newMat = []
    for _ in range(len(mat1)):
        newMat.append([0] * len(mat1[0]))

    for i, row in enumerate(mat1):
        for j, col in enumerate(row):
            newMat[i][j] = mat1[i][j] * mat2[i][j]

    return newMat


if __name__ == '__main__':
    # print(math.sin(radToDegrees(90)))
    # print(math.sin(math.pi/2))

    # rotMat = rotation_matrix((0, 1, 0), -math.pi/2)
    # print(rotMat)

    # rotatedVector = rotate(rotMat, (1, 0, 0))

    # print(rotatedVector)
    eye3 = [
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1],
    ]
    rotationMatrixTo4d(eye3)

    print(addMatrix(eye3, eye3))
