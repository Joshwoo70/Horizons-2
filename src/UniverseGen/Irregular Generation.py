import random
import math
from PIL import ImageDraw, Image
# Quick Filename
RAND = random.randrange(0, 108000000000)

# ---------------------------------------------------------------------------
NAME = input('Galaxy Name:')

HSB = int(input(
    'Galaxy Size Bracket <0 = 1-100, 1 = 100-1000, 2 = 1000-100000, 3 = 100000-1000000, 4 = 1000000-2000000>:'))

NUMC = (random.randint(0, 12))

if HSB == 0:
    NUMSTR = random.randrange(1, 100)
elif HSB == 1:
    NUMSTR = random.randrange(100, 1000)
elif HSB == 2:
    NUMSTR = random.randrange(1000, 100000)
elif HSB == 3:
    NUMSTR = random.randrange(100000, 1000000)
elif HSB == 4:
    NUMSTR = random.randrange(1000000, 2000000)

print(NUMSTR)

NUMCLUS = NUMSTR / 70

DISCLUS = NUMCLUS / 4

GALX = int(NUMSTR / (random.randrange(8, 20)))

GALY = int(NUMSTR / (random.randrange(6, 28)))

GALZ = int(NUMSTR / (random.randrange(10, 40)))

CLUSRAD = NUMCLUS / 5

DISCLRAD = CLUSRAD / 5

PNGSIZEA = GALX / 5

PNGFRAMEA = PNGSIZEA / 10

PNGSIZE = float(input('X and Y Size of PNG <Default:Bad Idea>:') or str(PNGSIZEA))

PNGFRAME = float(input('PNG Frame Size <Default:Bad Idea>:') or str(PNGFRAMEA))

stars = []
clusters = []

star_color_dict = {
    0: (229, 30, 30),
    1: (203, 30, 26),
    2: (181, 18, 6),
    3: (200, 39, 13),
    4: (200, 63, 21),
    5: (222, 137, 10),
    6: (212, 178, 42),
    7: (210, 188, 38),
    8: (217, 207, 66),
    9: (222, 226, 125),
    10: (222, 226, 160),
    11: (255, 255, 253),
    12: (255, 255, 255),
    13: (253, 255, 255),
    14: (250, 255, 255),
    15: (222, 243, 255),
    16: (222, 243, 255),
    17: (230, 243, 255),
    18: (140, 176, 255),
    19: (140, 176, 225)
}

SGX = GALX * 0.2
SGY = GALY * 0.2
SCRAD = CLUSRAD * 0.06
NUMCLUSA = NUMCLUS - DISCLUS
NUMCLUSB = NUMCLUS + DISCLUS
CLUSRADA = CLUSRAD - DISCLRAD
CLUSRADB = CLUSRAD + DISCLRAD
NUMCB = NUMC + 1


def generateclusters():
    c = 0
    while c < NUMCB:
        # random distance from centre
        dist = random.uniform(CLUSRAD, (GALX))
        # any rotation- clusters can be anywhere
        theta = random.random() * 360
        cx = math.cos(theta * math.pi / 180.0) * dist
        cy = math.sin(theta * math.pi / 180.0) * dist
        cz = random.random() * GALZ * 2.0 - GALZ
        rad = random.uniform(CLUSRADA, CLUSRADB)
        num = random.uniform(NUMCLUSA, NUMCLUSB)
        # add cluster to clusters array
        clusters.append((cx, cy, cz, rad, num))
        # process next
        c = c + 1
        sran = 0
        cran = 0


def generateStars():
    # Now generate the Hub. This places a point on or under the curve
    # maxHubZ - s d^2 where s is a scale factor calculated so that z = 0 is
    # at maxHubR (s = maxHubZ / maxHubR^2) AND so that minimum hub Z is at
    # maximum disk Z. (Avoids edge of hub being below edge of disk)

    scale = GALZ / (GALX * GALY)
    i = 0
    while i < NUMSTR:
        # Choose a random distance from center
        distX = random.randrange(0, GALX)
        distY = random.randrange(0, GALY)
        distXb = distX + random.uniform(0, SGX)
        distYb = distY + random.uniform(0, SGY)

        # Any rotation (points are not on arms)
        theta = random.random() * 360

        # Convert to cartesian
        x = math.cos(theta * math.pi / 180.0) * distXb
        y = math.sin(theta * math.pi / 180.0) * distYb
        z = (random.random() * 2 - 1) * (GALZ - scale * distXb * distYb)

        # Replaces the if/elif logic with a simple lookup. Faster and
        # and easier to read.
        scol = star_color_dict[random.randrange(0, 19)]

        # Add star to the stars array
        stars.append((x, y, z, scol))

        # Process next star
        i = i + 1
        sran = 0

    c = 0
    while c < NUMCB:
        for (cx, cy, cz, rad, num) in clusters:
            scale = rad / (rad * rad)
            i = 0
            while i < num:
                dist = random.uniform(-rad, rad)
                distb = dist + random.uniform(0, SCRAD)
                theta = random.random() * 360
                # Cartesian!
                x = cx + (math.cos(theta * math.pi / 180) * distb)
                y = cy + (math.sin(theta * math.pi / 180) * distb)
                z = (random.random() * 2 - 1) * ((cz + rad) - scale * distb * distb)
                scol = star_color_dict[random.randrange(0, 19)]
                stars.append((x, y, z, scol))
                i = i + 1
                sran = 0
        c = c + 1


def drawToPNG(filename):
    image = Image.new("RGB", (int(PNGSIZE), int(PNGSIZE)), PNGBGCOLOR)
    draw = ImageDraw.Draw(image)

    # Find maximal star distance
    max = 0
    for (x, y, z, scol) in stars:
        if abs(x) > max:
            max = x
        if abs(y) > max:
            max = y
        if abs(z) > max:
            max = z

    # Calculate zoom factor to fit the galaxy to the PNG size
    factor = float(PNGSIZE - PNGFRAME * 2) / (max * 2)
    for (x, y, z, scol) in stars:
        sx = factor * x + PNGSIZE / 2
        sy = factor * y + PNGSIZE / 2
        draw.point((sx, sy), fill=scol)

    # Save the PNG
    image.save(filename)
    print(filename)


# Generate the galaxy
generateclusters()
generateStars()

# Save the galaxy as PNG to galaxy.png
drawToPNG("irregulargalaxy" + str(RAND) + "-" + str(NAME) + ".png")

# Create the galaxy's data galaxy.txt
with open("irregulargalaxy" + str(RAND) + "-" + str(NAME) + ".txt", "w") as text_file:
    text_file.write("Galaxy Number: {}".format(RAND))
    text_file.write("Galaxy Name: {}".format(NAME))
    text_file.write("Number of Clusters: {}".format(NUMC))
    text_file.write("Stars: {}".format(NUMSTR))
    text_file.write("Number of Stars per Cluster {}".format(NUMCLUS))
    text_file.write("Star Number Distribution per Cluster {}".format(DISCLUS))
    text_file.write("Galaxy X Length: {}".format(GALX))
    text_file.write("Galaxy Y Length: {}".format(GALY))
    text_file.write("Galaxy Z Length: {}".format(GALZ))
    text_file.write("Cluster Radius: {}".format(CLUSRAD))
    text_file.write("Cluster Radius Distribution: {}".format(DISCLRAD))
    text_file.write("Image Size: {}".format(PNGSIZE))
    text_file.write("Frame Size: {}".format(PNGFRAME))