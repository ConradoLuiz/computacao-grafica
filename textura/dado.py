from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
import png

# Some api in the chain is translating the keystrokes to this octal string
# so instead of saying: ESCAPE = 27, we use the following.
ESCAPE = '\033'

# Number of the glut window.
window = 0

# Rotations for cube.
xrot = yrot = zrot = 0.0
dx = 1
dy = 1
dz = 1

# texture = []


def LoadTextures():
    global texture
    texture = glGenTextures(1)

    ################################################################################
    glBindTexture(GL_TEXTURE_2D, texture)
    reader = png.Reader(filename='./dado.png')
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
    ################################################################################

    ################################################################################
#     glBindTexture(GL_TEXTURE_2D, texture[1])
#     reader = png.Reader(filename='./textura.png')
#     w, h, pixels, metadata = reader.read_flat()
#     if(metadata['alpha']):
#         modo = GL_RGBA
#     else:
#         modo = GL_RGB
#     glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
#     glTexImage2D(GL_TEXTURE_2D, 0, modo, w, h, 0, modo,
#                  GL_UNSIGNED_BYTE, pixels.tolist())
# #    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
# #    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
#     glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
#     glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
#     glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
#     glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
#     glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    ################################################################################


def InitGL(Width, Height):
    LoadTextures()
    glEnable(GL_TEXTURE_2D)
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)
    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)


def ReSizeGLScene(Width, Height):
    if Height == 0:
        Height = 1
    glViewport(0, 0, Width, Height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)


def DrawGLScene():
    global xrot, yrot, zrot, dx, dy, dz, texture

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glClearColor(0.5, 0.5, .5, 1.0)
    glTranslatef(0.0, 0.0, -5.0)
    glRotatef(xrot, 1.0, 0.0, 0.0)
    glRotatef(yrot, 0.0, 1.0, 0.0)
    glRotatef(zrot, 0.0, 0.0, 1.0)

    # DAR BIND ANTES DE DECLARAR A ESTRUTURA
    # TEXTURE[0] == dado
    glBindTexture(GL_TEXTURE_2D, texture)
    glBegin(GL_QUADS)

    # Front Face
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-1.0, -1.0,  1.0)
    glTexCoord2f(0.0, .5)
    glVertex3f(1.0, -1.0,  1.0)
    glTexCoord2f(1.0/3.0, 1.0/2.0)
    glVertex3f(1.0,  1.0,  1.0)
    glTexCoord2f(1.0/3.0, 0.0)
    glVertex3f(-1.0,  1.0,  1.0)

    # Back Face
    glTexCoord2f(.66, .5)
    glVertex3f(-1.0, -1.0, -1.0)
    glTexCoord2f(.66, 1.0)
    glVertex3f(-1.0,  1.0, -1.0)
    glTexCoord2f(1., 1.0)
    glVertex3f(1.0,  1.0, -1.0)
    glTexCoord2f(1, .5)
    glVertex3f(1.0, -1.0, -1.0)

    # Top Face
    glTexCoord2f(0, .5)
    glVertex3f(-1.0,  1.0, -1.0)
    glTexCoord2f(0.0, 1)
    glVertex3f(-1.0,  1.0,  1.0)
    glTexCoord2f(.33, 1.0)
    glVertex3f(1.0,  1.0,  1.0)
    glTexCoord2f(.33, .5)
    glVertex3f(1.0,  1.0, -1.0)

    # Bottom Face
    glTexCoord2f(.66, 0)
    glVertex3f(-1.0, -1.0, -1.0)
    glTexCoord2f(1, 0.0)
    glVertex3f(1.0, -1.0, -1.0)
    glTexCoord2f(1, .5)
    glVertex3f(1.0, -1.0,  1.0)
    glTexCoord2f(.66, .5)
    glVertex3f(-1.0, -1.0,  1.0)

    # Right face
    glTexCoord2f(.66, 1.0)
    glVertex3f(1.0, -1.0, -1.0)
    glTexCoord2f(.66, .5)
    glVertex3f(1.0,  1.0, -1.0)
    glTexCoord2f(.33, .5)
    glVertex3f(1.0,  1.0,  1.0)
    glTexCoord2f(.33, 1)
    glVertex3f(1.0, -1.0,  1.0)

    # Left Face
    glTexCoord2f(.33, .5)
    glVertex3f(-1.0, -1.0, -1.0)
    glTexCoord2f(.33, 0)
    glVertex3f(-1.0, -1.0,  1.0)
    glTexCoord2f(.66, 0)
    glVertex3f(-1.0,  1.0,  1.0)
    glTexCoord2f(.66, .5)
    glVertex3f(-1.0,  1.0, -1.0)

    glEnd()
    # Done Drawing The Cube

    # xrot = xrot + dx                 # X rotation
    # yrot = yrot + dy                 # Y rotation
    # zrot = zrot + dz                 # Z rotation

    glutSwapBuffers()


def keyPressed(tecla, x, y):
    global dx, dy, dz
    if tecla == ESCAPE:
        glutLeaveMainLoop()
    elif tecla == b'x' or tecla == b'X':
        dx = 0.5
        dy = 0
        dz = 0
    elif tecla == b'y' or tecla == b'Y':
        dx = 0
        dy = 0.5
        dz = 0
    elif tecla == b'z' or tecla == b'Z':
        dx = 0
        dy = 0
        dz = 0.5


def teclaEspecialPressionada(tecla, x, y):
    global xrot, yrot, zrot, dx, dy, dz

    if tecla == 100:
        # ESQUERDA
        yrot -= dy
    elif tecla == 102:
        # DIREITA
        yrot += dy
    elif tecla == 101:
        # CIMA
        xrot -= dx
    elif tecla == 103:
        # BAIXO
        xrot += dx


def main():
    global window

    w, h = 640, 480

    glutInit(sys.argv)

    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)

    # get a 640 x 480 window
    glutInitWindowSize(w, h)

    # the window starts at the upper left corner of the screen
    glutInitWindowPosition(200, 200)

    window = glutCreateWindow("Textura")

    glutDisplayFunc(DrawGLScene)

    # When we are doing nothing, redraw the scene.
    glutIdleFunc(DrawGLScene)

    # Register the function called when our window is resized.
    glutReshapeFunc(ReSizeGLScene)

    # Register the function called when the keyboard is pressed.
    glutKeyboardFunc(keyPressed)

    glutSpecialFunc(teclaEspecialPressionada)

    # Initialize our window.
    InitGL(w, h)

    # Start Event Processing Engine
    glutMainLoop()


# Print message to console, and kick off the main to get it rolling.
if __name__ == "__main__":
    print("Hit ESC key to quit.")
    main()
