from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import math


width, height = 1200.0, 800.0
rotation_delay = 10
screen_translate = 0.1

zoom = 0.1

pMouseX = None
pMouseY = None
isDragging = False

h = .5
v1 = []
v2 = []
r = 1
n_lados = 30
a = (2*math.pi)/n_lados

for i in range(0,n_lados):
    x = r*math.cos(a*i)
    y = 0    
    z = r*math.sin(a*i)
    v1 += [[x,y,z]]

for i in range(0,n_lados):
    x = r*math.cos(a*i)
    y = h  
    z = r*math.sin(a*i)
    v2 += [[x,y,z]]


def prisma():

    # PARTE DE CIMA
    glColor3f( 1.0, 0.0, 0.0 ) 
    glBegin(GL_POLYGON)
    
    for vertex in v1:
        glVertex3fv(vertex)

    glEnd()

    # MEIO
    glBegin(GL_QUAD_STRIP)
    glColor3f( 0.0, 1.0, 0.0 ) 
    i = 0
    for vertex in v1:
        glVertex3fv(vertex)
        glVertex3fv(v2[i])
        i += 1
    glVertex3fv(v1[0]) # É NECESSÁRIO PARA FECHAR O LADO DO PRISMA
    glVertex3fv(v2[0]) # É NECESSÁRIO PARA FECHAR O LADO DO PRISMA
    glEnd()

    # PARTE DE BAIXO
    glBegin(GL_POLYGON)
    glColor3f( 0.0, 0.0, 1.0 ) 
    for vertex in v2:
        glVertex3fv(vertex)

    glEnd()

def mouseFunc(btn, state, mouseX, mouseY):
    # btn -> 0 == botao esquerdo; 1 == botao rolagem; 2 == botao direito; 3 == rolagem para cima; 4 == rolagem para baixo
    global pMouseX
    global pMouseY
    global isDragging

    if btn == 3:
        glTranslatef(0,0,zoom)
    if btn == 4:
        glTranslatef(0,0,-zoom)
    if btn == 0 and state == 0:
        pMouseX = mouseX
        pMouseY = mouseY
        isDragging = True
    if btn == 0 and state == 1:
        isDragging = False

def mouseDrag(x,y):
    if isDragging:
        global pMouseX
        global pMouseY
        glTranslatef(5 * (x-pMouseX)/width ,5 * -(y-pMouseY)/height  ,0)
        pMouseX = x
        pMouseY = y



def desenha():
    global a
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glPushMatrix()
    glRotatef(a,0,1,0)
    glScalef(2,2,2)
    prisma()
    glPopMatrix()
    glutSwapBuffers()
    a += 1
    return

def timer(i):
    glutPostRedisplay()
    glutTimerFunc(rotation_delay,timer,1)

def handleKey(key, x, y):
    glutPostRedisplay()
    if(key == b'a'):
        glTranslatef(-screen_translate,0.0,0)
    if(key == b'w'):
        glTranslatef(0,screen_translate,0)
    if(key == b's'):
        glTranslatef(0,-screen_translate,0)
    if(key == b'd'):
        glTranslatef(screen_translate,0.0,0)


if __name__ == '__main__':
    # PROGRAMA PRINCIPAL
    a = 0

    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH | GLUT_MULTISAMPLE)
    glutInitWindowSize(int(width),int(height))
    glutCreateWindow("Piramide")
    glutDisplayFunc(desenha)
    glEnable(GL_MULTISAMPLE)
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.,0.,0.,1.)
    gluPerspective(45,width/height,0.1,100.0)
    glTranslatef(0.0,0.0,-8)
    glutTimerFunc(rotation_delay,timer,1)
    glutKeyboardFunc(handleKey)
    glutMouseFunc(mouseFunc)
    glutMotionFunc(mouseDrag)
    # glRotatef(45,1,1,1)
    glutMainLoop()