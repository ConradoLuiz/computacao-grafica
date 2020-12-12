from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from Airplane import *
from Terrain import *
import Utils
import png
import math

vertices = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1),
)

linhas = (
    (0, 1),
    (0, 3),
    (0, 4),
    (2, 1),
    (2, 3),
    (2, 7),
    (6, 3),
    (6, 4),
    (6, 7),
    (5, 1),
    (5, 4),
    (5, 7),
)

faces = (
        (0, 1, 2, 3),
        (3, 2, 7, 6),
        (6, 7, 5, 4),
        (4, 5, 1, 0),
        (1, 5, 7, 2),
        (4, 0, 3, 6)
)

# https://www.opengl.org/wiki/Calculating_a_Surface_Normal
# Begin Function CalculateSurfaceNormal (Input Triangle) Returns Vector
#  Set Vector U to (Triangle.p2 minus Triangle.p1)
#  Set Vector V to (Triangle.p3 minus Triangle.p1)
#  Set Normal.x to (multiply U.y by V.z) minus (multiply U.z by V.y)
#  Set Normal.y to (multiply U.z by V.x) minus (multiply U.x by V.z)
#  Set Normal.z to (multiply U.x by V.y) minus (multiply U.y by V.x)
#  Returning Normal
# End Function


def calculaNormalFace(face):
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


def Cubo():
    glBegin(GL_QUADS)
    for face in faces:
        glNormal3fv(calculaNormalFace(face))
        for vertex in face:
            glVertex3fv(vertices[vertex])
    glEnd()


