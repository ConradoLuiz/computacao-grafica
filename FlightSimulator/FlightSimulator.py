from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from Airplane import *
from Terrain import *
import Utils
import png
import math


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

        self.cameraX = 20
        self.cameraY = 20
        self.cameraZ = 0 + self.cameraDistance

        self.cameraXRot = 0
        self.cameraZRot = 0

        self.cameraRotSpeed = 1.5

        self.debug = True

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

    def initGL(self):
        # self.loadTextures()
        # glEnable(GL_TEXTURE_2D)
        glEnable(GL_MULTISAMPLE)
        glClearDepth(1.0)
        glEnable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION)
        gluPerspective(45, self.width/self.height, 0.1, 100000.0)
        glShadeModel(GL_SMOOTH)

        glClearColor(69/255, 160/255, 200/255, 1.0)

        mat_ambient = (0.6, 0.0, 0.0, 1.0)
        mat_diffuse = (0, 0.0, 1.0, 1.0)
        mat_specular = (1.0, 1.0, 1.0, 1.0)
        mat_shininess = (10,)

        glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
        glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
        glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
        glMaterialfv(GL_FRONT, GL_SHININESS, mat_shininess)

        light_position = (0, 10, 0, 0.0)
        glLightfv(GL_LIGHT0, GL_POSITION, light_position)
        glEnable(GL_LIGHT0)

        light_position = (0, -5, 0, 0.0)
        glLightfv(GL_LIGHT1, GL_POSITION, light_position)
        glEnable(GL_LIGHT1)

        glEnable(GL_LIGHTING)

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
        # self.terrain.timer(self.delay, value)

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

    def mouseDrag(self, x, y):
        if self.isDragging:
            # glTranslatef(5 * (x-self.previousMouseX)/self.width,
            #              5 * -(y-self.previousMouseY)/self.height, 0)
            # self.cameraXRot = (x-self.previousMouseX/self.width)
            # self.cameraZRot = (y-self.previousMouseY/self.height)

            self.rotateCameraHorizontal((x-self.previousMouseX))
            self.rotateCameraVertical((y-self.previousMouseY))
            self.previousMouseX = x
            self.previousMouseY = y

    def specialKeys(self, key, x, y):
        self.airplane.command(key)
        glutPostRedisplay()

    def keys(self, key, x, y):
        self.airplane.command(key)
        if key == b'p':
            self.debug != self.debug
        if key == b'r':
            del self.airplane
            # del self.terrain
            self.loadObjects()
        if key == b'i':
            self.rotateCameraHorizontal(self.cameraRotSpeed)
            # self.cameraXRot += 0.1
            # self.cameraZRot += 0.1

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
        proj = Utils.project_onto_plane(
            (self.cameraX, self.cameraY, self.cameraZ), (0, 1, 0))
        # print(proj)
        self.cameraX = proj[0] * \
            math.cos(Utils.radToDegrees(rad)) - self.cameraY * \
            math.sin(Utils.radToDegrees(rad))

        self.cameraY = proj[0] * \
            math.sin(Utils.radToDegrees(rad)) + self.cameraY * \
            math.cos(Utils.radToDegrees(rad))

        # self.cameraZ = proj[1] * \
        #     math.cos(Utils.radToDegrees(rad)) - self.cameraY * \
        #     math.sin(Utils.radToDegrees(rad))

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

        gluLookAt(self.cameraX, self.cameraY,
                  self.cameraZ, self.camLookX, self.camLookY, self.camLookZ, 0, 1, 0)

        self.airplane.updatePos()
        self.airplane.draw()
        self.terrain.draw()

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
            glVertex3f(4, 0, 0)
            glEnd()
            # Y
            Materials.GeneralMaterial((0, 1, 0, 1))
            glLineWidth(3.0)
            glBegin(GL_LINES)
            glVertex3f(0, 0, 0)
            glVertex3f(0, 4, 0)
            glEnd()
            # Z
            Materials.GeneralMaterial((0, 0, 1, 1))
            glLineWidth(3.0)
            glBegin(GL_LINES)
            glVertex3f(0, 0, 0)
            glVertex3f(0, 0, 4)
            glEnd()
        glPopMatrix()

        glutSwapBuffers()
