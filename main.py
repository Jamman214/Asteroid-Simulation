from turtle import distance
import pygame
import math
import random
import numpy as np
from collisions import timeAtTouch

debugMode = 3
scale = 100
fps = 50
adaptiveScale = 1
#G = 0.0000000000667408
G=0.01

class coordinate():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class rock():
    density = 1
    hit = False
    unlocked = True
    drawPosition = [0,0]
    acceleration=[0,0]
    def __init__(self, pos, radius, velocity):
        self.velocity=velocity
        if radius<1:
            radius = 1
        self.position = [pos[0], pos[1]]
        self.colour = (0,0,0)
        #self.mass = random.randint(5,100)
        self.radius = radius
        self.mass = ((4/3)*math.pi*self.radius**3) * self.density
    
    def draw(self, font):
        print(self.position)
        self.drawPosition = np.add(np.divide(self.position, adaptiveScale), offset)
        if self.unlocked:
            pygame.draw.circle(screen, self.colour, self.drawPosition, self.radius/adaptiveScale)
            if debugMode > 0:
                pygame.draw.line(screen, (0,0,255), self.drawPosition, np.add(self.drawPosition, np.divide(np.multiply(self.velocity,100), adaptiveScale)), 1)
                if debugMode > 1:
                    text = font.render(str(round(self.position[0],9)) + " , " + str(round(self.position[1],9)), True, "red")
                    textRect = text.get_rect()
                    textRect.center = (self.drawPosition[0], self.drawPosition[1])
                    screen.blit(text, textRect)
                    if debugMode > 2:
                        text = font.render(str(round(self.mass)), False, "green")
                        textRect = text.get_rect()
                        textRect.center = (self.drawPosition[0], self.drawPosition[1]+10)
                        screen.blit(text, textRect)
        else:
            pygame.draw.circle(screen, [0,255,0], self.drawPosition, self.radius/adaptiveScale)
            
    def distanceTo(self, position):
        return math.sqrt((position[0] - self.position[0])**2 + (position[1] - self.position[1])**2)
    
    def vectorTo(self, position):
        return normalise([position[0] - self.position[0], position[1] - self.position[1]])

def vectorTo(pos1, pos2):
        return [pos2[0] - pos1[0], pos2[1] - pos1[1]]
    
def distanceBetween(v1, v2):
    temp = np.subtract(v1,v2)
    return math.sqrt(temp[0]**2 + temp[1]**2) * adaptiveScale

def normalise(v):
    norm = np.linalg.norm(v)
    if norm == 0: 
       return v
    return v / norm

def gravity(asteroids):
    for asteroid in asteroids:
        asteroid.acceleration = [0,0]
    for i in range(len(asteroids)-1):
        for asteroid in asteroids[i+1:]:
            distance = asteroids[i].distanceTo(asteroid.position)
            vector = asteroids[i].vectorTo(asteroid.position)
            acceleration = np.divide(vector * G, ((distance**2)))
            asteroids[i].acceleration = np.add(asteroids[i].acceleration, np.multiply(acceleration, asteroid.mass))
            asteroid.acceleration = np.add(asteroid.acceleration, np.multiply(np.multiply(acceleration,-1), asteroids[i].mass))
                
def COM(asteroids):
    total = 0;pos=[0,0]
    for asteroid in asteroids:
        pos = np.add(pos, np.multiply(asteroid.drawPosition, asteroid.mass))
        total += asteroid.mass
    if total != 0:
        return np.divide(pos, total)
    return offset
        
def findScale(asteroids):
    temp = 1
    for asteroid in asteroids:
        temp2 = abs((asteroid.position[0]+100*(asteroid.acceleration[0])) / offset[0])
        if temp2 > temp:
            temp = temp2
        temp2 = abs((asteroid.position[1]+100*(asteroid.acceleration[1])) / offset[1])
        if temp2 > temp:
            temp = temp2
    return temp * 1.5

def dispDebugInfo(debugMode, font, massCenter):
    if debugMode > 0:
        text = font.render(str(round(massCenter[0],9)) + " , " + str(round(massCenter[1],9)), True, "green")
        textRect = text.get_rect()
        textRect.center = (700, 750)
        screen.blit(text, textRect)
        pygame.draw.circle(screen, "red", massCenter, 5)
        
