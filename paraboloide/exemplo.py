import math
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

width, height = 1200.0, 800.0
rotation_delay = 30
screen_translate = 0.1

x0 = -1
y0 = -1
xf = 1
yf = 1
dx = 0.1
dy = 0.1

def paraboloide(x,y):
    # Paraboloide Circular
    return x**2+y**2

def desenhaFuncao():
    glBegin(GL_POINTS)
    x = x0
    while x < xf:
        y = y0
        while y < yf:
            z = paraboloide(x,y)
            glVertex3f(x,y,z)
            y += dy
        x += dx
    glEnd()

def desenha():
    global a
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glPushMatrix()
    glRotatef(-a, 1,0,0)
    desenhaFuncao()
    glPopMatrix()
    glutSwapBuffers()
    a += 1
    return

def timer(i):
    glutPostRedisplay()
    glutTimerFunc(rotation_delay,timer,1)

if __name__ == '__main__':
    # PROGRAMA PRINCIPAL
    a = 0

    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH | GLUT_MULTISAMPLE)
    glutInitWindowSize(int(width),int(height))
    glutCreateWindow("Paraboloide")
    glutDisplayFunc(desenha)
    glEnable(GL_MULTISAMPLE)
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.,0.,0.,1.)
    gluPerspective(45,width/height,0.1,100.0)
    glTranslatef(0.0,-0.4,-6)
    glutTimerFunc(rotation_delay,timer,1)
    glutMainLoop()