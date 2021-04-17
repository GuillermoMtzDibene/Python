This four modules implement an algorithm called "Seam Carving" and I am using the pillow library (Python Image Library).

The algorithm read an image in RGB form. That is, each pixel lies in three-dimensional space with coordinates (R,G,B) each one being a number between 0 and 255.
Then, the algorithm calculates the squared distance form a pixel to its four neighbours and calls the sum of this distances the energy.
Having these energies, and using dynamic programming, we calculate the continuous sequence from top to bottom of pixels with least energy (the entire sequence has minimal energy).
This sequence is then deleted. The algorithm is repeated a specified number of times, effectively narrowing the given image by a given any desired number of pixels.
This algorithm is relatively slow. See the documentation for more information.

This algorithm was the final project in a workshop about dynamic programming; the functions and overall structure of the algorithm was provided by the instructor.
The actual code in each function and the class definitions was made by me.
