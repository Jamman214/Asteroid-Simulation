import numpy as np
import math
#import main


def timeAtTouch(obj1, obj2):
    t2 = ( (obj1.velocity[0]**2 + obj1.velocity[1]**2) + (obj2.velocity[0]**2 + obj2.velocity[1]**2) - (2 * (obj1.velocity[0] * obj2.velocity[0]) + (obj1.velocity[1] * obj2.velocity[1])) )
    t1 = 2 * ( (obj1.velocity[0] * (obj1.position[0] - obj2.position[0])) + (obj1.velocity[1] * (obj1.position[1] - obj2.position[1])) + (obj2.velocity[0] * (obj2.position[0] - obj1.position[0])) + (obj2.velocity[1] * (obj2.position[1] - obj1.position[1])) )
    t0 = ( (obj1.position[0]**2 + obj1.position[1]**2) + (obj2.position[0]**2 + obj2.position[1]**2) - 2 * ( (obj1.position[0] * obj2.position[0]) + (obj1.position[1] * obj2.position[1])) )
    t0 -= (obj1.radius + obj2.radius)**2
    discriminant = t1**2 - (4*t2*t0)
    if discriminant < 0:
        return False, None
    root1 = (-t1-math.sqrt(discriminant)) / (2*t2)
    root2 = (-t1+math.sqrt(discriminant)) / (2*t2)
    if root1 > root2:
        temp = root1
        root1 = root2
        root2 = temp
    if 0 <= root1 <= 1:
        return True, root1
    if 0 <= root2 <= 1:
        return True, root2
    return False, None

def resolveFor(obj1, obj2, axis):
        t2 = (0.5 * obj1.mass) + ( (0.5 * obj2.mass) * (obj1.mass**2 / obj2.mass**2))
        t1 = ( (0.5 * obj2.mass) * (-obj1.mass * ( (obj1.mass * obj1.velocity[axis]) + (obj2.mass * obj2.velocity[axis]) )))
        t0 = ( (obj1.mass**2 - (0.5 * obj1.mass)) * obj1.velocity[axis]**2 ) + ( (obj2.mass**2 - (0.5 * obj2.mass)) * obj2.velocity[axis]**2 ) + (obj1.mass * obj1.velocity[axis] * obj2.mass * obj2.velocity[axis])
        return t2,t1,t0

def normalise(v):
    norm = np.linalg.norm(v)
    if norm == 0: 
       return v
    return v / norm

def collisionForces(obj1, obj2):
    tangent = normalise([obj2.position[1] - obj1.position[1], obj2.position[0] - obj1.position[0]])
    tangent = [-tangent[1], tangent[0]]
    relativeVelocity = [obj2.velocity[0] - obj1.velocity[0], obj2.velocity[1] - obj1.velocity[1]]
    length = np.dot(relativeVelocity, tangent)
    paraTangentComponent = np.multiply(tangent, length)
    perpTangentComponent = np.subtract(paraTangentComponent, relativeVelocity)
    obj1.velocity = np.add(obj1.velocity, np.multiply(perpTangentComponent, 2))
    obj2.velocity = np.subtract(obj2.velocity, np.multiply(perpTangentComponent, 2))
    
#def cosCol(obj1, obj2):
#    lineBetween = 
'''
a = main.rock([10,0], 0); a.velocity = [0,0]
b = main.rock([0,0], 0); b.velocity = [10,0]
print(timeAtTouch(a, b))
'''
def attempt(obj1, obj2):
    one = np.multiply(obj1.velocity,obj1.mass)
    two = np.multiply(obj2.velocity,obj2.mass)
    distance = math.sqrt((one[0]-two[0]))
    norm = np.array(-one[1], one[0])