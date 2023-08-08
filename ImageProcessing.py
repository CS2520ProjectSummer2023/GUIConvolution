import numpy
import math


from PIL import Image


def edge_detector(image):
    """Open an image and perform the image convolution on it"""

    """Create a copy of the image so that we can place the new pixels onto"""
    img = Image.open(image).convert("L")
    img_new = Image.open(image).convert("L")

    pixels_new = img_new.load()

    height, width = img.size

    kernel_matrix = numpy.zeros([3, 3], dtype=int)
    x_operator = [-1, 0, 1], [-2, 0, 2], [-1, 0, 1]
    y_operator = [1, 2, 1], [0, 0, 0], [-1, -2, -1]

    gx = numpy.array(x_operator)
    gy = numpy.array(y_operator)

    for i in range(1, height - 1):
        for j in range(1, width - 1):
            # Grab each pixel in a one pixel radius of pixel (i,j)
            kernel_matrix[0][0] = img.getpixel((i - 1, j - 1))
            kernel_matrix[0][1] = img.getpixel((i - 1, j))
            kernel_matrix[0][2] = img.getpixel((i - 1, j + 1))
            kernel_matrix[1][0] = img.getpixel((i, j - 1))
            kernel_matrix[1][1] = img.getpixel((i, j))
            kernel_matrix[1][2] = img.getpixel((i, j + 1))
            kernel_matrix[2][0] = img.getpixel((i + 1, j - 1))
            kernel_matrix[2][1] = img.getpixel((i + 1, j))
            kernel_matrix[2][2] = img.getpixel((i + 1, j + 1))
            edge = int(compute_convolution(kernel_matrix, gx, gy))
            #Place the value of the edge into the pixel
            pixels_new[i, j] = edge

    return img_new


def compute_direction(pixel_matrix, direction_matrix):
    """Compute the directional value of the pixels based on the passed in Direction Matrix"""
    directional_value = 0
    for i in range(3):
        for j in range(3):
            directional_value = directional_value + (pixel_matrix[i][j] * direction_matrix[i][j])

    return directional_value


def compute_convolution(pixel_matrix, x_direction, y_direction):
    """Compute the convolution of the pixel matrix based on the x and y direction of the pixel matrix"""
    x_direction = compute_direction(pixel_matrix, x_direction)
    y_direction = compute_direction(pixel_matrix, y_direction)

    return math.sqrt(math.pow(x_direction, 2) + math.pow(y_direction, 2))


def greyscale_image(image):
    """Apply a greyscale filter to an image using the greyscale formula of (.299 * R) + (.587 * G) + (0.114 * B)"""
    img = Image.open(image)
    pixels = img.load()

    height, width = img.size
    for i in range(0, height):
        for j in range(0, width):
            #Grab the tuple of RGB values at the specified pixel
            rgb_tuple = img.getpixel((i, j))
            #Apply the greyscale formula
            grey_scale_value = ((0.299 * rgb_tuple[0]) + (0.587 * rgb_tuple[1]) + (0.114 * rgb_tuple[2]))
            #Apple the greyscale value to each RGB value at that pixel
            pixels[i, j] = (int(grey_scale_value), int(grey_scale_value), int(grey_scale_value))

    return img


def image_inversion(image):
    """Invert the colors on an image by getting the inverse RGB of each pixel"""
    img = Image.open(image)
    pixels = img.load()
    height, width = img.size
    # Iterate over the image and apply the color inversion formula
    for i in range(0, height):
        for j in range(0, width):
            rgb_tuple = img.getpixel((i, j))
            red = 255 - rgb_tuple[0]
            green = 255 - rgb_tuple[1]
            blue = 255 - rgb_tuple[2]

            #Place the new RGB values at pixel(i,j)
            pixels[i, j] = (red, green, blue)

    return img


def gaussian_blur(image):
    """Apply a gaussian blur to an image with the sigma set to 1, and the radius of the kernel set to 1"""
    img = Image.open(image)
    img_new = Image.open(image)
    pixels_new = img_new.load()

    height, width = img.size
    radius = 1
    sigma = 1
    #Initialize size of kernel based on radius
    kernel_width = (2 * radius) + 1
    kernel_matrix = numpy.zeros([kernel_width, kernel_width], dtype=float)
    #Initialize kernel sum to 0
    kernel_sum = 0


    #Precompute the weight matrix so it doesn't need to be computed multiple times
    compute_weight_matrix(kernel_matrix, kernel_sum, radius, sigma, kernel_width)

    for x in range(radius, height - radius):
        for y in range(radius, width - radius):
            #Initialize the RGB values to zero
            red = 0
            green = 0
            blue = 0
            # Collect the RGB values of the pixels within a one pixel radius of (x,y) defined in the loops above
            for kernel_x in range(-radius, radius + 1):
                for kernel_y in range(-radius, radius + 1):
                    # Grab the RGB values and multiply them by the values within the weight matrix
                    kernel_value = kernel_matrix[kernel_x + radius][kernel_y + radius]
                    red += img.getpixel((x - kernel_x, y - kernel_y))[0] * kernel_value
                    green += img.getpixel((x - kernel_x, y - kernel_y))[1] * kernel_value
                    blue += img.getpixel((x - kernel_x, y - kernel_y))[2] * kernel_value
            # Place thew new pixels at position (x,y)
            pixels_new[x, y] = (int(red), int(green), int(blue))

    return img_new


def compute_weight_matrix(k_matrix, kernel_sum, radius, sigma, width):
    """Precomputes the weight matrix used for applying the gaussian blur to an image.
    This is done using the formula (1/(2* PI * Sigma ^2)) * e (^ -((x^2) + (y^2))/ (2* Sigma ^2))"""
    gauss_denominator = 1 / (2 * math.pi * sigma ** 2)
    for x in range(-radius, radius + 1):
        for y in range(-radius, radius + 1):
            gauss_exponent = -((x ** 2) + (y ** 2)) / (2 * (sigma ** 2))
            gauss_value = gauss_denominator * (math.e ** gauss_exponent)
            #Place the gauss value into the kernel matrix based on the x and y loop variables
            k_matrix[x][y] = gauss_value
            #Sum the gauss value into the running sum of the kernel sum
            kernel_sum += gauss_value

    normalize_matrix(k_matrix, kernel_sum, width)


def normalize_matrix(k_matrix, matrix_sum, k_width):
    """Normalize the weights in the matrix so that the entire matrix can add up to 1"""
    for x in range(k_width):
        for y in range(k_width):
            k_matrix[x][y] = k_matrix[x][y] / matrix_sum


def sharpen_image(image):
    """Sharpens and image by applying a blur, then subtracting it from the original, then adding it again"""
    img = Image.open(image)
    img_blurred = gaussian_blur(image)
    pixels = img.load()
    pixels_blurred = img_blurred.load()

    height, width = img.size

    # Sharpening pass for the image using a generic formula of 2 * (Original Image) - (Blurred Image)
    for x in range(0, height):
        for y in range(0, width):
            rgb_tuple_original = pixels[x, y]
            rgb_tuple_blurred = pixels_blurred[x, y]
            pixels_blurred[x, y] = (int(2 * rgb_tuple_original[0] - rgb_tuple_blurred[0]),
                                    int(2 * rgb_tuple_original[1] - rgb_tuple_blurred[1]),
                                    int(2 * rgb_tuple_original[2] - rgb_tuple_blurred[2]))

    return img_blurred
