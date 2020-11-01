from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

width, height = 1200.0, 800.0
rotation_delay = 10
screen_translate = 0.1

zoom = 0.1

pMouseX = None
pMouseY = None
isDragging = False

def piramide():
    glBegin( GL_TRIANGLE_FAN )

    glColor3f( 1.0, 0.0, 0.0 ) 
    glVertex3f(0.0, 1.0, 0.)

    glColor3f( 0.0, 1.0, 0.0 ) 
    glVertex3f(-1., -1.0, 1.)
    
    glVertex3f(1., -1.0, 1.)

    glVertex3f(1., -1., -1.)
    
    glVertex3f(-1., -1., -1.)

    glVertex3f(-1., -1., 1.)

    glEnd()

    glBegin(GL_QUADS)
    
    glColor3f( 0.0, 0.0, 1.0 ) 
    glVertex3f(1.,-1.,1.)

    glVertex3f(1.,-1.,-1.)

    glVertex3f(-1.,-1.,-1.)

    glVertex3f(-1.,-1.,1.)

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
    # glRotatef(90,0,1,0)
    glRotatef(a,0,1,0)
    piramide()
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