
from math import dist
from random import randint


heightmap = [[1, 1, 1, 1, 2, 3, 3, 2, 2, 2, 3, 3, 3, 3, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 5], [1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 3, 3, 2, 1, 2, 2, 2, 1, 1, 1], [1, 2, 2, 2, 2, 2, 2, 2, 3, 2, 2, 3, 3, 3, 4, 4, 3, 3, 2, 2, 2, 2, 2, 2, 1], [2, 2, 2, 2, 2, 1, 2, 2, 3, 3, 2, 2, 3, 3, 4, 4, 4, 3, 2, 2, 3, 3, 2, 2, 1], [2, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 4, 4, 3, 3, 2, 3, 3, 3, 3, 3, 2], [3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 3, 3, 3, 4, 4, 4, 3, 3, 3, 3, 4, 3, 3, 2], [2, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 3, 4, 4, 4, 4, 4, 3, 3, 3, 4, 4, 3, 3, 2], [2, 2, 2, 3, 3, 3, 2, 2, 2, 2, 2, 3, 3, 4, 3, 4, 3, 3, 3, 3, 3, 3, 3, 3, 2], [2, 3, 2, 2, 3, 3, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 3, 3, 2, 2], [3, 3, 3, 3, 3, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2], [2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 1, 1], [2, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 2, 2, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 1, 1], [2, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 3, 2, 2, 2, 2, 2, 2, 2, 3, 2, 2, 1], [2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1], [1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 2, 2, 2, 1], [1, 1, 1, 1, 2, 2, 1, 1, 1, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 3, 2, 2, 2, 2], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2], [2, 1, 1, 1, 1, 1, 5, 5, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], [1, 2, 1, 1, 1, 1, 5, 5, 1, 1, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2], [1, 1, 1, 1, 1, 5, 5, 5, 5, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 2, 1, 1], [1, 1, 1, 1, 1, 5, 5, 5, 5, 5, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1], [5, 1, 1, 5, 5, 5, 5, 5, 5, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1], [5, 1, 1, 5, 5, 5, 5, 5, 5, 1, 1, 2, 2, 2, 3, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1], [5, 1, 1, 5, 5, 5, 5, 5, 1, 1, 1, 2, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 5]]


sensor_locations = []
for i in range(0,100):
    sensor_locations.append([randint(0,25),randint(0,25)])

total = 0
minnumber = 100000
value = 0

guessmap = []

for row in heightmap:
    rowi = heightmap.index(row)
    print (row)
    guesscol = []
    for col in row:
        coli = row.index(col)
        for j in sensor_locations:
            distance = pow((rowi-j[0])**2+(coli-j[1])**2,1/2)
            if distance < 10:
                total =+ col
                minnumber = min(distance,minnumber)

total = 0
value = 0
number = 0
guessmap = []

for row in heightmap:
    rowi = heightmap.index(row)
    print (row)
    guesscol = []
    for col in row:
        coli = row.index(col)
        for j in sensor_locations:
            distance = pow((rowi-j[0])**2+(coli-j[1])**2,1/2)
            if distance < 10:
                total =+ col
                number =+ distance - minnumber
                print("distance weight", number)
        print(value)
        value = total / max(1,number)
        guesscol.append(round(value,1))
    guessmap.append(guesscol)
    
print (guessmap)


