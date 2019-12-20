import random
from math import *

twenty_grid_sw = []
twenty_grid_ne = []

for x in range(10,101,20):
    for y in range(10,201,20):
        twenty_grid_sw.append((x,y))
        twenty_grid_ne.append((x+100, y))



fromsample = random.sample(twenty_grid_sw, 20)
tosample = random.sample(twenty_grid_ne, 20)

trips = []

for i in range(int(len(fromsample))):
    trips.append((fromsample.pop(), tosample.pop()))

for trip in trips:
    print(str(trip) + ',')



print("ALALALLALALA NEW TRIPS")

## new one lul

zones = [[] for _ in range(8)]

for x in range(10,101,20):
    for y in range(10,201,20):
        for i in range(len(zones)):
            zones[i].append((x+(200*i), y+(200*i)))


zonesamples = []

for zone in zones:
    zonesamples.append(random.sample(zone, 6))

trips = []

for zone in zonesamples:
    for i in range(int(len(zone)/2)):
        trips.append((zone.pop(), zone.pop()))

for trip in trips:
    print(str(trip) + ',')


print("ALALALLALALA NEW TRIPS")

## new one lul


trips = []

for i in range(10,21,10):
    trips.append(((i, 10), (i, 10+10)))

    trips.append(((i+100, 10), (i+100, 10+10)))

    trips.append(((i+100, 10+100), (i+100, 10+110)))

    trips.append(((i, 10+100), (i, 10+110)))

for trip in trips:
    print(str(trip) + ',')




print("SPOKES")

## new one lul



trips = []

spokes = 8

for i in range(spokes):
    
    j = 2 * i / spokes

    print(j)
    
    trips.append((
        (round(10*sin(pi*j), 2), round(10*cos(pi*j), 2)),
        (round(100*sin(pi*j), 2), round(100*cos(pi*j), 2))
        ))

for trip in trips:
    print(str(trip) + ',')

print("ALALALLALALA NEW TRIPS")

## new one lul

pickup_grid = []
dropoff_grid = []

for y in range(10,201,10):
    for x in range(10, 101, 10):
        pickup_grid.append((x,y))
    for x in range(110, 201, 10):
        dropoff_grid.append((x,y))

fromsample = random.sample(pickup_grid, 200)
tosample = random.sample(dropoff_grid, 200)

trips = []

for i in range(int(len(fromsample))):
    trips.append((fromsample.pop(), tosample.pop()))

for trip in trips:
    print(str(trip) + ',')


print("ALALALLALALA NEW TRIPS")

## new one lul

pickup_grid = []
dropoff_grid = []

for y in range(10, 201, 40):
    for x in range(10, 101, 40):
        pickup_grid.append((x,y))
    for x in range(110, 201, 40):
        dropoff_grid.append((x,y))

trips = []

for i in range(int(len(pickup_grid))):
    trips.append((pickup_grid.pop(), dropoff_grid.pop()))

for trip in trips:
    print(str(trip) + ',')

print("ALALALLALALA NEW TRIPS")

## new one lul

row1 = []

for x in range(10, 201, 10):
    row1.append((x, 10))

row2 = []

for (x,y) in row1[:len(row1)//2]:
    row2.append((x, y + 200))

trips = []

for i in range(len(row1)//2):
    trips.append((row1[i], row1[i+len(row1)//2]))

for i in range(len(row2)//2):
    trips.append((row2[i], row2[i+len(row2)//2]))

for trip in trips:
    print(str(trip) + ',')

print("completed mapgen")