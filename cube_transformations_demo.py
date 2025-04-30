#CUBE DEMO LINEAR ALGEBRA
#Code Written by Mike Montulet and Jennifer Greene

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

#Vertices of the cube.
cube_vertices = np.array([
    [1, 1, 1], #Vertex 0
    [1, 1, -1], #Vertex 1
    [1, -1, 1], #Vertex 2
    [1, -1, -1], #Vertex 3
    [-1, 1, 1], #Vertex 4
    [-1, 1, -1], #Vertex 5
    [-1, -1, 1], #Vertex 6
    [-1, -1, -1] #Vertex 7
], dtype=np.float32)

#Edges of the cube.
edges = [
    (0,1), (0,2), (0,4), (1, 3), (1,5),
    (2,3), (2,6), (3,7), (4,5), (4,6),
    (5,7), (6,7)
]

#Faces of the cube. (Each face is two triangles)
faces = [
    [0, 1, 5], [0, 4, 5], #Front Face
    [2, 3, 7], [2, 6, 7], #Back Face
    [4, 5, 7], [4, 6, 7], #Left Face
    [0, 1, 3], [0, 2, 3], #Right Face
    [0, 2, 6], [0, 4, 6], #Top Face
    [1, 3, 7], [1, 5, 7]  #Bottom Face
]

#Initialize 4x4 Transformation Matrices for each type of transformation. 
#By Default it is the Identity Matrix.
scale_matrix = np.identity(4, dtype = np.float32)
rotate_matrix = np.identity(4, dtype = np.float32)
translate_matrix = np.identity(4, dtype = np.float32)

#Function to actually draw the cube lines.
def draw_cube(vertices):
    glBegin(GL_LINES)

    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex][:3])
    glEnd()

def draw_fill_cube(vertices):
    glBegin(GL_TRIANGLES)

    for face in faces:
        for vertex in face:
            glVertex3fv(vertices[vertex][:3])
    glEnd()

