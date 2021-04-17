"""
The first step in the seam carving algorithm: computing the energy of an image.

The functions you fill out in this module will be used as part of the overall
seam carving process. If you run this module in isolation, the energy of an
image will be visualized as a grayscale heat map, with brighter spots
representing pixels.
"""


import sys

from utils import Color, read_image_into_array, write_array_into_image


def energy_at(pixels, x, y):
    """
    Compute the energy of the image at the given (x, y) position.

    The energy of the pixel is determined by looking at the pixels surrounding
    the requested position. In the case the requested position is at the edge
    of the image, the current position is used whenever a "surrounding position"
    would go out of bounds.
    """
    
    h = len(pixels)
    w = len(pixels[0])

    #Calculate the previous and subsequent x coordinate taking care of the edges of the image
    x0 = x if x == 0 else x - 1
    x1 = x if x == w - 1 else x + 1
    #Now calculate the increments in the RGB colours
    dxr = pixels[y][x0].r - pixels[y][x1].r
    dxg = pixels[y][x0].g - pixels[y][x1].g
    dxb = pixels[y][x0].b - pixels[y][x1].b
    #This is the total increment in x
    dx = dxr * dxr + dxg * dxg + dxb * dxb

    #Ditto for y
    y0 = y if y == 0 else y - 1
    y1 = y if y == h - 1 else y + 1

    dyr = pixels[y0][x].r - pixels[y1][x].r
    dyg = pixels[y0][x].g - pixels[y1][x].g
    dyb = pixels[y0][x].b - pixels[y1][x].b
    dy = dyr * dyr + dyg * dyg + dyb * dyb

    #The energy is then the sum of the increments in both the x and y axes
    return dx + dy

def compute_energy(pixels):
    """
    Compute the energy of the image at every pixel.

    The input is given as a 2D array of colors, and the output is a 2D
    array of numbers, each representing the energy value at the corresponding
    position.
    """
    h = len(pixels)
    w = len(pixels[0])
    
    return [[energy_at(pixels, j, i) for j in range(w)] for i in range(h)]


def energy_data_to_colors(energy_data):
    """
    Convert the energy values at each pixel into colors that can be used to
    visualize the energy of the image. The steps to do this conversion are:

      1. Normalize the energy values to be between 0 and 255.
      2. Convert these values into grayscale colors, where the RGB values are
         all the same for a single color.
    """

    colors = [[0 for _ in row] for row in energy_data]

    max_energy = max(
        energy
        for row in energy_data
        for energy in row
    )

    for y, row in enumerate(energy_data):
        for x, energy in enumerate(row):
            energy_normalized = round(energy / max_energy * 255)
            colors[y][x] = Color(
                energy_normalized,
                energy_normalized,
                energy_normalized
            )

    return colors


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f'USAGE: {__file__} <input> <output>')
        sys.exit(1)

    input_filename = sys.argv[1]
    output_filename = sys.argv[2]

    print(f'Reading {input_filename}...')
    pixels = read_image_into_array(input_filename)

    print('Computing the energy...')
    energy_data = compute_energy(pixels)
    energy_pixels = energy_data_to_colors(energy_data)

    print(f'Saving {output_filename}')
    write_array_into_image(energy_pixels, output_filename)