class FlightSimulator():

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.delay = 30

        self.wX = 0
        self.wY = 0
        self.wZ = 0

        self.zoom = 1
        self.deltaZoom = 0.1

        self.previousMouseX = 0
        self.previousMouseY = 0

        self.cameraDistance = 25
        self.cameraHeight = 4

        self.cameraX = 0 + self.cameraDistance
        self.cameraY = 4
        self.cameraZ = 0

        self.cameraXRot = 0
        self.cameraZRot = 0

        self.cameraRotSpeed = 1.5

        self.debug = False

        self.flyingSpeed = 1

        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA |
                            GLUT_DEPTH | GLUT_MULTISAMPLE)

        glutInitWindowSize(self.width, self.height)
        self.window = glutCreateWindow("Flight Simulator")

        glutDisplayFunc(self.draw)

        self.initGL()

        glutTimerFunc(self.delay, self.timer, self.delay)
        glutMouseFunc(self.mouse)
        glutSpecialFunc(self.specialKeys)
        glutMotionFunc(self.mouseDrag)
        glutKeyboardFunc(self.keys)

        self.a = 0

    def initGL(self):
        # self.loadTextures()
        # glEnable(GL_TEXTURE_2D)

        # glShadeModel(GL_FLAT)

        mat_ambient = (0.6, 0.0, 0.0, 1.0)
        mat_diffuse = (0, 0.0, 1.0, 1.0)
        mat_specular = (1.0, 1.0, 1.0, 1.0)
        mat_shininess = (10,)

        glClearColor(69/255, 160/255, 200/255, 1.0)
        glShadeModel(GL_SMOOTH)

        glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
        glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
        glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
        glMaterialfv(GL_FRONT, GL_SHININESS, mat_shininess)

        glEnable(GL_LIGHTING)
        self.light_position = (0, 10, 0, .4)
        glEnable(GL_LIGHT0)

        glClearDepth(1.0)
        glMatrixMode(GL_PROJECTION)
        gluPerspective(45, self.width/self.height, 0.1, 100000.0)
        # glMatrixMode(GL_MODELVIEW)

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_MULTISAMPLE)

        self.loadObjects()

    def loadObjects(self):
        self.airplane = Airplane()
        self.terrain = Terrain(self.width, self.height)

    def loadTextures(self):
        self.textures = glGenTextures(2)

        ################################################################################
        glBindTexture(GL_TEXTURE_2D, self.textures[0])
        reader = png.Reader(filename='textures/sky.png')
        w, h, pixels, metadata = reader.read_flat()
        if(metadata['alpha']):
            modo = GL_RGBA
        else:
            modo = GL_RGB
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexImage2D(GL_TEXTURE_2D, 0, modo, w, h, 0, modo,
                     GL_UNSIGNED_BYTE, pixels.tolist())
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
        ################################################################################

        glBindTexture(GL_TEXTURE_2D, self.textures[1])
        reader = png.Reader(
            filename='textures/PicknGO.png')
        w, h, pixels, metadata = reader.read_flat()
        if(metadata['alpha']):
            modo = GL_RGBA
        else:
            modo = GL_RGB
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexImage2D(GL_TEXTURE_2D, 0, modo, w, h, 0, modo,
                     GL_UNSIGNED_BYTE, pixels.tolist())
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)

    def timer(self, i):
        glutPostRedisplay()
        value = i + self.delay

        self.airplane.timer(self.delay, value)
        self.terrain.timer(self.delay, value)

        glutTimerFunc(self.delay, self.timer, value)

    def run(self):
        glutMainLoop()

    def mouse(self, btn, state, mouseX, mouseY):
        # btn -> 0 == botao esquerdo; 1 == botao rolagem; 2 == botao direito; 3 == rolagem para cima; 4 == rolagem para baixo
        if btn == 3:
            # self.zoom -= self.deltaZoom
            self.zoomCamera(0.8)
        if btn == 4:
            # self.zoom += self.deltaZoom
            self.zoomCamera(1.1)

        if btn == 0 and state == 0:
            self.previousMouseX = mouseX
            self.previousMouseY = mouseY
            self.isDragging = True
        if btn == 0 and state == 1:
            self.isDragging = False
        # if btn == 2 and state == 0:
        #     pause_rotation = not pause_rotation

        print(mouseX, mouseY)

    def mouseDrag(self, x, y):
        if self.isDragging:

            self.terrain.mouse(x, y, self.previousMouseX, self.previousMouseY)

            # self.rotateCameraHorizontal((x-self.previousMouseX))
            # self.rotateCameraVertical((y-self.previousMouseY))
            self.previousMouseX = x
            self.previousMouseY = y

    def specialKeys(self, key, x, y):
        # self.airplane.command(key)
        self.terrain.command(key)

        glutPostRedisplay()

    def keys(self, key, x, y):
        # self.airplane.command(key)
        self.terrain.command(key)

        if key == b'p':
            self.debug != self.debug
        if key == b'r':
            del self.airplane
            del self.terrain
            self.loadObjects()

        if key == b'i':
            self.rotateCameraHorizontal(self.cameraRotSpeed)
            # self.cameraXRot += 0.1
            # self.cameraZRot += 0.1
        if key == b't':
            self.a += 1

        if key == b'o':
            self.rotateCameraHorizontal(-self.cameraRotSpeed)
            # self.cameraXRot -= 0.1
            # self.cameraZRot -= 0.1

        glutPostRedisplay()

    def calculateCameraPos(self):
        # self.cameraX = self.airplane.x
        # self.cameraY = self.airplane.y + self.cameraHeight
        # # (+self.airplane.zRot * .2)
        # self.cameraZ = (self.airplane.z + self.zoom + self.cameraDistance) * \
        #     self.airplane.zRot

        # self.cameraX = self.cameraX + self.zoom
        # self.cameraY = 20 + self.zoom
        # self.cameraZ = (-20 - self.zoom)

        self.camLookX = 0
        self.camLookY = 0
        self.camLookZ = 0
        pass

    def rotateCameraHorizontal(self, rad):
        self.cameraX = self.cameraX * \
            math.cos(Utils.radToDegrees(rad)) - self.cameraZ * \
            math.sin(Utils.radToDegrees(rad))

        self.cameraZ = self.cameraX * \
            math.sin(Utils.radToDegrees(rad)) + self.cameraZ * \
            math.cos(Utils.radToDegrees(rad))

    def rotateCameraVertical(self, rad):
        normalizedPosition = Utils.normalize(
            (self.cameraX, self.cameraY, self.cameraZ))

        if normalizedPosition[1] >= 0.98 and rad > 0:
            return
        if normalizedPosition[1] <= -0.98 and rad < 0:
            return

        proj = Utils.project_onto_plane(
            normalizedPosition, (0, 1, 0))

        proj = Utils.normalize(proj)

        perpendicular = Utils.perpendicular_vector(proj)

        rotMat = Utils.rotation_matrix(perpendicular, Utils.radToDegrees(rad))

        self.cameraX, self.cameraY, self.cameraZ = Utils.rotate(
            rotMat, [self.cameraX, self.cameraY, self.cameraZ])

    def zoomCamera(self, delta):
        # self.zoom += delta
        self.cameraX *= delta
        self.cameraY *= delta
        self.cameraZ *= delta

    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        self.calculateCameraPos()
        # print(self.cameraXRot)
        # print(self.cameraZRot)
        glPushMatrix()
        glLightfv(GL_LIGHT0, GL_POSITION, self.light_position)

        gluLookAt(self.cameraX, self.cameraY,
                  self.cameraZ, self.camLookX, self.camLookY, self.camLookZ, 0, 1, 0)

        self.airplane.updatePos()

        self.airplane.draw()
        self.terrain.draw()
        # glPushMatrix()
        # glTranslatef(0, 0, 6)
        # glRotatef(self.a, 1, 0, 0)
        # Cubo()
        # glPopMatrix()

        # ESFERA NO CENTRO DO MUNDO
        # glutWireSphere(2, 30, 30)

        # CUBO NA DIREITA DO CENTRO
        # glTranslatef(0, 0, 7)
        # glutSolidCube(4)

        if self.debug:
            # print('Zoom', self.zoom)
            # print('Delta Zoom', self.deltaZoom)
            glTranslatef(0, 0, 0)
            Materials.GeneralMaterial((1, 1, 1, 1))
            glutSolidSphere(.1, 30, 30)
            # X
            Materials.GeneralMaterial((1, 0, 0, 1))
            glLineWidth(3.0)
            glBegin(GL_LINES)
            glVertex3f(0, 0, 0)
            glVertex3f(10, 0, 0)
            glEnd()
            # Y
            Materials.GeneralMaterial((0, 1, 0, 1))
            glLineWidth(3.0)
            glBegin(GL_LINES)
            glVertex3f(0, 0, 0)
            glVertex3f(0, 10, 0)
            glEnd()
            # Z
            Materials.GeneralMaterial((0, 0, 1, 1))
            glLineWidth(3.0)
            glBegin(GL_LINES)
            glVertex3f(0, 0, 0)
            glVertex3f(0, 0, 10)
            glEnd()
        glPopMatrix()

        glutSwapBuffers()