def bubbleSortTimes(inpArray, pos):
    print(inpArray)
    for i in range(len(inpArray)):
        for j in range(len(inpArray)-1 - i):
            if inpArray[j][pos] > inpArray[j+1][pos]:
                temp = inpArray[j]
                inpArray[j] = inpArray[j+1]
                inpArray[j+1] = temp
    return inpArray

def handleCollisions(asteroids):
    collisions = []
    length = len(asteroids) # length of asteroids
    for i in range(length - 1): # Loops over pairs of asteroids
        for j in range(i+1, length):
            tempBool, tempFloat = timeAtTouch(asteroids[i], asteroids[j]) # Calculates the time in their trajectory at which they touch
            if tempBool:
                collisions.append([tempFloat, i, j]) # Builds up array of collisions
    if len(collisions) > 1:
        collisions = bubbleSortTimes(collisions, 0)
        max = len(collisions)
        cur = 0
        pos1 = 0
        while pos1 < max:
            cur = collisions[pos1][1:]
            pos2 = pos1+1
            while pos2 < max:
                if (collisions[pos2][1] in cur) or (collisions[pos2][2] in cur):
                    collisions.pop(pos2)
                    max -= 1
                else:
                    pos2 += 1
            pos1 += 1
    for crash in collisions:
        asteroids[crash[1]].unlocked = False
        asteroids[crash[2]].unlocked = False
        asteroids[crash[1]].time = crash[0]
        asteroids[crash[2]].time = crash[0]


def main():
    global adaptiveScale
    global offset
    mouseUp = True
    asteroids = []
    pygame.display.set_caption("Python Boid Sim")
    font = pygame.font.Font('freesansbold.ttf', 10)
    clock = pygame.time.Clock()
    done = False
    massCenter = offset
    placeFlag = False; placePos = [-1,1]; radius = 0; velFlag = False
    playing = True
    while not done:
        screen.fill((255,255,255))
        
        #Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN and mouseUp:
                if placeFlag:
                    radius = distanceBetween(pygame.mouse.get_pos(), placePos)
                    placeFlag = False
                    velFlag = True
                elif velFlag:
                    asteroids.append(rock(np.subtract(placePos, offset) * adaptiveScale, radius, np.divide(vectorTo(placePos, pygame.mouse.get_pos()), 100/adaptiveScale)))
                    velFlag = False
                else:
                    placeFlag = True; placePos = pygame.mouse.get_pos()
                mouseUp = False
            if event.type == pygame.MOUSEBUTTONUP and not mouseUp:
                mouseUp = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_0:
                    adaptiveScale = findScale(asteroids)
                elif event.key == pygame.K_1:
                    playing = not playing
                else:
                    print("test")
        
        #Visual display for placing asteroids
        if placeFlag:
            pygame.draw.circle(screen, [255,0,0], placePos, np.divide(distanceBetween(placePos, pygame.mouse.get_pos()), adaptiveScale), 3)
        elif velFlag:
            pygame.draw.circle(screen, [255,0,0], placePos, np.divide(radius, adaptiveScale), 3)
            pygame.draw.line(screen, [100,0,100], placePos, pygame.mouse.get_pos(), 3)
        
        #Velocity and acceleration calculations
        if playing:
            
            # Calculate the gravity every frame
            gravity(asteroids)
            
            #Calculate new velocities for asteroids
            for asteroid in asteroids:
                if asteroid.unlocked:
                    asteroid.velocity = np.add(asteroid.velocity, asteroid.acceleration)
                else:
                    asteroid.acceleration = [0,0]
                    asteroid.velocity = [0,0]
            
            #Calculate times at collisions 
            handleCollisions(asteroids)
                        
            #Calculate position using time and velocity 
            for asteroid in asteroids:
                if asteroid.unlocked:
                    asteroid.position = np.add(asteroid.position, asteroid.velocity)
                else:
                    if not asteroid.hit:
                        asteroid.position = np.add(asteroid.position, np.multiply(asteroid.velocity, asteroid.time))
                        asteroid.hit = True
        
        #Draws asteroids
        for asteroid in asteroids:
            asteroid.draw(font)
        
        #Display center of mass
        massCenter = COM(asteroids)
        dispDebugInfo(debugMode, font, massCenter)
        
        #****   Game Loop End ****
        pygame.display.flip()
        clock.tick(fps)

screenSize = [1400, 800]
offset = np.divide(screenSize, 2)
pygame.init()
screen = pygame.display.set_mode(screenSize)
main()

