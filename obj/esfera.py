import math
import png
from ply import *
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


def LoadTextures():
    global texture
    texture = glGenTextures(1)

    ################################################################################
    glBindTexture(GL_TEXTURE_2D, texture)
    reader = png.Reader(filename='./terra.png')
    w, h, pixels, metadata = reader.read_flat()
    if(metadata['alpha']):
        modo = GL_RGBA
    else:
        modo = GL_RGB
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glTexImage2D(GL_TEXTURE_2D, 0, modo, w, h, 0, modo,
                 GL_UNSIGNED_BYTE, pixels.tolist())
#   glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
#   glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)


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
subdivisoes = 50
dr = .1
dt = math.pi / subdivisoes

fi_min = 0
fi_max = math.pi
dfi = math.pi / (subdivisoes * 2)

r = 1

t = 0
t_max = 2*math.pi


def terra():
    id_terra = glGenLists(1)

    glNewList(id_terra, GL_COMPILE)
    glFrontFace(GL_CCW)

    glBindTexture(GL_TEXTURE_2D, texture)
    glBegin(GL_TRIANGLES)

    t = 0
    while t <= t_max:
        fi = fi_min
        while fi <= fi_max:
            x, y, z = polarToCart(r, t, fi)
            vertex = [x, y, z]

            # PRIMEIRO TRIANGULO ------------------------------
            glTexCoord2f(t/t_max, fi/fi_max)
            glVertex3fv(vertex)

            glTexCoord2f(t/t_max, (fi+dfi)/fi_max)
            glVertex3fv(polarToCart(r, t, fi+dfi))

            glTexCoord2f((t+dt)/t_max, (fi+dfi)/fi_max)
            glVertex3fv(polarToCart(r, t+dt, fi+dfi))

            # SEGUNDO TRIANGULO --------------------------------

            glTexCoord2f(t/t_max, fi/fi_max)
            glVertex3fv(vertex)

            glTexCoord2f((t+dt)/t_max, fi/fi_max)
            glVertex3fv(polarToCart(r, t+dt, fi))

            glTexCoord2f((t+dt)/t_max, (fi+dfi)/fi_max)
            glVertex3fv(polarToCart(r, t+dt, fi+dfi))

            # -------------------------------------------------

            fi += dfi
        t += dt
    glEnd()
    # glDisable(GL_TEXTURE_2D)
    glEndList()
    return id_terra


def myMap(v, b1, t1, b2, t2):
    return (v - b1)/(t1 - b1) * (t2 - b2) + b2


def desenha():
    global a
    global terra
    global bunny
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glPushMatrix()
    glRotatef(-90, 1, 0, 0)
    glRotatef(-a, 0, 0, 1)
    glCallList(terra)
    glPopMatrix()

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


def InitGL(Width, Height):
    global terra
    LoadTextures()
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_MULTISAMPLE)
    glClearDepth(1.0)
    glEnable(GL_DEPTH_TEST)
    glClearColor(0., 0., 0., 1.)
    glShadeModel(GL_SMOOTH)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, Width/Height, 0.1, 100.0)
    glTranslatef(0.0, -0.4, -6)
    terra = terra()


def timer(i):
    glutPostRedisplay()
    glutTimerFunc(rotation_delay, timer, 1)


if __name__ == '__main__':
    # PROGRAMA PRINCIPAL
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA |
                        GLUT_DEPTH | GLUT_MULTISAMPLE)
    glutInitWindowSize(int(width), int(height))
    window = glutCreateWindow("Paraboloide")
    glutDisplayFunc(desenha)

    InitGL(width, height)

    glutTimerFunc(rotation_delay, timer, 1)
    glutMouseFunc(mouseFunc)
    glutMotionFunc(mouseDrag)
    glutKeyboardFunc(handleKey)
    glutMainLoop()
