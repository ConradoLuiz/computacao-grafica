import math
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

width, height = 1200.0, 800.0
rotation_delay = 30
screen_translate = 0.1
zoom = 0.1
pause_rotation = False
pespective = 45

n_points = 50

x0 = -1
y0 = -1
xf = 1
yf = 1
dx = 0.05
dy = 0.05

pMouseX = None
pMouseY = None
isDragging = False

a = 0


def polarToCart(r, t, f):
    x = r*math.cos(t)*math.sin(f)
    y = r*math.sin(t)*math.sin(f)
    z = r*math.cos(f)
    return x, y, z


def paraboloide(x, y):
    # Paraboloide Circular
    # return x**2 + y**2
    return x**2 - y**2
    # return x**2 + math.sqrt(abs(y))


v = []
subdivisoes = 10
dr = .1
dt = math.pi / subdivisoes

fi_min = 0
fi_max = math.pi
dfi = math.pi / (subdivisoes * 2)

r = 1

t = 0
while t <= 2*math.pi:
    fi = fi_min
    while fi <= fi_max:
        x, y, z = polarToCart(r, t, fi)
        v += [[x, y, z]]
        fi += dfi
    t += dt


def myMap(v, b1, t1, b2, t2):
    return (v - b1)/(t1 - b1) * (t2 - b2) + b2


def desenhaFuncao():

    glBegin(GL_TRIANGLES)
    i = 0
    for vertex in v[:(len(v)-subdivisoes*2 - 2)]:

        vs = vertex
        glColor3fv(vs)
        glVertex3fv(vs)

        vs = v[i+1]
        glColor3fv(vs)
        glVertex3fv(vs)

        vs = v[i+(subdivisoes*2)+2]
        glColor3fv(vs)
        glVertex3fv(vs)

        vs = vertex
        glColor3fv(vs)
        glVertex3fv(vs)

        vs = v[i+(subdivisoes*2)+1]
        glColor3fv(vs)
        glVertex3fv(vs)

        vs = v[i+(subdivisoes*2)+2]
        glColor3fv(vs)
        glVertex3fv(vs)

        i += 1
    glEnd()


def desenha():
    global a
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glPushMatrix()
    glRotatef(-90, 1, 0, 0)
    glRotatef(-a, 0, 0, 1)
    desenhaFuncao()
    glPopMatrix()

    # glPushMatrix()
    # glTranslatef(0, 0, 0)
    # glRotatef(-a, 0, 0, 1)
    # desenhaFuncao()
    # glPopMatrix()

    # glPushMatrix()
    # glRotatef(-90, 1, 0, 0)
    # glRotatef(-a, 0, 0, 1)
    # glColor3f(0, 0, 1)
    # glBegin(GL_POINTS)
    # for vx in v:
    #     glVertex3fv(vx)

    # glEnd()
    # glPopMatrix()

    # glPushMatrix()
    # glTranslatef(3, .5, 0.)
    # glBegin(GL_POINTS)
    # for vx in v[:n_points]:
    #     glVertex3fv(vx)

    # glEnd()
    # glPopMatrix()
    glutSwapBuffers()
    if not pause_rotation:
        a += 1
    return


def mouseFunc(btn, state, mouseX, mouseY):
    # btn -> 0 == botao esquerdo; 1 == botao rolagem; 2 == botao direito; 3 == rolagem para cima; 4 == rolagem para baixo
    global pMouseX
    global pMouseY
    global isDragging
    global pause_rotation
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
    if btn == 2 and state == 0:
        pause_rotation = not pause_rotation


def mouseDrag(x, y):
    if isDragging:
        global pMouseX
        global pMouseY
        glTranslatef(5 * (x-pMouseX)/width, 5 * -(y-pMouseY)/height, 0)
        pMouseX = x
        pMouseY = y


def handleKey(key, x, y):
    glutPostRedisplay()
    global n_points
    global pespective
    if key == b'o':
        n_points += 1

    if key == b'i':
        n_points = max(n_points - 1, 0)


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
    glutKeyboardFunc(handleKey)
    glutMainLoop()
