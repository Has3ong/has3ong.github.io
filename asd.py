from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


m_xTranslation, m_yTranslation, m_zTranslation = 0.0, 0.0, -10.0
m_xRotation, m_yRotation, m_zRotation = 0.0, 0.0, 0.0
m_xScaling, m_yScaling, m_zScaling = 1.0, 1.0, 1.0
x_last, y_last = 0, 0


def Draw():
    size = [2.0, 2.0, 2.0]

    point1 = [size[0] / 2.0, size[1] / 2.0, size[2] / -2.0]
    point2 = [size[0] / 2.0, size[1] / 2.0, size[2] / 2.0]
    point3 = [size[0] / 2.0, size[1] / -2.0, size[2] / 2.0]
    point4 = [size[0] / 2.0, size[1] / -2.0, size[2] / -2.0]
    point5 = [size[0] / -2.0, size[1] / -2.0, size[2] / 2.0]
    point6 = [size[0] / -2.0, size[1] / 2.0, size[2] / 2.0]
    point7 = [size[0] / -2.0, size[1] / 2.0, size[2] / -2.0]
    point8 = [size[0] / -2.0, size[1] / -2.0, size[2] / -2.0]

    glBegin(GL_QUADS)

    glVertex3fv(point1)  # TOP
    glVertex3fv(point2)
    glVertex3fv(point6)
    glVertex3fv(point7)

    glVertex3fv(point3)  # Bottom
    glVertex3fv(point4)
    glVertex3fv(point8)
    glVertex3fv(point5)

    glVertex3fv(point2)  # Front
    glVertex3fv(point3)
    glVertex3fv(point5)
    glVertex3fv(point6)

    glVertex3fv(point7)  # Back
    glVertex3fv(point8)
    glVertex3fv(point4)
    glVertex3fv(point1)

    glVertex3fv(point6)  # Left
    glVertex3fv(point5)
    glVertex3fv(point8)
    glVertex3fv(point7)

    glVertex3fv(point1)  # Right
    glVertex3fv(point4)
    glVertex3fv(point3)
    glVertex3fv(point2)

    glEnd()

def initFun():
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glShadeModel(GL_FLAT)

def displayFun():
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(1.0, 1.0, 1.0)
    glLoadIdentity()
    gluLookAt(0.0, 0.0, 5.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    glPushMatrix()
    glTranslatef(m_xTranslation, m_yTranslation, m_zTranslation)
    glRotatef(m_xRotation, 1.0, 0.0, 0.0)
    glRotatef(m_yRotation, 0.0, 1.0, 0.0)
    glRotatef(m_zRotation, 0.0, 0.0, 1.0)
    glScalef(m_xScaling, m_yScaling, m_zScaling)
    Draw()
    glPopMatrix()
    glFlush()
    glutPostRedisplay()

def reshapeFunc(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glFrustum(-1.0, 1.0, -1.0, 1.0, 1.5, 20.0)
    glMatrixMode(GL_MODELVIEW)

def MyMouseClick(Button, State, x, y):
    global m_zTranslation
    print(Button, State, x, y)
    if Button == 3:
        m_zTranslation += 1.0
    elif Button == 4:
        m_zTranslation += -1.0
    else:
        x_last, y_last = x, y

def MyMouseMove(x, y):
    global m_xRotation, m_yRotation, x_last, y_last
    m_speedRotation = (1.0 / 100.0)
    m_xRotation -= (float)(y - y_last) * m_speedRotation
    m_yRotation += (float)(x - x_last) * m_speedRotation


if __name__=='__main__':
    glutInit()
    glutInitWindowSize(500, 500)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"TEST")
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutDisplayFunc(displayFun)
    glutReshapeFunc(reshapeFunc)

    glutMouseFunc(MyMouseClick)
    glutMotionFunc(MyMouseMove)

    initFun()
    glutMainLoop()
