from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from Airplane import *


class FlightSimulator():

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.delay = 30

        self.zoom = 0
        self.deltaZoom = 0.05
        self.previousMouseX = 0
        self.previousMouseY = 0

        self.cameraDistance = 25
        self.cameraHeight = 4

        self.cameraX = 0
        self.cameraY = 0
        self.cameraZ = 0 + self.cameraDistance

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
        # glutKeyboardFunc(handleKey)

    def initGL(self):
        glEnable(GL_MULTISAMPLE)
        glClearDepth(1.0)
        glEnable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION)
        gluPerspective(45, self.width/self.height, 0.1, 100.0)
        glShadeModel(GL_SMOOTH)
        glClearColor(53/255, 81/255, 92/255, 1.)
        self.airplane = Airplane()

    def timer(self, i):
        glutPostRedisplay()
        glutTimerFunc(self.delay, self.timer, 1)

    def run(self):
        glutMainLoop()

    def mouse(self, btn, state, mouseX, mouseY):
        # btn -> 0 == botao esquerdo; 1 == botao rolagem; 2 == botao direito; 3 == rolagem para cima; 4 == rolagem para baixo
        if btn == 3:
            self.zoom += self.deltaZoom
        if btn == 4:
            self.zoom -= self.deltaZoom
        # if btn == 0 and state == 0:
        #     self.previousMouseX = mouseX
        #     self.previousMouseY = mouseY
        # isDragging = True
        # if btn == 0 and state == 1:
        #     isDragging = False
        # if btn == 2 and state == 0:
        #     pause_rotation = not pause_rotation

        # def mouseDrag(self):

        # def keyboardFunc(self):

    def specialKeys(self, key, x, y):
        self.airplane.command(key)

    def calculateCameraPos(self):
        self.cameraX = self.airplane.x
        self.cameraY = self.airplane.y + self.cameraHeight
        self.cameraZ = self.airplane.z + self.zoom + self.cameraDistance

    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.calculateCameraPos()

        glPushMatrix()
        gluLookAt(self.cameraX, self.cameraY,
                  self.cameraZ, self.airplane.x, self.airplane.y, self.airplane.z, 0, 1, 0)
        self.airplane.updatePos()
        self.airplane.draw()
        glutWireSphere(2, 30, 30)
        glPopMatrix()
        glutSwapBuffers()
