import math
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

width, height = 1200.0, 800.0
rotation_delay = 30
screen_translate = 0.1
zoom = 0.1

x0 = -1
y0 = -1
xf = 1
yf = 1
dx = 0.1
dy = 0.1

pMouseX = None
pMouseY = None
isDragging = False

a = 0


def paraboloide(x, y):
    # Paraboloide Circular
    return x**2+y**2


v = []
x = x0
while x < xf:
    y = y0
    while y < yf:
        z = paraboloide(x, y)
        v += [[x, y, z]]
        y += dy
    x += dx


def desenhaFuncao():
    glBegin(GL_POINTS)

    i = 0
    for vertex in v:
        glColor3f(vertex[0], vertex[1], vertex[2])
        glVertex3f(vertex[0], vertex[1], vertex[2])
        i += 1

    glEnd()


def desenha():
    global a
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glPushMatrix()
    glRotatef(-a, 1, 0, 0)
    desenhaFuncao()
    glPopMatrix()
    glutSwapBuffers()
    a += 1
    return


def mouseFunc(btn, state, mouseX, mouseY):
    # btn -> 0 == botao esquerdo; 1 == botao rolagem; 2 == botao direito; 3 == rolagem para cima; 4 == rolagem para baixo
    global pMouseX
    global pMouseY
    global isDragging

    if btn == 3:
        glTranslatef(0, 0, zoom)
    if btn == 4:
        glTranslatef(0, 0, -zoom)
    if btn == 0 and state == 0:
        pMouseX = mouseX
        pMouseY = mouseY
        isDragging = True
    if btn == 0 and state == 1:
        isDragging = False


def mouseDrag(x, y):
    if isDragging:
        global pMouseX
        global pMouseY
        glTranslatef(5 * (x-pMouseX)/width, 5 * -(y-pMouseY)/height, 0)
        pMouseX = x
        pMouseY = y


def timer(i):
    glutPostRedisplay()
    glutTimerFunc(rotation_delay, timer, 1)


if __name__ == '__main__':
    # PROGRAMA PRINCIPAL
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA |
                        GLUT_DEPTH | GLUT_MULTISAMPLE)
    glutInitWindowSize(int(width), int(height))
    glutCreateWindow("Paraboloide")
    glutDisplayFunc(desenha)
    glEnable(GL_MULTISAMPLE)
    glEnable(GL_DEPTH_TEST)
    glClearColor(0., 0., 0., 1.)
    gluPerspective(45, width/height, 0.1, 100.0)
    glTranslatef(0.0, -0.4, -6)
    glutTimerFunc(rotation_delay, timer, 1)
    glutMouseFunc(mouseFunc)
    glutMotionFunc(mouseDrag)
    glutMainLoop()
