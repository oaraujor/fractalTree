import math

def vectorRotation(vector, angleDeg):
    cosAngle = math.cos(angleDeg)
    sinAngle = math.sin(angleDeg)

    rotatedVector = [
        (vector[0] * cosAngle) + ((vector[1]) * (-1) * (sinAngle)),
        ((vector[0] * sinAngle) + (vector[1] * cosAngle))
        ]

    return rotatedVector

def vectorScaling(vector, factor):
    scaledVector = []
    for element in vector:
        scaledVector.append(element * factor)
    return scaledVector
