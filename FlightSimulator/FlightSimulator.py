from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from Airplane import *
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

        self.zoom = 0
        self.deltaZoom = 0.1

        self.previousMouseX = 0
        self.previousMouseY = 0

        self.cameraDistance = 25
        self.cameraHeight = 4

        self.cameraX = 0
        self.cameraY = 0
        self.cameraZ = 0 + self.cameraDistance

        self.cameraXRot = 1
        self.cameraZRot = 1

        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA |
                            GLUT_DEPTH | GLUT_MULTISAMPLE)

        glutInitWindowSize(self.width, self.height)
        self.window = glutCreateWindow("Flight Simulator")

        glutDisplayFunc(self.draw)

        self.initGL()

        glutTimerFunc(self.delay, self.timer, 1)
        glutMouseFunc(self.mouse)
        glutSpecialFunc(self.specialKeys)
        # glutMotionFunc(self.mouseDrag)
        glutKeyboardFunc(self.keys)

    def initGL(self):
        # self.loadTextures()
        # glEnable(GL_TEXTURE_2D)
        glEnable(GL_MULTISAMPLE)
        glClearDepth(1.0)
        glEnable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION)
        gluPerspective(45, self.width/self.height, 0.1, 100.0)
        glShadeModel(GL_SMOOTH)
        glClearColor(53/255, 81/255, 92/255, 1.)

        mat_ambient = (0.6, 0.0, 0.0, 1.0)
        mat_diffuse = (0, 0.0, 1.0, 1.0)
        mat_specular = (1.0, 1.0, 1.0, 1.0)
        mat_shininess = (50,)
        light_position = (3, 3.0, 3.0, 0.0)

        glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
        glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
        glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
        glMaterialfv(GL_FRONT, GL_SHININESS, mat_shininess)
        glLightfv(GL_LIGHT0, GL_POSITION, light_position)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)

        self.airplane = Airplane()

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
        glutTimerFunc(self.delay, self.timer, 1)

    def run(self):
        glutMainLoop()

    def mouse(self, btn, state, mouseX, mouseY):
        # btn -> 0 == botao esquerdo; 1 == botao rolagem; 2 == botao direito; 3 == rolagem para cima; 4 == rolagem para baixo
        if btn == 3:
            self.zoom -= self.deltaZoom
        if btn == 4:
            self.zoom += self.deltaZoom
        if btn == 0 and state == 0:
            self.previousMouseX = mouseX
            self.previousMouseY = mouseY
            self.isDragging = True
        if btn == 0 and state == 1:
            self.isDragging = False
        if btn == 2 and state == 0:
            pause_rotation = not pause_rotation

    # def mouseDrag(self, x, y):
    #     if self.isDragging:
    #         glMatrixMode(GL_MODELVIEW)
    #         glTranslatef(5 * (x-self.previousMouseX)/self.width,
    #                      5 * -(y-self.previousMouseY)/self.height, 0)
    #         glMatrixMode(GL_MODELVIEW)
    #         # self.cameraXRot = (x-self.previousMouseX/self.width)
    #         # self.cameraZRot = (y-self.previousMouseY/self.height)
    #         self.previousMouseX = x
    #         self.previousMouseY = y

    def specialKeys(self, key, x, y):
        self.airplane.command(key)
        glutPostRedisplay()

    def keys(self, key, x, y):
        self.airplane.command(key)
        glutPostRedisplay()

    def calculateCameraPos(self):
        # self.cameraX = self.airplane.x
        # self.cameraY = self.airplane.y + self.cameraHeight
        # # (+self.airplane.zRot * .2)
        # self.cameraZ = (self.airplane.z + self.zoom + self.cameraDistance) * \
        #     self.airplane.zRot
        self.cameraX = (20 + self.zoom)
        self.cameraY = 20
        self.cameraZ = (-20 - self.zoom)

        self.camLookX = 0
        self.camLookY = 0
        self.camLookZ = 0

    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        self.calculateCameraPos()
        # print(self.cameraXRot)
        # print(self.cameraZRot)
        glPushMatrix()
        # glBindTexture(GL_TEXTURE_2D, self.textures[0])
        # glutSolidSphere(5, 30, 30)
        # glutSolidSphere(2, 30, 30)
        # glRotatef()
        gluLookAt(self.cameraX, self.cameraY,
                  self.cameraZ, self.camLookX, self.camLookY, self.camLookZ, 0, 1, 0)

        self.airplane.updatePos()
        self.airplane.draw()

        # ESFERA NO CENTRO DO MUNDO
        glutWireSphere(2, 30, 30)

        # CUBO NA DIREITA DO CENTRO
        glTranslatef(0, 0, 7)
        glutSolidCube(4)

        glPopMatrix()

        glutSwapBuffers()
