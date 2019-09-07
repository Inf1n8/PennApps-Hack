import io
import os
from PIL import Image

imagePath = ""

def findDistances(gun, people):
    print("===========================")
    (gXMin, gYMin, gXMax, gYMax) = gun
    gXCenter = (gXMax + gXMin / 2.)
    gYCenter = (gYMax + gYMin / 2.)
    print("gXCenter: ", gXCenter)
    print("gYCenter: ", gYCenter)

    distance = 10000000000.
    id = -1

    ROIxMin, ROIyMin, ROIxMax, ROIyMax = 0., 0., 0., 0.
    for (i, (pXMin, pYMin, pXMax, pYMax)) in enumerate(people):
        pXCenter = (pXMax + pXMin / 2.)
        pYCenter = (pYMax + pYMin / 2.)
        print("pXCenter: ",pXCenter)
        print("pYCenter: ", pYCenter)

        tmpX = (gXCenter - pXCenter)**2
        tmpY = (gYCenter - pYCenter)**2
        dist = (tmpX + tmpY)**0.5
        print("dist: ", dist)
        if dist < distance:
            distance = dist
            id = i
            ROIxMin, ROIyMin, ROIxMax, ROIyMax = pXMin, pYMin, pXMax, pYMax

    print("===========================")
    return id, distance, (ROIxMin, ROIyMin, ROIxMax, ROIyMax)


def localize_objects(path):
    """Localize objects in the local image.

    Args:
    path: The path to the local file.
    """
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()

    with open(path, 'rb') as image_file:
        content = image_file.read()
    image = vision.types.Image(content=content)

    objects = client.object_localization(
        image=image).localized_object_annotations

    gun = tuple()
    people = []
    print('Number of objects found: {}'.format(len(objects)))
    for object_ in objects:
        print('\n{} (confidence: {})'.format(object_.name, object_.score))

        if object_.name == "Gun" or object_.name == "Weapon" or object_.name == "Handgun":
            print('Normalized bounding polygon vertices: ')
            xMin, ymin, xMax, yMax = 0.0, 0.0, 0.0, 0.0
            # tmpX = []
            # tmpY = []

            for (i, vertex) in enumerate(object_.bounding_poly.normalized_vertices):
                if i == 0:
                    xMin= vertex.x
                    yMin = vertex.y
                if i == 1:
                    xMax = vertex.x
                if i == 2:
                    yMax = vertex.y
                # tmpX.append(vertex.x)
                # tmpY.append(vertex.y)
                print(' - ({}, {})'.format(vertex.x, vertex.y))

            gun = (xMin, yMin, xMax, yMax)

        if object_.name == "Man" or object_.name == "Person" or object_.name == "Woman":
            print('Normalized bounding polygon vertices: ')
            xMin, ymin, xMax, yMax = 0.0, 0.0, 0.0, 0.0
            for (i, vertex) in enumerate(object_.bounding_poly.normalized_vertices):
                if i == 0:
                    xMin= vertex.x
                    yMin = vertex.y
                if i == 1:
                    xMax = vertex.x
                if i == 2:
                    yMax = vertex.y
                print(' - ({}, {})'.format(vertex.x, vertex.y))

            people.append((xMin, yMin, xMax, yMax))

    return gun, people





gun, people = localize_objects(imagePath)
print(gun)
print(people)
id, distance, (ROIxMin, ROIyMin, ROIxMax, ROIyMax) = findDistances(gun, people)
print(id, distance, ROIxMin, ROIyMin, ROIxMax, ROIyMax)

im = Image.open(imagePath)
width, height = im.size
left = width * ROIxMin
top = height - (height * ROIyMax)
right = width * ROIxMax
bottom = height - (height * ROIyMin)
print(left, top, right, bottom)
im1 = im.crop((left, top, right, bottom))
im1.show()