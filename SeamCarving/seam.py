"""
The implementation of the second step in the seam carving algorithm: finding
the lowest-energy seam in an image.

The function you fill out in this module will be used as part of the overall
seam carving process. If you run this module in isolation, the lowest-energy
seam will be visualized.
"""


import sys

from energy import compute_energy
from utils import Color, read_image_into_array, write_array_into_image


class SeamEnergyWithBackPointer:
    """
    Represents the total energy of a seam along with a back pointer:

      - Stores the total energy of a seam that ends at some position in the
        image. The position is not stored because it can be inferred from where
        in a 2D grid this object appears.

      - Also stores the x-coordinate for the pixel in the previous row that led
        to this particular seam energy. This is the back pointer from which the
        entire seam can be reconstructed.
    """

    def __init__(self, energy = 0, x_position_prev_row = None):
        self.energy = energy
        self.x_position_prev_row = x_position_prev_row

def compute_vertical_seam(energy_data):
    """
    Find the lowest-energy vertical seam given the energy of each pixel in the
    input image. The image energy should have been computed before by the
    `compute_energy` function in the `energy` module.

    This is the second version of the seam finding algorithm. In addition to
    storing and finding the lowest-energy value of any seam, you will also store
    back pointers used to reconstruct the lowest-energy seam.

    At the end, you will return a list of x-coordinates where you would have
    returned a single x-coordinate instead.

    This is one of the functions you will need to implement. You may want to
    copy over the implementation of the first version as a starting point.
    Expected return value: a tuple with two values:

      1. The list of x-coordinates forming the lowest-energy seam, starting at
         the top of the image.
      2. The total energy of that seam.
    """

    h = len(energy_data)
    w = len(energy_data[0])
    
    #Initialise a 2D array with BackPointers and the first row is the solution
    result = [[SeamEnergyWithBackPointer() for _ in row] for row in energy_data]
    for j in range(w):
        result[0][j].energy = energy_data[0][j]

    #We are going to use the recurrence relation M(x,y) = energy(x,y) + Min(M(x-1,y-1),M(x,y-1),M(x+1,y))
    for i in range(1, h):
        for j in range(w):
            j0 = j if j == 0 else j - 1
            j1 = j if j == w - 1 else j + 1
            min_val = min(energy_data[i - 1][j0], energy_data[i - 1][j], energy_data[i - 1][j1])
            result[i][j].energy = energy_data[i][j] + min_val
            if energy_data[i - 1][j0] == min_val:
                result[i][j].x_position_prev_row = j0
            elif energy_data[i - 1][j] == min_val:
                result[i][j].x_position_prev_row = j
            else:
                result[i][j].x_position_prev_row = j1
    
    #We now compute the minimum energy of the seam as well as the x_coordinate of the last row
    min_x_last_row, min_energy = min(enumerate(result[h-1][j].energy for j in range(w)))
    #We are going to create a list with all the x_coordinates we want starting from the last row and moving up
    x_coords = [min_x_last_row]
    y_coord  = h-1
    while y_coord > 0:
        #We insert at the end of the list the next x_coordinate
        x_coords.append(result[y_coord][min_x_last_row].x_position_prev_row)
        #We go up one row
        y_coord -= 1
        #Update the min_x_last_row
        min_x_last_row = x_coords[-1]

    #We now reverse the list in place
    x_coords.reverse()
    return x_coords, min_energy


def visualize_seam_on_image(pixels, seam_xs):
    """
    Draws a red line on the image along the given seam. This is done to
    visualize where the seam is.
    """

    h = len(pixels)
    w = len(pixels[0])

    new_pixels = [[p for p in row] for row in pixels]

    for y, seam_x in enumerate(seam_xs):
        min_x = max(seam_x - 2, 0)
        max_x = min(seam_x + 2, w - 1)

        for x in range(min_x, max_x + 1):
            new_pixels[y][x] = Color(255, 0, 0)

    return new_pixels


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

    print('Finding the lowest-energy seam...')
    seam_xs, min_seam_energy = compute_vertical_seam_v2(energy_data)

    print(f'Saving {output_filename}')
    visualized_pixels = visualize_seam_on_image(pixels, seam_xs)
    write_array_into_image(visualized_pixels, output_filename)

    print()
    print(f'Minimum seam energy was {min_seam_energy} at x = {seam_xs[-1]}')