#Function to rotate the cube. (Angle is in degrees)
def rotation_matrix(axis, angle):
    #Converts angle to radians
    angle = np.radians(angle)

    if axis == 'x': #Rotates about the x axis.
        return np.array([
            [1, 0, 0 ,0],
            [0, np.cos(angle), -np.sin(angle), 0],
            [0, np.sin(angle), np.cos(angle), 0],
            [0, 0, 0, 1]
        ], dtype = np.float32)
    elif axis == 'y': #Rotates about the y axis.
        return np.array([
            [np.cos(angle), 0, np.sin(angle), 0],
            [0, 1, 0, 0],
            [-np.sin(angle), 0, np.cos(angle), 0],
            [0, 0, 0, 1]
        ], dtype = np.float32)
    elif axis == 'z': #Rotates about the z axis.
        return np.array([
            [np.cos(angle), -np.sin(angle), 0, 0],
            [np.sin(angle), np.cos(angle), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ], dtype = np.float32)
    else: #Case for if axis given is invalid.
        return np.identity(4, dtype = np.float32)
    
#Function to resize (scale) the cube.
def scalar_matrix(x, y, z): 
    return np.array([
        [x, 0, 0, 0],
        [0, y, 0, 0],
        [0, 0, z, 0],
        [0, 0, 0, 1]
    ], dtype = np.float32)

#Function to move (translate) the cube.
def translation_matrix(x, y, z):
    return np.array([
        [1, 0, 0, x],
        [0, 1, 0, y],
        [0, 0, 1, z],
        [0, 0, 0, 1]
    ], dtype = np.float32)

#Applies the transformation to each vertex of the cube.
def apply_transformation(vertices, matrix):
    homogeneous_vertices = np.hstack((vertices, np.ones((vertices.shape[0], 1))))
    transformed_cube = homogeneous_vertices @ matrix.T #T is the transpose.
    return transformed_cube

#Main Function.
def main():
    global scale_matrix
    global rotate_matrix
    global translate_matrix

    #Starts the pygame window and viewing perspective.
    pygame.init()
    pygame.font.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -10)

    clock = pygame.time.Clock()

    #Boolean to determine which view to have.
    isSolid = False

    isPlaying = True

    while isPlaying:
        deltaTime = clock.tick(60) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isPlaying = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                isSolid = not isSolid
                
        keys = pygame.key.get_pressed()

        #Arrow keys control rotation of cube. Rotation is in world space.
        if(keys[pygame.K_LEFT]):
            rotate_matrix = rotation_matrix('y', -90 * deltaTime) @ rotate_matrix
        elif(keys[pygame.K_RIGHT]):
            rotate_matrix = rotation_matrix('y', 90 * deltaTime) @ rotate_matrix
        elif(keys[pygame.K_UP]):
            if(keys[pygame.K_LSHIFT]):
                rotate_matrix = rotation_matrix('z', -90 * deltaTime) @ rotate_matrix
            else:
                rotate_matrix = rotation_matrix('x', -90 * deltaTime) @ rotate_matrix
        elif(keys[pygame.K_DOWN]):
            if(keys[pygame.K_LSHIFT]): 
                rotate_matrix = rotation_matrix('z', 90 * deltaTime) @ rotate_matrix
            else:
                rotate_matrix = rotation_matrix('x', 90 * deltaTime) @ rotate_matrix
        #WASD control translation of the cube.
        elif(keys[pygame.K_w]):
            if(keys[pygame.K_LSHIFT]):
                translate_matrix = translate_matrix @ translation_matrix(0, 0, 1 * deltaTime) 
            else:
                translate_matrix = translate_matrix @ translation_matrix(0, 1 * deltaTime, 0)
        elif(keys[pygame.K_s]):
            if(keys[pygame.K_LSHIFT]):
                translate_matrix = translate_matrix @ translation_matrix(0, 0, -1 * deltaTime)
            else:
                translate_matrix = translate_matrix @ translation_matrix(0, -1 * deltaTime, 0)
        elif(keys[pygame.K_a]):
            translate_matrix = translate_matrix @ translation_matrix(-1 * deltaTime, 0, 0)
        elif(keys[pygame.K_d]):
            translate_matrix = translate_matrix @ translation_matrix(1 * deltaTime, 0, 0)
        # + and - keys scale the cube. Press x,y,z before to only scale that axis.
        #Scaling is in local space.
        elif(keys[pygame.K_x]):
            if(keys[pygame.K_EQUALS]):
                scale_factor = 1 + 0.5 * deltaTime
                scale_matrix = scale_matrix @ scalar_matrix(scale_factor, 1, 1)
            elif(keys[pygame.K_MINUS]):
                scale_factor = 1 - 0.5 * deltaTime
                scale_matrix = scale_matrix @ scalar_matrix(scale_factor, 1, 1)
        elif(keys[pygame.K_y]):
            if(keys[pygame.K_EQUALS]):
                scale_factor = 1 + 0.5 * deltaTime
                scale_matrix = scale_matrix @ scalar_matrix(1, scale_factor, 1)
            elif(keys[pygame.K_MINUS]):
                scale_factor = 1 - 0.5 * deltaTime
                scale_matrix = scale_matrix @ scalar_matrix(1, scale_factor, 1)
        elif(keys[pygame.K_z]):
            if(keys[pygame.K_EQUALS]):
                scale_factor = 1 + 0.5 * deltaTime
                scale_matrix = scale_matrix @ scalar_matrix(1, 1, scale_factor)
            elif(keys[pygame.K_MINUS]):
                scale_factor = 1 - 0.5 * deltaTime
                scale_matrix = scale_matrix @ scalar_matrix(1, 1, scale_factor)
        elif(keys[pygame.K_EQUALS]):
            scale_factor = 1 + 0.5 * deltaTime
            scale_matrix = scale_matrix @ scalar_matrix(scale_factor, scale_factor, scale_factor)
        elif(keys[pygame.K_MINUS]):
            scale_factor = 1 - 0.5 * deltaTime
            scale_matrix = scale_matrix @ scalar_matrix(scale_factor, scale_factor, scale_factor)
        #Resets all transformations
        elif(keys[pygame.K_r]): 
            scale_matrix = np.identity(4, dtype = np.float32)
            rotate_matrix = np.identity(4, dtype = np.float32)
            translate_matrix = np.identity(4, dtype = np.float32)

        
        
        #Add different effects when the cube is solid.
        if(isSolid):
            glEnable(GL_DEPTH_TEST)
            glEnable(GL_POLYGON_OFFSET_FILL)
            glPolygonOffset(1.0, 1.0)  # Push solid faces back slightly
        else:
            glDisable(GL_DEPTH_TEST)
            glDisable(GL_POLYGON_OFFSET_FILL)

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        #Apply the transformations in specific order. Scale, Rotate, then Translate
        final_matrix = translate_matrix @ rotate_matrix @ scale_matrix

        #Apply all of the transformations to the cube.
        transformed_cube_vertices = apply_transformation(cube_vertices, final_matrix)

        #Actually draw the cube on the screen.
        if(isSolid):
            glColor3f(1, 1, 1)
            draw_fill_cube(transformed_cube_vertices)
            glColor3f(0.0, 0.0, 0.0)
            draw_cube(transformed_cube_vertices)
        else:
            glColor3f(1, 1, 1)
            draw_cube(transformed_cube_vertices)
        pygame.display.flip() #Updates the entire screen.
        pygame.display.set_caption("Cube Transformations") #Changes name of pygame window.

    pygame.quit()

if __name__ == "__main__":

    main()
