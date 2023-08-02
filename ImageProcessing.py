import numpy
import math

import numpy as np
from PIL import Image


def edge_detector(image):
    """Open an image and perform the image convolution on it"""

    """Create a copy of the image so that we can place the new pixels onto"""
    img = Image.open(image).convert("L")
    imgNew = Image.open(image).convert("L")
    pixels = img.load()
    pixelsNew = imgNew.load()

    height, width = img.size

    kernelMatrix = numpy.zeros([3, 3], dtype=int)
    XOperator = [-1, 0, 1], [-2, 0, 2], [-1, 0, 1]
    YOperator = [1, 2, 1], [0, 0, 0], [-1, -2, -1]

    Gx = numpy.array(XOperator)
    Gy = numpy.array(YOperator)

    for i in range(1, height - 1):
        for j in range(1, width - 1):
            kernelMatrix[0][0] = img.getpixel((i - 1, j - 1))
            kernelMatrix[0][1] = img.getpixel((i - 1, j))
            kernelMatrix[0][2] = img.getpixel((i - 1, j + 1))
            kernelMatrix[1][0] = img.getpixel((i, j - 1))
            kernelMatrix[1][1] = img.getpixel((i, j))
            kernelMatrix[1][2] = img.getpixel((i, j + 1))
            kernelMatrix[2][0] = img.getpixel((i + 1, j - 1))
            kernelMatrix[2][1] = img.getpixel((i + 1, j))
            kernelMatrix[2][2] = img.getpixel((i + 1, j + 1))
            edge = int(compute_convolution(kernelMatrix, Gx, Gy))
            pixelsNew[i, j] = (edge)

    return imgNew


def compute_direction(PixelMatrix, DirectionMatix):
    directional_value = 0
    for i in range(3):
        for j in range(3):
            directional_value = directional_value + (PixelMatrix[i][j] * DirectionMatix[i][j])

    return directional_value


def compute_convolution(PixelMatrix, XDirection, YDirection):
    y_direction = compute_direction(PixelMatrix, YDirection)
    x_direction = compute_direction(PixelMatrix, XDirection)

    return math.sqrt(math.pow(x_direction, 2) + math.pow(y_direction, 2))


def greyscale_image(image):
    img = Image.open(image)
    pixels = img.load()
    img.show()

    height, width = img.size
    for i in range(0, height):
        for j in range(0, width):
            RGBTuple = img.getpixel((i, j))
            greyScaleValue = ((0.299 * RGBTuple[0]) + (0.587 * RGBTuple[1]) + (0.114 * RGBTuple[2]))
            pixels[i, j] = (int(greyScaleValue), int(greyScaleValue), int(greyScaleValue))

    return img


def image_inversion(image):
    img = Image.open(image)
    pixels = img.load()
    height, width = img.size
    for i in range(0, height):
        for j in range(0, width):
            RGBTuple = img.getpixel((i, j))
            red = 255 - RGBTuple[0]
            green = 255 - RGBTuple[1]
            blue = 255 - RGBTuple[2]

            pixels[i, j] = (red, green, blue)

    return img



